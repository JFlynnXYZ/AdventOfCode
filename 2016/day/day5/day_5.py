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

from hashlib import md5
from itertools import takewhile

def solution():
    salt = DAY_INPUT[0].strip("\n")
    result = []
    count = 0
    find = "00000"
    while len(result) < 8 and False:
        hash = md5(salt + str(count)).hexdigest()
        if hash.startswith(find):
            print hash
            result.append(hash[5])
        count += 1

    count = 0
    result2 = [None]*8
    while any(r is None for r in result2):
        hash = md5(salt + str(count)).hexdigest()
        if hash.startswith(find):
            if hash[5].isdigit():
                ind = int(hash[5])
                if ind < 8 and result2[ind] is None:
                    result2[ind] = hash[6]
        count += 1

    return ''.join(result), ''.join(result2)


########################################################################################################################
### Output #############################################################################################################
########################################################################################################################


def main():
    print prettyInfo(DAY_DESC, DAY_INPUT_STR)
    print prettyAnswers(*solution())


if __name__ == "__main__":
    main()
