def log(robot, s):
    """Prints message with indentation based on stack."""
    print ("| " * robot.log_level) + s


def reset_log(robot):
    """Resets the log level of the robot."""
    robot.log_level = 0


def push_log(robot, repeat=1):
    """Increases indentation level for output."""
    for i in range(repeat):
        robot.log_level += 1


def pop_log(robot, repeat=1):
    """Decreases indentation level for output."""
    for i in range(repeat):
        if robot.log_level > 0:
            robot.log_level -= 1
