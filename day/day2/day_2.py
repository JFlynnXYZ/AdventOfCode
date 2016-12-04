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

KEYPAD = [["1", "2", "3"],
          ["4", "5", "6"],
          ["7", "8", "9"]]

KEYPAD_ACTUAL = [["1"],
              ["2", "3", "4"],
           ["5", "6", "7", "8", "9"],
           ["A", "B", "C"],
                ["D"]]


class Keypad(object):

    def __init__(self, rowGrid=None):
        self.keypadRow = []
        self.keypadCol = []
        self.numRows = 0
        self.numCols = 0

        if rowGrid is not None:
            self.addGridRows(rowGrid)

    def __repr__(self):
        repr = "< Keypad:\n"
        for r in self.keypadRow:
            rLen = len(r)
            repr += "\t"*int(((self.numRows-rLen)*0.5))
            finalR = rLen - 1
            for i, v in enumerate(r):
                repr += str(v)
                if i != finalR:
                    repr += ",\t"
            repr += "\n"
        repr += " >"
        return repr

    def getRowItem(self, row, col):
        return self.keypadRow[col][row]

    def getColItem(self, col, row):
        return self.keypadCol[row][col]

    def getRow(self, row):
        return self.keypadRow[row][:]

    def getCol(self, col):
        return self.keypadCol[col][:]

    def getRowLen(self, row):
        return len(self.getRow(row))

    def getColLen(self, col):
        return len(self.getCol(col))

    def findLocation(self, val):
        for i, r in enumerate(self.keypadRow):
            for j, v in enumerate(r):
                if v == val:
                    return j, i
        else:
            return None

    def __getitem__(self, key):
        if type(key) == tuple:
            if len(key) == 2:
                return self.getRowItem(*key)
            elif len(key) == 1:
                return self.getRow(key)
            else:
                raise ValueError("Don't understand key")

    def addRow(self, row):
        self.keypadRow.append(self.paddRow(row, max(len(row), self.numCols)))
        self.numRows = len(self.keypadRow)
        newColLen = max(len(x) for x in self.keypadRow)
        if self.numCols != newColLen:
            self.numCols = newColLen
            self.calculateRows()

        self.calculateColumns()

    def addGridRows(self, rows):
        for r in rows:
            self.addRow(r)

    def calculateRows(self):
        for i, row in enumerate(self.keypadRow):
            self.keypadRow[i] = self.paddRow(row, self.numCols)

    def paddRow(self, row, cols=1):
        newRow = []
        rLen = len(row)
        cVals = [(cols - rLen) / 2 + rId for rId in range(rLen)]
        count = 0
        for j in range(cols):
            if j in cVals:
                newRow.append(row[count])
                count += 1
            else:
                newRow.append(None)
        return newRow

    def calculateColumns(self):
        self.keypadCol = [[] for _ in range(self.numCols)]
        for row in self.keypadRow:
            rLen = len(row)
            for i,v in enumerate(row):
                self.keypadCol[i].append(v)


class Player(object):

    def __init__(self, keypad=None):
        self.location = (1, 1)
        self.code = ""
        self.keypad = keypad

        if keypad is not None:
            self.location = list(self.keypad.findLocation("5"))

    def canMove(self, x, y):
        return self.keypad[x, y] is not None

    def move(self, char):
        newLocation = self.location[:]
        if char == "U":
            newLocation[1] = max(self.location[1] - 1, 0)
        elif char == "D":
            newLocation[1] = min(self.location[1] + 1, self.keypad.numRows-1)
        elif char == "L":
            newLocation[0] = max(self.location[0] - 1, 0)
        elif char == "R":
            newLocation[0] = min(self.location[0] + 1, self.keypad.numCols-1)

        if self.canMove(*newLocation):
            self.location = newLocation

    def parseCommands(self, lines):
        for l in lines:
            for char in l:
                self.move(char)
            self.code += str(self.keypad[self.location[0], self.location[1]])

    def setKeypad(self, keypad):
        self.keypad = keypad

    def getCode(self):
        return self.code

    def reset(self):
        self.code = ""
        self.location = list(self.keypad.findLocation("5"))


def solution():
    keypad = Keypad(KEYPAD)
    keypadActual = Keypad(KEYPAD_ACTUAL)
    player = Player(keypad)
    player.parseCommands(DAY_INPUT)
    code1 = player.getCode()

    player.setKeypad(keypadActual)
    player.reset()
    player.parseCommands(DAY_INPUT)
    code2 = player.getCode()
    return code1, code2


########################################################################################################################
### Output #############################################################################################################
########################################################################################################################

def main():
    print prettyInfo(DAY_DESC, DAY_INPUT_STR)
    print prettyAnswers(*solution())


if __name__ == "__main__":
    main()
