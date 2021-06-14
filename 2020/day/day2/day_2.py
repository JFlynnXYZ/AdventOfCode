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

import collections
import sys
import re

regex = re.compile(r"(?P<min>\d+)\-(?P<max>\d+) (?P<char>\w)\: ("
                   r"?P<pass>\w*)")

def solve1(inp):
    valid_count = 0
    for l in inp:
        match = regex.match(l)
        if not match:
            sys.stderr.write("WHY NO MATCH!\n")
            sys.exit(1)

        count = collections.Counter(match.group("pass"))
        pass_char = match.group("char")
        min_occ, max_occ = int(match.group("min")), int(match.group("max"))
        valid_count += pass_char in count and count[pass_char] >= min_occ \
                       and count[pass_char] <= max_occ
    return valid_count


def solve2(inp):
    valid_count = 0
    for l in inp:
        match = regex.match(l)
        if not match:
            sys.stderr.write("WHY NO MATCH!\n")
            sys.exit(1)

        passwd = match.group("pass")
        pass_char = match.group("char")
        min_idx, max_idx = int(match.group("min"))-1, int(match.group("max"))-1
        min_match = passwd[min_idx] == pass_char
        max_match = passwd[max_idx] == pass_char
        valid_count += (min_match ^ max_match)  # XOR

    return valid_count


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
