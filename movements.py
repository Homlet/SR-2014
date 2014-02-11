from mechanics import Journey

def move_straight(robot, dist):
    journey = Journey(robot, distance=dist)
    journey.start()

def turn(robot, alpha=0.524):  # 0.524 rad = 30 degrees
    journey = Journey(robot, angle=alpha)
    journey.start()