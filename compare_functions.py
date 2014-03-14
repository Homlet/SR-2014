from math import atan2, hypot, pi

class Shell:
    def __init__(self, x, y, theta):
        self.x = x
        self.y = y
        self.theta = theta

def f1(robot, x, y):
    """
    Returns angle to turn and the distance to move.
    """
    dx = x - robot.x
    dy = y - robot.y
    alpha = atan2(dx, -dy)
    # alpha is bearing robot needs to have to look at the point
    theta = robot.theta
    if alpha < 0:
        alpha += pi+pi
    beta = alpha - theta
    # beta is angle for robot to turn clock-wise
    if beta < -pi:
        beta += pi+pi
    if beta > pi:
        beta -= pi+pi
    
    return hypot(dx, dy), beta

def f2(robot, x, y):
    """
    Returns angle to turn and the distance to move.
    """
    dx = x - robot.x
    dy = y - robot.y
    alpha = atan2(dx, -dy)
    theta = robot.theta
    gamma = alpha - theta
    if abs(gamma) > pi:
        gamma -= 2*pi
    
    return hypot(dx, dy), gamma

def use_functions_for(func, x, y, robot):
    for f in func:
        print(f(robot, x, y))
def main():
    robotX = 4
    robotY = 4
    robotTheta = 3/2*pi

    x = 5
    y = 1
    robot = Shell(robotX, robotY, robotTheta)
    functions = [f1, f2]
    use_functions_for(functions, x, y, robot)

main()