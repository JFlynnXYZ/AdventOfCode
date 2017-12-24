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


def solve1(inp):
    return sum(int(inp[i]) for i in range(len(inp))
               if inp[i] == inp[(i+1) % len(inp)])


def solve2(inp):
    return sum(int(inp[i]) for i in range(len(inp))
               if inp[i] == inp[(i + len(inp) / 2) % len(inp)])


def solution():
    return solve1(DAY_INPUT_STR), solve2(DAY_INPUT_STR)


########################################################################################################################
### Output #############################################################################################################
########################################################################################################################


def main():
    print prettyInfo(DAY_DESC, DAY_INPUT_STR)
    print prettyAnswers(*solution())


if __name__ == "__main__":
    main()
