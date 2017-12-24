########################################################################################################################
### Advent Setup #######################################################################################################
########################################################################################################################

import os
from AdventBuilder import setupDayVariables, prettyInfo, prettyAnswers

__dir__ = os.path.dirname(__file__)
DAY_NUM, DAY_DESC, DAY_INPUT = setupDayVariables(__dir__)

########################################################################################################################
#### My Solution #######################################################################################################
########################################################################################################################


def taxiCabDistance(start, end):
    return abs(start[0] - end[0]) + abs(start[1] - end[1])


class Direction(object):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3
    TOTAL = 4


class Rotate(object):
    RIGHT = 1
    LEFT = -1
    TOTAL = 2


class Player(object):
    def __init__(self, commands=None):
        self.facing = Direction.NORTH
        self.location = [0, 0]
        self.previousLocations = [self.location[:]]
        self.visitedTwice = False
        self.firstLocationVisitedTwice = None

        if commands is not None:
            self.parseCommands(commands)

    def distanceFromFirstLocationVisitedTwice(self):
        return taxiCabDistance([0, 0], self.firstLocationVisitedTwice)

    def distanceFromLocation(self, location):
        return taxiCabDistance(self.location, location)

    def distanceFromStartLocation(self):
        return self.distanceFromLocation([0, 0])

    def rotate(self, rot):
        self.facing += rot
        if self.facing >= Direction.TOTAL:
            self.facing -= Direction.TOTAL
        elif self.facing < Direction.NORTH:
            self.facing += Direction.TOTAL

    def move(self, mv):
        for i in range(mv):
            if self.facing == Direction.NORTH:
                self.location[1] += 1
            elif self.facing == Direction.EAST:
                self.location[0] += 1
            elif self.facing == Direction.SOUTH:
                self.location[1] -= 1
            elif self.facing == Direction.WEST:
                self.location[0] -= 1

            self.checkIfAlreadyVisited(self.location)

    def checkIfAlreadyVisited(self, location):
        if self.location in self.previousLocations and not self.visitedTwice:
            self.visitedTwice = True
            self.firstLocationVisitedTwice = location[:]
        self.previousLocations.append(location[:])

    def command(self, strCmd):
        rot = Rotate.RIGHT if strCmd[0] == "R" else Rotate.LEFT
        mv = int(strCmd[1:])
        self.rotate(rot)
        self.move(mv)

    def parseCommands(self, strCmds):
        strCmdLs = strCmds.split(", ")
        for strCmd in strCmdLs:
            self.command(strCmd)


def solution():
    player = Player(DAY_INPUT)
    return player.distanceFromStartLocation(), player.distanceFromFirstLocationVisitedTwice()


########################################################################################################################
### Output #############################################################################################################
########################################################################################################################


def main():
    print prettyInfo(DAY_DESC, DAY_INPUT)
    print prettyAnswers(*solution())


if __name__ == "__main__":
    main()
