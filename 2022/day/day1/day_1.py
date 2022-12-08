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

import itertools

def solve1(inp):
    grouper = itertools.groupby(inp, key=lambda x: x == "")
    res = max(sum(int(x) for x in j) for i, j in grouper if not i)
    return res


def solve2(inp):
    grouper = itertools.groupby(inp, key=lambda x: x == "")
    res = sorted((sum(int(x) for x in j) for i, j in grouper if not i), reverse=True)

    return sum(res[:3])


def solution():
    return solve1(DAY_INPUT), solve2(DAY_INPUT)


########################################################################################################################
### Output #############################################################################################################
########################################################################################################################


def main():
    print(prettyInfo(DAY_DESC, DAY_INPUT_STR))
    print(prettyAnswers(*solution()))


if __name__ == "__main__":
    main()
