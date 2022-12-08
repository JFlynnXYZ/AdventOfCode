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


def score(item):
    if item.islower():
        start = ord('a')
        mod = 1
    else:
        start = ord('A')
        mod = 27
    return (ord(item) - start) + mod


def solve1(inp):
    priority = 0
    for i in inp:
        half = int(len(i)/2)
        comp1, comp2 = set(i[:half]), set(i[half:])
        intersect = comp1.intersection(comp2)
        priority += score(intersect.pop())
    return priority


def solve2(inp):
    priority = 0
    for i in zip(*(iter(inp),) * 3):
        running_set = set(i[0])
        for b in i[1:]:
            running_set.intersection_update(b)
        priority += score(running_set.pop())

    return priority


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
