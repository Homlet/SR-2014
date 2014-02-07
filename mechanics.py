from time import clock, sleep
from math import copysign

from sr import INPUT_PULLUP

NOTHES_PER_WHEEL = 4
ROBOT_RADIUS = 0.185
M_SWITCH_LEFT  = 12
M_SWITCH_RIGHT = 2
WHEEL_CIRCUMFERENCE = 0.31

class Motor:
    def __init__(self, motor, switchID, rduino, k):
        self.motor = motor
        self.power = 50 * k
        self.k = k
        self.switchID = switchID
        self.ruggeduino = rduino
        self.ruggeduino.pin_mode(switchID, INPUT_PULLUP)

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
        dt = clock() - start
        print 'Time for a notch:%.8f' % (dt)
        return dt
        # return clock() - start

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
            self.length = angle * ROBOT_RADIUS

        # Better use notches here.
        self.turnsToDo = abs(self.length // WHEEL_CIRCUMFERENCE)
        direction1 = copysign(1, self.length)
        direction2 = direction1
        if angle != 0:
            direction2 *= -1
      
        self.m0 = Motor(robot.motors[0].m0, M_SWITCH_LEFT, rduino, direction1)
        self.m1 = Motor(robot.motors[0].m1, M_SWITCH_RIGHT, rduino, direction2)

    def start(self):
        for each in [self.m0, self.m1]: each.start()

        while (self.m1.notchesPassed // NOTHES_PER_WHEEL) < self.turnsToDo:
            a = clock()
            self.m0.count_notches()
            self.m1.count_notches()
            print 'Time delay due to timing (loop): %.8f' % (clock() - a)
            self.sync_power()
            sleep(2)  # Sync every 0.05 seconds?

        self.m0.stop()
        self.m1.stop()

    def sync_power(self):
        # Increase/Decrease power.
        # Should vary depending on turns/time difference between motors.
        # Number of significant figures is important here
        # Need to work out number of significant figures to be used.
        # 10 is just very rough estimate and should be properly worked out.
        base_notch_dt = self.m0.time_a_switch()
        notch_dt = self.m1.time_a_switch()

        dt = notch_dt - base_notch_dt
        print 'difference between notch_dt and base_notch_dt %.8f' % (dt)
        self.m1.set_power(self.m1.power + dt*1*self.m1.k)

        # m1.set_power(m1.power + (notch_dt-base_notch_dt)*10*m1.k)
