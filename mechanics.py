from time import time, sleep
from math import copysign, floor, modf
from threading import Thread

from sr import INPUT_PULLUP


NOTCHES_ON_WHEEL = 4
ROBOT_RADIUS = 0.185
M_SWITCH_LEFT  = 12
M_SWITCH_RIGHT = 13
WHEEL_CIRCUMFERENCE = 0.31

# Notes on approximation:
#
# Average dt for right wheel notch at power = 50 is
#     30 ms.
# Same thing for left wheel is
#     70 ms.
# Right wheel usually turns a bit quicker, according to notches.

class Journey:
    """
    Handles a forwards or rotational movement using threading.
    """
    def __init__(self, robot, distance=0, angle=0):
        self.robot = robot
        rduino = self.robot.ruggeduinos[0]

        self.run = True
        if distance != 0:
            self.length = distance
        elif angle != 0:
            self.length = -angle * ROBOT_RADIUS
        else:
            self.run = False
            return

        turnsToDo = self.length / WHEEL_CIRCUMFERENCE
      
        self.m0 = Motor(robot.motors[0].m0, M_SWITCH_LEFT, rduino, turnsToDo)
        if angle != 0:
            turnsToDo *= -1
        self.m1 = Motor(robot.motors[0].m1, M_SWITCH_RIGHT, rduino, turnsToDo)

    def start(self):
        if self.run:
            self.m0.start()
            self.m1.start()
            self.m0.join()
            self.m1.join()
        else:
            print "Warning: cannot run zero-length journey."


class Motor(Thread):
    """
    Drives a motor a given number of turns using micro-switches or,
    for small distances, approximation. Runs concurrently.
    """
    def __init__(self, motor, switchID, rduino, turns):
        super(Motor, self).__init__()
        self.switchID = switchID
        self.motor = motor
        self.power = 35 * copysign(1, turns)
        if self.switchID == 2:
            self.power *= 1
        self.turnsToDo = abs(turns)
        self.ruggeduino = rduino
        self.ruggeduino.pin_mode(switchID, INPUT_PULLUP)

    def time_a_switch(self):
        """
        At exit point of this function switch is pressed.
        It returns time difference between 2 consecutive switch triggers
        """
        while self.ruggeduino_input() is False:
            pass
        start = time()
        while self.ruggeduino_input() is True:
            pass
        return time() - start

    def ruggeduino_input(self):
        return self.ruggeduino.digital_read(self.switchID)

    def run(self):
        triggersToDo = self.turnsToDo * NOTCHES_ON_WHEEL
        self.motor.power = self.power
        if triggersToDo < 2:
            # Probably need different powers for turning/moving forward of the robot
            sleep(5 * self.turnsToDo * WHEEL_CIRCUMFERENCE)
        else:
            total_t = 0
            i = 0

            start_dt = self.time_a_switch()
            for i in range(1, int(floor(triggersToDo))):
                total_t += self.time_a_switch()

            if i != 0:
                average_dt = total_t / i

            if start_dt < average_dt:
                sleep(average_dt - start_dt)
            sleep(average_dt * modf(triggersToDo)[0])
        self.stop()

    def stop(self):
        # self.motor.power = -self.power * 0.3
        # sleep(0.1)
        self.motor.power = 0
