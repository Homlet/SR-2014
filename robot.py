# from time import sleep

# from sr import Robot

# from movements import Tracker
# from strategy import line_up_to_marker, scan_corner, move_till_touch


# def main():
#     robot.position = Tracker(robot.zone)
#     p = robot.position
#     print 'Start\n    x = %.1f y = %.1f theta = %.1f' % (p.x, p.y, p.theta)
#     # print '   ', (robot.position.x, robot.position.y), robot.position.angle
    
#     # Main strategy goes here:
#     marker = scan_corner(robot, robot.zone)
#     line_up_to_marker(robot, marker)
#     move_till_touch(robot)
    
#     p = robot.position
#     print 'End\n    x = %.1f y = %.1f theta = %.1f' % (p.x, p.y, p.theta)
#     # print '   ', (robot.position.x, robot.position.y), robot.position.angle

# robot = Robot()

# world_exists = True
# while world_exists:
#     main()
#     sleep(5)

from sr import Robot

def main():
    robot = Robot()
    robot.motors[0].m0.power = 50
    robot.motors[0].m1.power = 50

main()
