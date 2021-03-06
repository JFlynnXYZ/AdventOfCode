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
    return (len([r for r in inp if len(r.split()) == len(set(r.split()))]))


def solve2(inp):
    num_valids = 0
    for r in inp:
        if len(r.split()) == len(set(r.split())):
            word_sets = [set(x) for x in r.split()]
            for w in word_sets:
                if len([w for s in word_sets if w == s]) >= 2:
                    break
            else:
                num_valids += 1
    return num_valids


def solution():
    return solve1(DAY_INPUT), solve2(DAY_INPUT)


########################################################################################################################
### Output #############################################################################################################
########################################################################################################################


def main():
    print prettyInfo(DAY_DESC, DAY_INPUT_STR)
    print prettyAnswers(*solution())


if __name__ == "__main__":
    main()
