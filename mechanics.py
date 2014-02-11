from time import time, sleep
from math import copysign, floor, fmod
from threading import Thread

from sr import INPUT_PULLUP

NOTCHES_ON_WHEEL = 4
ROBOT_RADIUS = 0.185
M_SWITCH_LEFT  = 12
M_SWITCH_RIGHT = 2
WHEEL_CIRCUMFERENCE = 0.31

# average dt for right wheel notch at power = 50
        # is 30 ms
# same thing for left wheel
        # is 70 ms 

# Right wheel usually turns a bit quicker, according to notches

class Journey:
    def __init__(self, robot, distance=0, angle=0):
        self.robot = robot
        rduino = self.robot.ruggeduinos[0]

        if distance != 0:
            self.length = distance
        elif angle != 0:
            self.length = angle * ROBOT_RADIUS

        turnsToDo = self.length / WHEEL_CIRCUMFERENCE
      
        self.m0 = Motor(robot.motors[0].m0, M_SWITCH_LEFT, rduino, turnsToDo)
        if angle != 0:
            turnsToDo *= -1
        self.m1 = Motor(robot.motors[0].m1, M_SWITCH_RIGHT, rduino, turnsToDo)

    def start(self):
        self.m0.start()
        self.m1.start()
        self.m0.join()
        self.m1.join()


class Motor(Thread):
    def __init__(self, motor, switchID, rduino, turns):
        Thread.__init__(self)
        self.motor = motor
        self.power = 35 * copysign(1, turns)
        self.turnsToDo = abs(turns)
        self.switchID = switchID
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
            sleep(3.75 * self.turnsToDo * WHEEL_CIRCUMFERENCE)
        else:
            total_t = 0
            i = 0

            start_dt = self.time_a_switch()
            for i in range(1, floor(triggersToDo)):
                total_t += self.time_a_switch()

            if i != 0:
                average_dt = total_t / i

            if start_dt < average_dt:
                sleep(average_dt - start_dt)
            sleep(average_dt * fmod(triggersToDo)[0])
        self.stop()

    def stop(self):
        self.motor.power = -self.power * 0.3
        sleep(0.1)
        self.motor.power = 0