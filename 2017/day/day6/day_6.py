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


from itertools import cycle


def solve1(inp):
    results = []
    while inp not in results:
        results.append(inp[:])
        max_value = max(inp)
        max_idx = inp.index(max_value)
        inp[max_idx] = 0
        for i in (x % len(inp) for x in range(max_idx+1,
                                              max_idx + 1 + max_value)):
            inp[i] += 1

    return len(results)


def solve2(inp):
    return solve1(inp)


def solution():
    inp = [int(x) for x in DAY_INPUT_STR.split()]
    # Reusing the same memory from the list, so inp contains the final
    # value that starts the infinite loop. Just pass it through again
    # to find how long the loop is.
    return solve1(inp), solve2(inp)


########################################################################################################################
### Output #############################################################################################################
########################################################################################################################


def main():
    print prettyInfo(DAY_DESC, DAY_INPUT_STR)
    print prettyAnswers(*solution())


if __name__ == "__main__":
    main()
