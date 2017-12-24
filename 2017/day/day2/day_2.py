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
    res = 0
    for r in inp:
        vals = [int(x) for x in r.split("\t")]
        res += max(vals)-min(vals)
    return res


def solve2(inp):
    res = 0
    for r in inp:
        vals = [int(x) for x in r.split("\t")]
        found = False
        for i in xrange(len(vals)):
            if found:
                break
            c = vals[i]
            for j in (x for x in range(len(vals)) if x != i):
                t = vals[j]
                if not c % t:
                    res += c / t
                    found = True
                    break
                elif not c % t:
                    res += c / t
                    found = True
                    break
    return res



def solution():
#     DAY_INPUT_STR = """5\t9\t2\t8
# 9\t4\t7\t3
# 3\t8\t6\t5"""
#     DAY_INPUT = DAY_INPUT_STR.split("\n")
    return solve1(DAY_INPUT), solve2(DAY_INPUT)


########################################################################################################################
### Output #############################################################################################################
########################################################################################################################


def main():
    print prettyInfo(DAY_DESC, DAY_INPUT_STR)
    print prettyAnswers(*solution())


if __name__ == "__main__":
    main()
