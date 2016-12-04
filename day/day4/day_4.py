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
import itertools
from collections import deque
import string
import enchant
ROOM_REGEX = re.compile(r"^(?P<roomName>[a-z-]+)-(?P<sectorID>[\d]{3})\[(?P<checksum>\w+)]$")


def cipher(n):
    az = string.ascii_lowercase
    x = n % len(az)
    return string.maketrans(az, az[x:] + az[:x])


def solution():
    matches = [ROOM_REGEX.match(l) for l in DAY_INPUT]
    keyFunc = lambda char: char[1]
    actualRoomSectorIds = []
    actualRoomNames = []
    storage = 0
    for m in matches:
        roomName, sectorID, checksum = m.group("roomName"), int(m.group("sectorID")), m.group("checksum")
        roomNameNoDash = roomName.replace("-", "")
        chars = set(roomNameNoDash)
        counts = [(c, roomNameNoDash.count(c)) for c in chars]
        top = sorted(counts, key=keyFunc, reverse=True)
        actualCheckSum = ''.join([cd for ch in [sorted([c[0] for c in list(g)]) for _, g in itertools.groupby(top, keyFunc)] for cd in ch][:5])
        if actualCheckSum == checksum:
            actualRoomSectorIds.append(sectorID)
            actualRoomNames.append((roomName, sectorID))
            words = roomName.split("-")
            decrpytedWords = [string.translate(s, cipher(sectorID)) for s in words]
            if any("north" in w for w in decrpytedWords):
                storageRoom = sectorID

    return sum(actualRoomSectorIds), storageRoom

########################################################################################################################
### Output #############################################################################################################
########################################################################################################################


def main():
    print prettyInfo(DAY_DESC, DAY_INPUT_STR)
    print prettyAnswers(*solution())


if __name__ == "__main__":
    main()
