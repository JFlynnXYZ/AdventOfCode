import os

__dir__ = os.path.dirname(__file__)
DAY_NUM = int(os.path.basename(__dir__))
DAY_INPUT = '\n'.join(open("input_{}.txt".format(DAY_NUM)).readlines())


def main():
    print DAY_INPUT


if __name__ == "__main__":
    main()
