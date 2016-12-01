import os
from AdventBuilder import prettyInfo

__dir__ = os.path.dirname(__file__)
DAY_NUM = int(os.path.basename(__dir__))
DAY_DESC = ''.join(open("desc_{}.txt".format(DAY_NUM)).readlines())
DAY_INPUT = ''.join(open("input_{}.txt".format(DAY_NUM)).readlines()).strip("\n")


def main():
    print prettyInfo(DAY_DESC, DAY_INPUT)


if __name__ == "__main__":
    main()
