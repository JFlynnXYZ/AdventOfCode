########################################################################################################################
### Advent Setup #######################################################################################################
########################################################################################################################
import math
import os
from AdventBuilder import setupDayVariables, prettyInfo, prettyAnswers

__dir__ = os.path.dirname(__file__)
DAY_NUM, DAY_DESC, DAY_INPUT, DAY_INPUT_STR = setupDayVariables(__dir__)

########################################################################################################################
#### My Solution #######################################################################################################
########################################################################################################################


R = 0b001
P = 0b010
S = 0b100
s = {0: 'Rock', 1: 'Paper', 2: 'Scissor'}
sb = {R: 'Rock', P: 'Paper', S: 'Scissor'}


def solve1(inp):
    total_score = 0
    for their_hand, my_hand in (i.split(" ") for i in inp):
        th = ord(their_hand) - ord('A')
        mh = ord(my_hand) - ord('X')
        total_score += (mh+1)
        #print(f"{s[mh]} vs {s[th]}==", end="")
        if mh == th:
            #print("Draw")
            total_score += 3
        else:
            mhb = (1 << mh)
            thb = (1 << th)
            shift = (thb << 1)
            if shift > 0b100:
                shift = shift > 3
            win = mhb & shift
            if win:
                #print("Win")
                total_score += 6
            else:
                #print("Loss")
                pass

    return total_score


def solve2(inp):
    total_score = 0
    for their_hand, result in (i.split(" ") for i in inp):
        th = ord(their_hand) - ord('A')
        res = ord(result) - ord('X')
        shift = (1-res)
        thb = (1 << th)
        mhb = thb

        if shift < 0:
            mhb = mhb << abs(shift)
            if mhb > 0b100:
                mhb = mhb > 3
        elif shift > 0:
            mhb = mhb >> abs(shift)
            if mhb == 0b000:
                mhb = 0b100

        mh = int(math.log2(mhb & -mhb))  # Get the first rightmost bit set
        total_score += mh + 1
        total_score += res * 3
        print(f"{sb[thb]} vs {sb[mhb]}=={('Loss', 'Draw', 'Win')[res]}", end="\n")

    return total_score


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
