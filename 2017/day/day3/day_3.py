########################################################################################################################
### Advent Setup #######################################################################################################
########################################################################################################################

import os
from AdventBuilder import setupDayVariables, prettyInfo, prettyAnswers

__dir__ = os.path.dirname(__file__)
DAY_NUM, DAY_DESC, DAY_INPUT, DAY_INPUT_STR = setupDayVariables(__dir__)

########################################################################################################################
#### My Solution #######################################################################################################
########################################################################################################################

import math
import itertools


def spiral(val):
    val = val-1
    x = y = dx = 0
    dy = -1
    yield x,y
    for i in range(val):
        if x == y or (x < 0 and x == -y) or (x > 0 and x == 1-y):
            dx, dy = -dy, dx
        x, y = x+dx, y+dy
        yield x,y


def taxicab_distance(end, start=(0, 0)):
    return abs(start[0] - end[0]) + abs(start[1] - end[1])


def adj_sqrs(coord):
    return [(coord[0] + i, coord[1] + j)
            for i in (-1, 0, 1)
            for j in (-1, 0, 1)
            if i != 0 or j != 0]


def solve1(inp):
    return taxicab_distance(list(spiral(inp))[-1])


def solve2(inp):
    grid = {}
    for i,coord in enumerate(spiral(inp)):
        val = 0
        if coord == (0,0):
            grid[coord] = 1
            continue

        for adj in adj_sqrs(coord):
            try:
                val += grid[adj]
            except KeyError:
                pass
        if val > inp:
            return val

        grid[coord] = val


def solution():
    val = int(DAY_INPUT_STR)
    return solve1(val), solve2(val)


########################################################################################################################
### Output #############################################################################################################
########################################################################################################################


def main():
    print prettyInfo(DAY_DESC, DAY_INPUT_STR)
    print prettyAnswers(*solution())


if __name__ == "__main__":
    main()
