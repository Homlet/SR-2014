def log(robot, s):
    """Prints message with indentation based on stack."""
    print str("| " * robot.log_level) + s


def reset_log(robot):
    """Resets the log level of the robot."""
    robot.log_level = 0


def push_log(robot, levels=1):
    """Increases indentation level for output."""
    robot.log_level += levels


def pop_log(robot, levels=1):
    """Decreases indentation level for output."""
    robot.log_level -= levels
    if robot.log_level < 0:
        robot.log_level = 0


def indented(func):
    """Decorator to automatically indent a function."""
    def new(robot, *args, **kwargs):
        try:
            push_log(robot)
            out = func(robot, *args, **kwargs)
            pop_log(robot)
            return out
        except:
            if 'out' in locals(): return out
            else: return func(robot, *args, **kwargs)
    return new
