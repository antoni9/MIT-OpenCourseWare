# Problem Set 11: Simulating robots
# Name:
# Collaborators:
# Time:

import math
import random
import pylab

# === Provided classes

class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).

        x: a real number indicating the x-coordinate
        y: a real number indicating the y-coordinate
        """
        self.x = x
        self.y = y
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: integer representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)


# === Problems 1 and 2

class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.
        Initially, no tiles in the room have been cleaned.

        width: an integer > 0
        height: an integer > 0
        """
        # TODO: Your code goes here
        self.width = width
        self.height = height
        self.tiles = {}
        for width in range(0, self.width+1):
            for height in range(0, self.height+1):
                self.tiles[(width, height)] = 1
        self.numberOfTiles = len(self.tiles.keys()) - self.width - self.height - 1
        self.cleanTiles = 0

    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.
        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """
        # TODO: Your code goes here
        self.tiles[(int(pos.getX()), int(pos.getY()))] = 0
        self.cleanTiles += 1

    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        # TODO: Your code goes here
        if self.tiles[(int(m), int(n))] != 1:
            return True
        else: return False

    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        # TODO: Your code goes here
        return self.numberOfTiles

    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """
        # TODO: Your code goes here
        return self.cleanTiles


    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """
        # TODO: Your code goes here
        pos = Position(random.randrange(0, self.width), random.randrange(0, self.height))
        return pos

    def isPositionInRoom(self, pos):
        """
        Return True if POS is inside the room.

        pos: a Position object.
        returns: True if POS is in the room, False otherwise.
        """
        # TODO: Your code goes here
        if pos.getX() < 0 or pos.getX() > self.width:
            return False
        elif pos.getY() < 0 or pos.getY() > self.height:
            return False
        else: return True

class BaseRobot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in
    the room.  The robot also has a fixed speed.

    Subclasses of BaseRobot should provide movement strategies by
    implementing updatePositionAndClean(), which simulates a single
    time-step.
    """
    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified
        room. The robot initially has a random direction d and a
        random position p in the room.

        The direction d is an integer satisfying 0 <= d < 360; it
        specifies an angle in degrees.

        p is a Position object giving the robot's position.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        # TODO: Your code goes here
        self.p = room.getRandomPosition()
        self.d = random.randint(0, 359)
        self.s = speed

    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        # TODO: Your code goes here
        return self.p

    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        # TODO: Your code goes here
        return self.d

    def getRobotSpeed(self):
        """
        Returns robot speed.
        :return: robot speed as an int
        """
        return self.s

    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        # TODO: Your code goes here
        self.p = position

    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        # TODO: Your code goes here
        self.d = direction



class Robot(BaseRobot):
    """
    A Robot is a BaseRobot with the standard movement strategy.

    At each time-step, a Robot attempts to move in its current
    direction; when it hits a wall, it chooses a new direction
    randomly.
    """
    def updatePositionAndClean(self, room):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        # TODO: Your code goes here
        if not room.isTileCleaned(self.p.getX(), self.p.getY()):
            room.cleanTileAtPosition(self.p)
        while not room.isPositionInRoom(self.p.getNewPosition(self.getRobotDirection(), self.getRobotSpeed())):
            self.setRobotDirection(random.randint(0, 359))
        self.setRobotPosition(self.p.getNewPosition(self.getRobotDirection(), self.getRobotSpeed()))
        # print(self.getRobotPosition().getX(), self.getRobotPosition().getY(), self.getRobotDirection())
        if not room.isTileCleaned(self.p.getX(), self.p.getY()):
            room.cleanTileAtPosition(self.p)

# === Problem 3

def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type, visualize=False):
    """
    Runs NUM_TRIALS trials of the simulation and returns a list of
    lists, one per trial. The list for a trial has an element for each
    timestep of that trial, the value of which is the percentage of
    the room that is clean after that timestep. Each trial stops when
    MIN_COVERAGE of the room is clean.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE,
    each with speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    Visualization is turned on when boolean VISUALIZE is set to True.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. Robot or
                RandomWalkRobot)
    visualize: a boolean (True to turn on visualization)
    """
    # TODO: Your code goes here
    res = []
    for trial in range(num_trials):
        trialRes = []
        room = RectangularRoom(width, height)
        robots = [robot_type(room, speed) for robot in range(num_robots)]
        while ((room.getNumCleanedTiles() / room.getNumTiles()) * 100) < min_coverage:
            for robot in robots:
                robot.updatePositionAndClean(room)
                if ((room.getNumCleanedTiles() / room.getNumTiles()) * 100) >= min_coverage:
                    break
            trialRes.append((room.getNumCleanedTiles() / room.getNumTiles()) * 100)
        res.append(trialRes)
    return res


# === Provided function
def computeMeans(list_of_lists):
    """
    Returns a list as long as the longest list in LIST_OF_LISTS, where
    the value at index i is the average of the values at index i in
    all of LIST_OF_LISTS' lists.

    Lists shorter than the longest list are padded with their final
    value to be the same length.
    """
    # Find length of longest list
    longest = 0
    for lst in list_of_lists:
        if len(lst) > longest:
           longest = len(lst)
    # Get totals
    tots = [0]*(longest)
    for lst in list_of_lists:
        for i in range(longest):
            if i < len(lst):
                tots[i] += lst[i]
            else:
                tots[i] += lst[-1]
    # Convert tots to an array to make averaging across each index easier
    tots = pylab.array(tots)
    # Compute means
    means = tots/float(len(list_of_lists))
    return means

# x = computeMeans(runSimulation(1, 1.0, 10, 10, 90, 10, Robot))
# print(len(x))

# === Problem 4
def averages(listOfLists):
    averages = []
    for a in listOfLists:
        averages.append(len(a))
    return averages

def showPlot1(robot):
    """
    Produces a plot showing dependence of cleaning time on room size.
    """
    # TODO: Your code goes here
    res = []
    h = 5
    sizes = []
    for i in range(0, 10):
        sizes.append(h)
        res.append(computeMeans(runSimulation(1, 1.0, h, h, 75, 10, robot)))
        h += 5

    average = averages(res)

    pylab.plot(sizes, average, label=str(robot.__name__))
    pylab.title('dependence of cleaning time on room size')
    pylab.ylabel('time steps')
    pylab.xlabel('size of room')
    pylab.legend(loc='upper left')

# showPlot1(Robot)
# pylab.show()

def showPlot2(robot):
    """
    Produces a plot showing dependence of cleaning time on number of robots.
    """
    # TODO: Your code goes here
    colours = ['r', 'g', 'b', 'c']
    numTrials = 10
    for trials in range(0, 4):      # Dont' run this, computes way too many trials
        res = []
        h = 1
        robots = []
        for i in range(0, 10):
            robots.append(h)
            res.append(computeMeans(runSimulation(h, 1.0, 25, 25, 75, numTrials, robot)))
            h += 1

        average = averages(res)
        pylab.plot(robots, average, str(colours[0]), label='%d num trials, %s'%(numTrials, robot.__name__))

        # numTrials *= 2
        colours.pop(0)

    pylab.legend(loc='upper right')
    pylab.title('dependence of cleaning time on number of robots')
    pylab.ylabel('time steps')
    pylab.xlabel('number of robots')

# showPlot2(Robot)
# pylab.show()

def showPlot3(robot):
    """
    Produces a plot showing dependence of cleaning time on room shape.
    """
    # TODO: Your code goes here
    res = []
    roomSizes = [(20, 20), (25, 16), (40, 10), (50, 8), (80, 5), (100, 4)]
    ratios = []
    for i in roomSizes:
        res.append(computeMeans(runSimulation(2, 1.0, i[0], i[1], 75, 100, robot)))
        ratios.append(i[0] / i[1])
    average = averages(res)

    pylab.plot(ratios, average)
    pylab.title('dependence of cleaning time on room shape')
    pylab.ylabel('time steps')
    pylab.xlabel('ratio of room sides')

# showPlot3(Robot)
# pylab.show()

def showPlot4(robot):
    """
    Produces a plot showing cleaning time vs. percentage cleaned, for
    each of 1-5 robots.
    """
    # TODO: Your code goes here

    perc = range(1, 100, 20)     # don't run, takes a long time
    for i in range(1, 6):
        res = []
        for per in perc:
            res.append(computeMeans(runSimulation(i, 1.0, 25, 25, per, 30, robot)))
        average = averages(res)
        x = None
        if robot.__name__ == 'RandomWalkRobot':
            x = 'r'
        else: x = 'b'
        pylab.plot(perc, average, '%s'%(x), label='num robots = %d, robot name %s' % (i, robot.__name__))
        pylab.xlabel('percentage of room clean')
        pylab.ylabel('time steps')
        pylab.legend(loc='upper left')

# showPlot4(Robot)
# pylab.show()

# === Problem 5

class RandomWalkRobot(BaseRobot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement
    strategy: it chooses a new direction at random after each
    time-step.
    """
    # TODO: Your code goes here
    def updatePositionAndClean(self, room):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        # TODO: Your code goes here
        if not room.isTileCleaned(self.p.getX(), self.p.getY()):
            room.cleanTileAtPosition(self.p)
        while True:
            self.setRobotDirection(random.randint(0, 359))
            while not room.isPositionInRoom(self.p.getNewPosition(self.getRobotDirection(), self.getRobotSpeed())):
                self.setRobotDirection(random.randint(0, 359))
            break
        self.setRobotPosition(self.p.getNewPosition(self.getRobotDirection(), self.getRobotSpeed()))
        if not room.isTileCleaned(self.p.getX(), self.p.getY()):
            room.cleanTileAtPosition(self.p)

# === Problem 6

def showPlot5():
    """
    Produces a plot comparing the two robot strategies.
    """
    # TODO: Your code goes here
    robots = (RandomWalkRobot, Robot)

    for robot in robots:
        # showPlot1(robot)    # RandomWalkRobot time increases exponentially as room size increases, while Robot time
        #                     # is closer to linear time.
        # showPlot2(robot)    # RandomWalkRobot time decreases exponentially as numRobots increases, but is not as good
        #                     # as Robot.
        # showPlot3(Robot)    # RandomWalkRobot time increases exponentially as room ratio increases, while Robot time
        #                     # is linear.
        # showPlot4(robot)    # 3,4,5 RandomWalkRobots take roughly the same time as 1 Robot to clean the same area
    pylab.show()

showPlot5()