# barnybug https://www.reddit.com/r/adventofcode/comments/5gy1f2/2016_day_7_solutions/davzcwy/

import re
def abba(x):
    return any(a == d and b == c and a != b for a, b, c, d in zip(x, x[1:], x[2:], x[3:]))
lines = [re.split(r'\[([^\]]+)\]', line) for line in open('input.txt')]
parts = [(' '.join(p[::2]), ' '.join(p[1::2])) for p in lines]
print('Answer #1:', sum(abba(sn) and not(abba(hn)) for sn, hn in parts))
print('Answer #2:', sum(any(a == c and a != b and b+a+b in hn for a, b, c in zip(sn, sn[1:], sn[2:])) for sn, hn in parts))

#bpeel https://github.com/bpeel/advent2016/blob/master/day7.py
import sys
import re

def has_abba(s):
    return re.search(r'(.)(?!\1)(.)\2\1', s) != None

def has_tls(s):
    for md in re.finditer(r'\[.*?\]', s):
        if has_abba(md.group(0)):
            return False

    return has_abba(s)

def hypernet_has_bab(s, bab):
    for md in re.finditer(r'\[.*?\]', s):
        if md.group(0).find(bab) != -1:
            return True

    return False

def has_ssl(s):
    for outside in re.split(r'\[.*?\]', s):
        for md in re.finditer(r'(?=((.)(?!\2).\2))', outside):
            aba = md.group(1)

            if hypernet_has_bab(s, aba[1] + aba[0] + aba[1]):
                return True

    return False

lines = [line.rstrip() for line in sys.stdin]
print("Part 1", sum(map(has_tls, lines)))
print("Part 2", sum(map(has_ssl, lines)))