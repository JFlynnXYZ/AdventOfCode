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

import re
import string

def checkAbba(seq):
    return any(seq[i] != seq[i+1] and seq[i:i+2] == seq[i+2:i+4][::-1] for i in range(len(seq)-2))

def findAllAba(hyper):
    return [hyper[i:i+3] for i in range(len(hyper)-2) if hyper[i] != hyper[i+1] and hyper[i] == hyper[i+2]]

def abaToBab(aba):
    return aba.translate(string.maketrans(aba[:2], aba[1::-1]))

def solution():
    splitInp = [re.split('\[|\]', l) for l in DAY_INPUT]
    superHyper = [(spi[::2], spi[1::2]) for spi in splitInp]
    sol1 = sol2 = 0

    for supe, hyp in superHyper:
        # Solution 1
        if not any(checkAbba(hn) for hn in hyp) and \
                any(checkAbba(sup) for sup in supe):
            sol1 += 1

        # Solution 2
        allSuperAba = [s for sl in [findAllAba(sup) for sup in supe] for s in sl]
        allHyperBab = [s for sl in [[abaToBab(h) for h in findAllAba(hyp)] for hyp in hyp] for s in sl]

        if any(True if s in allHyperBab else False for s in allSuperAba):
            sol2 += 1

    return sol1, sol2


########################################################################################################################
### Output #############################################################################################################
########################################################################################################################


def main():
    print prettyInfo(DAY_DESC, DAY_INPUT_STR)
    print prettyAnswers(*solution())


if __name__ == "__main__":
    main()
