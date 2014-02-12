from math import sin, cos, atan, radians, degrees, sqrt, pi
from time import sleep

from sr import Robot

from movements import move_straight, turn
from position import compute_directions_for

res = (1280, 720)


def line_up_to(marker, robot):
    dist, angle1, angle2 = compute_directions_for(marker)
    print 'dist=%.2f, angle1=%.2f, angle2=%.2f' % (dist, angle1, angle2)
    turn(robot, angle1)
    sleep(1)
    move_straight(robot, dist)
    sleep(1)
    turn(robot, angle2)
    
def main():
    world_exists = True
    robot = Robot()
    turn(robot, pi)
    return

    markers = robot.see(res=res)
    while world_exists:
        markers = robot.see(res=res)
        while not markers:
            turn(robot)
            sleep(0.5)
            markers = robot.see(res=res)
        line_up_to(markers[0], robot)
        while robot.see(res=res):
            pass
        sleep(5)

main()
