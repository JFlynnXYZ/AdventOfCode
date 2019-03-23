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
import re
PROG_REGEX = re.compile(r"(?P<name>\w+) \((?P<weight>\d+)\)(?:(?: -> )(?P<children>[\w, ]*))?")


class Program(object):
    all_processes = {}
    root_proc = None

    def __init__(self, s):
        match = PROG_REGEX.match(s)
        if not match:
            raise ValueError("Invalid program string '{}'".format(s))
        self.name = match.group("name")
        self.weight = int(match.group("weight"))
        self.child_names = match.group("children").split(", ") if match.group("children") != None else []
        self.children = []
        self.parent = None
        Program.all_processes[self.name] = self

    def __repr__(self):
        children = ', '.join([x.name for x in self.children])
        return "<{}: {}; Children: {}>".format("Program",
                                               self.name,
                                               children)

    def total_child_weight(self):
        weight = self.weight
        for c, _ in self.walk(self):
            weight += c.weight
        return weight

    def has_children(self):
        return len(self.children) > 0

    def find_unbalanced_program(self, root=None):
        if root is None:
            root = self
        if root.has_children():
            for c in root:
                if c.is_unbalanced():
                    return self.find_unbalanced_program(c)
            else:
                weights = [x.total_child_weight() for x in root]
                dif_weight = Counter(weights).most_common()[-1][0]
                child = root.children[weights.index(dif_weight)]
                return child
        else:
            return root

    def parent_weight_offset(self):
        weights = []
        for c in self.parent:
            if c == self:
                continue
            weights.append(c.total_child_weight())
        target_weight = set(weights).pop()
        return self.total_child_weight() - target_weight

    def new_required_weight(self):
        return self.weight - self.parent_weight_offset()

    def child_weights(self):
        return [c.total_child_weight() for c in self.children]

    def is_unbalanced(self):
        return len(set(self.child_weights())) > 1

    def __str__(self):
        return self.name

    def pprint(self, level=0):
        ret = "\t" * level + repr(self.name) + "\n"
        for child in self.children:
            ret += child.pprint(level + 1)
        return ret

    def __iter__(self):
        for c in self.children:
            yield c

    def _assign_children(self):
        for n in self.child_names:
            self.children.append(Program.all_processes[n])
            Program.all_processes[n].parent = self

    @staticmethod
    def assign_all_children():
        for n,p in Program.all_processes.iteritems():
            p._assign_children()

        for n,p in Program.all_processes.iteritems():
            if p.parent is None:
                Program.root_proc = p
                break

    @staticmethod
    def draw_graph():
        for p in Program.root_proc:
            print p.pprint()

    @staticmethod
    def bottom_program():
        return Program.root_proc

    @staticmethod
    def walk(val=None, level=0):
        if val is None:
            val = Program.root_proc
            level = -1
        else:
            yield val, level

        level +=1

        for c in val:
            yield c, level
            for child, lvl in c.walk(c, level= level):
                yield child, lvl



def solve1(inp):
    for l in inp:
        Program(l)
    Program.assign_all_children()
    return Program.bottom_program()


def solve2(inp):
    return Program.bottom_program().find_unbalanced_program().new_required_weight()



def solution():
    return solve1(DAY_INPUT), solve2(DAY_INPUT)


########################################################################################################################
### Output #############################################################################################################
########################################################################################################################


def main():
    print prettyInfo(DAY_DESC, DAY_INPUT_STR)
    print prettyAnswers(*solution())


if __name__ == "__main__":
    main()

