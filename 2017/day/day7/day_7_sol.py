from re import match
from collections import Counter

weight, supports = {}, {}
with open("input_7.txt") as input_file:
    for line in input_file:
        m = match("^(\w+) \((\d+)\)(?: -> )?(.*)$", line)
        prog = m.group(1)
        weight[prog] = int(m.group(2))
        supports[prog] = m.group(3).split(", ") if m.group(3) else []

def part1():
    supported = {s for supp in supports.values() for s in supp}
    unsupported = [prog for prog in supports if prog not in supported]
    assert len(unsupported) == 1
    return unsupported[0]

def total_weight(prog):
    return weight[prog] + sum(total_weight(s) for s in supports[prog])

def fix_weight(prog, delta):
    total_wts = Counter(map(total_weight, supports[prog]))
    if len(total_wts)==1: return prog, weight[prog] + delta
    assert len(total_wts) == 2
    ((w2, c2), (w1, c1)) = total_wts.most_common(2)
    assert c1 == 1
    bad = [s for s in supports[prog] if total_weight(s)==w1]
    assert len(bad) == 1
    return fix_weight(bad[0], w2-w1)

def part2(): return fix_weight(part1(), None)

print part2()