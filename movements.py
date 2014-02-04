from time import sleep
from math import copysign

def move_straight(robot, distance):
    """
    May need to consider creating a function to move forwards carefully
    i.e while moving, trying to see if robot is getting to a point where
    it's supposed to be getting. Adjust if neccesary.
    """

    power = copysign(50, distance)
    t = distance / (power/50)
    robot.motors[0].m0.power = power
    robot.motors[0].m1.power = power
    sleep(abs(t))
    stop_motors(robot)

def turn(robot, angle=0.524):
    """
    0.524 rad = 30 degrees
    """
    power = copysign(45, angle)
    t = 0.3 * (angle/0.524)
    robot.motors[0].m0.power = -power
    robot.motors[0].m1.power =  power
    sleep(abs(t))
    stop_motors(robot)

def stop_motors(robot):
    robot.motors[0].m0.power = 0
    robot.motors[0].m1.power = 0
