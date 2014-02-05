from time import clock
from math import copysign

NOTHES_PER_WHEEL = 9
WHEEL_SEPARATION = 0.37
M_SWITCH_LEFT  = 12
M_SWITCH_RIGHT = 2
WHEEL_CIRCUMFERENCE = 0.31

class Motor():
    def __init__(self, motor, switchID, rduino, k):
        self.motor = motor
        self.power = 50 * k
        self.k = k
        self.switchID = switchID
        self.ruggeduino = rduino

        self.turnsMade = 0
        self.notchesPassed = 0
        self.timeActive = 0

    # If time_a_switch() takes too long - better use threading.
    def time_a_switch(self):
        while self.ruggeduino.digital_read(self.switchID) is True:
            pass
        start = clock()
        while self.ruggeduino.digital_read(self.switchID) is False:
            pass
        return clock() - start

    def count_notches(self):
        self.timeActive += self.time_a_switch()
        self.notchesPassed += 1

    def set_power(self, power):
        self.power = power
        self.start()

    def start(self):
        self.motor.power = self.power

    def stop(self):
        self.motor.power = 0


class Journey:
    def __init__(self, robot, distance=0, angle=0):
        self.robot = robot
        rduino = self.robot.ruggeduinos[0]

        if distance != 0:
            self.length = distance
        elif angle != 0:
            self.length = angle * WHEEL_SEPARATION / 2

# Better use notches here.
        self.turnsToDo = abs(self.length // WHEEL_CIRCUMFERENCE)
        direction1 = copysign(1, self.length)
        direction2 = direction1
        if angle != 0:
            direction2 *= -1
      
        self.m1 = Motor(robot.motors[0].m0, M_SWITCH_LEFT, rduino, direction1)
        self.m2 = Motor(robot.motors[0].m1, M_SWITCH_RIGHT, rduino, direction2)

    def start(self):
        for each in [self.m1, self.m2]: each.start()

        while (m1.notchesPassed // NOTHES_PER_WHEEL) < self.turnsToDo:
            self.m1.count_notches()
            self.m2.count_notches()
            self.sync_power()
            sleep(0.05)  # Sync every 0.05 seconds?

        self.m1.stop()
        self.m2.stop()

    def sync_power(self):
        # Increase/Decrease power.
        # Should vary depending on turns/time difference between motors.
        # Number of significant figures is important here
        # Need to work out number of significant figures to be used.
        # 10 is just very rough estimate and should be properly worked out.
        base_notch_dt = self.m1.time_a_switch()
        notch_dt = self.m2.time_a_switch()
        m2.set_power(m2.power + (notch_dt-base_notch_dt)*10*m2.k)