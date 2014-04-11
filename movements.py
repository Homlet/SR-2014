from mechanics import (init_arms_pins, close_arms, lower_arms, extend_arms,
    retract_arms, open_arms, raise_arms, Journey)


def move_straight(robot, dist):
    """
    Moves the robot dist metres forward and updates the tracker.
    """
    journey = Journey(robot, distance=dist)
    journey.start()
    robot.position.move(dist)


def turn(robot, alpha=0.524):  # 0.524 rad = 30 degrees
    """
    Turns the robot alpha RADIANS and updates the tracker.
    """
    journey = Journey(robot, angle=alpha)
    journey.start()
    robot.position.turn(alpha)


def prepare_grab(robot):
    init_arms_pins(robot)
    close_arms(robot)
    lower_arms(robot)
    extend_arms(robot)
    open_arms(robot)


def grab(robot):
    init_arms_pins(robot)
    close_arms(robot)
    raise_arms(robot)
    retract_arms(robot)


def put_down(robot):
    pass
