def log(robot, s):
    """Prints message with indentation based on stack."""
#    if not hasattr(robot, "log_level"):
#        robot.log_level = 0
    print ("  " * robot.log_level) + s


def push_log(robot, repeat=1):
    """Increases indentation level for output."""
    for i in range(repeat):
        if hasattr(robot, "log_level"):
            if robot.log_level > 0:
                robot.log_level += 1
        else:
            robot.log_level = 1


def pop_log(robot, repeat=1):
    """Decreases indentation level for output."""
    for i in range(repeat):
        if hasattr(robot, "log_level"):
            if robot.log_level > 0:
                robot.log_level -= 1
        else:
            robot.log_level = 0
