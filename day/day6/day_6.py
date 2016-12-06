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

from collections import Counter
from operator import itemgetter as _itemgetter
import heapq as _heapq

class ImprovedCounter(Counter):

    def least_common(self, n=None):
        '''List the n least common elements and their counts from the least
        common to the most.  If n is None, then list all element counts.

        >>> ImprovedCounter('abcdeabcdabcaba').least_common(3)
        [('e', 1), ('d', 2), ('c', 3)]

        '''
        if n is None:
            return sorted(self.iteritems(), key=_itemgetter(1))
        return _heapq.nsmallest(n, self.iteritems(), key=_itemgetter(1))


def solution():
    sol1 = ''.join([Counter(x).most_common(1)[0][0] for x in zip(*DAY_INPUT)])
    sol2 = ''.join([ImprovedCounter(x).least_common(1)[0][0] for x in zip(*DAY_INPUT)])
    return sol1, sol2


########################################################################################################################
### Output #############################################################################################################
########################################################################################################################


def main():
    print prettyInfo(DAY_DESC, DAY_INPUT_STR)
    print prettyAnswers(*solution())


if __name__ == "__main__":
    main()
