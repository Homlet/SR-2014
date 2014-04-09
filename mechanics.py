from time import time, sleep
from math import copysign, floor, modf
from threading import Thread

from sr import INPUT_PULLUP

from log import log, indented


NOTCHES_ON_WHEEL = 4
ROBOT_RADIUS = 0.185
M_SWITCH_LEFT = 13
M_SWITCH_RIGHT = 12
WHEEL_CIRCUMFERENCE = 0.31
LEFT_ARM = 1
ARMS_LIFT = 0
RIGHT_ARM = 2
ARMS_FORWARDS_STOP = 10  # TODO
ARMS_BACKWARDS_STOP = 9  # TODO


class Journey:
    """
    Handles straight or rotational movement using threading.
    """
    def __init__(self, robot, distance=0, angle=0):
        self.robot = robot
        rduino = robot.ruggeduinos[0]

        self.run = True
        if distance != 0:
            self.length = distance
            log(robot, "Creating journey with dist=%.1f" % (distance))
            approx = (50, 3.7)
        elif angle != 0:
            self.length = -angle * ROBOT_RADIUS
            log(robot, "Creating journey with angle=%.1f" % (angle))
            approx = (40, 8)
        else:
            self.run = False
            approx = (0, 0)
            return

        turnsToDo = self.length / WHEEL_CIRCUMFERENCE

        self.m0 = Motor(
            robot.motors[0].m0, M_SWITCH_LEFT, rduino, turnsToDo, approx
        )
        if angle != 0:
            turnsToDo *= -1
        self.m1 = Motor(
            robot.motors[0].m1, M_SWITCH_RIGHT, rduino, turnsToDo, approx
        )

    def start(self):
        if self.run:
            log(self.robot, "Starting journey...")
            self.m0.start()
            self.m1.start()
            self.m0.join()
            self.m1.join()
            log(self.robot, "done.")
        else:
            log(self.robot, "Warning: cannot run zero-length journey.")


class Motor(Thread):
    """
    Drives a motor a given number of turns using micro-switches or,
    for small distances, approximation. Runs concurrently.
    """
    def __init__(self, motor, switchID, rduino, turns, approx):
        super(Motor, self).__init__()
        self.switchID = switchID
        self.motor = motor
        self.turns = turns
        self.approx = approx
        self.ruggeduino = rduino
        self.ruggeduino.pin_mode(switchID, INPUT_PULLUP)

    def time_a_switch(self):
        """
        At exit point of this function switch is pressed.
        It returns time difference between 2 consecutive switch triggers
        """
        while not self.ruggeduino_input():
            pass
        start = time()
        while self.ruggeduino_input():
            pass
        return time() - start

    def ruggeduino_input(self):
        return self.ruggeduino.digital_read(self.switchID)

    def run(self):
        triggers = abs(self.turns) * NOTCHES_ON_WHEEL
        if triggers < 2:
            self.motor.power = copysign(self.approx[0], self.turns)
            sleep(self.approx[1] * abs(self.turns) * WHEEL_CIRCUMFERENCE)
        else:
            self.motor.power = copysign(50, self.turns)
            total_t = 0
            i = 0

            start_dt = self.time_a_switch()
            for i in range(1, int(floor(triggers))):
                total_t += self.time_a_switch()

            if i != 0:
                average_dt = total_t / i

            if start_dt < average_dt:
                sleep(average_dt - start_dt)
            sleep(average_dt * modf(triggers)[0])
        self.stop()

    def stop(self):
        self.motor.power = -copysign(10, self.turns)
        sleep(0.1)
        self.motor.power = 0


def open_arms(robot):
    robot.servos[0][LEFT_ARM] = 50
    robot.servos[0][RIGHT_ARM] = 50


def close_arms(robot):
    pos = 90
    robot.servos[0][LEFT_ARM] = pos
    robot.servos[0][RIGHT_ARM] = 100 - pos


def raise_arms(robot):
    robot.servos[0][ARMS_LIFT] = 63


def lower_arms(robot):
    robot.servos[0][ARMS_LIFT] = 100


def init_arms_pins(robot):
    robot.ruggeduinos[0].pin_mode(ARMS_FORWARDS_STOP, INPUT_PULLUP)
    robot.ruggeduinos[0].pin_mode(ARMS_BACKWARDS_STOP, INPUT_PULLUP)


@indented
def extend_arms(robot, power):
    stop_pin = ARMS_BACKWARDS_STOP if power >= 0 else ARMS_FORWARDS_STOP

    hit_stop = False
    beyond_time_limit = False

    if stop_pin == ARMS_FORWARDS_STOP:
        log(robot, "Extending arms.")
    else:
        log(robot, "Retracting arms.")
    start = time()
    robot.motors[1].m1.power = power
    while not (hit_stop or beyond_time_limit):
        hit_stop = not robot.ruggeduinos[0].digital_read(stop_pin)
        log(robot, hit_stop)
        beyond_time_limit = time() > start + 3  # Failsafe limit
    robot.motors[1].m1.power = 0
    log(robot, "Stopping arms.")
