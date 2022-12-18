#!/usr/bin/env python3

import re
import math


class Monkey:
    def __init__(self, name, items, op, test, targetT, targetF):
        self.name = name
        self.items = items
        self.op = op  # str we'll parse in operation()
        self.test = test  # digit we'll divide by (it's always divide)
        self.targetT = targetT  # Monkey we target if test is T
        self.targetF = targetF  # Monkey we target if test is F
        self.inspections = 0

    def Operation(self, old):
        # do some math based on self.op

        # it would be better to parse this on __init__, but who cares!
        # Rnd2 Cares!
        m = re.search(r"new = (\w+) ([\+\*]) (\w+)", self.op)
        if m:
            if m.group(1) == "old":
                one = old
            else:
                one = int(m.group(1))
            if m.group(3) == "old":
                two = old
            else:
                two = int(m.group(3))
            if m.group(2) == "+":
                new = one + two
            else:
                new = one * two
        else:
            print(self.op)
            print("Error, unsupported operation")

        #        if new > 1000:
        #            new = new / 1000
        return new

    def Test(self, item):
        if item % self.test == 0:
            return self.targetT
        else:
            return self.targetF


## INITIALIZE
testcase = False
Rnd1 = False
Worry_Cleanup = False
if testcase:
    monkeys = [
        Monkey(0, [79, 98], "new = old * 19", 23, 2, 3),
        Monkey(1, [54, 65, 75, 74], "new = old + 6", 19, 2, 0),
        Monkey(2, [79, 60, 97], "new = old * old", 13, 1, 3),
        Monkey(3, [74], "new = old + 3", 17, 0, 1),
    ]
else:
    # my input
    monkeys = [
        Monkey(0, [91, 58, 52, 69, 95, 54], "new = old * 13", 7, 1, 5),
        Monkey(1, [80, 80, 97, 84], "new = old * old", 3, 3, 5),
        Monkey(2, [86, 92, 71], "new = old + 7", 2, 0, 4),
        Monkey(
            3,
            [96, 90, 99, 76, 79, 85, 98, 61],
            "new = old + 4",
            11,
            7,
            6,
        ),
        Monkey(4, [60, 83, 68, 64, 73], "new = old * 19", 17, 1, 0),
        Monkey(5, [96, 52, 52, 94, 76, 51, 57], "new = old + 3", 5, 7, 3),
        Monkey(6, [75], "new = old + 5", 13, 4, 2),
        Monkey(7, [83, 75], "new = old + 1", 19, 2, 6),
    ]

    ## MAIN ##

if testcase:
    print("TESTCASE")

if Rnd1:
    num_rounds = 20
else:
    num_rounds = 10000

# determine common factor we'll need later for Rnd2
factor = 1
for monkey in monkeys:
    factor *= monkey.test

for round in range(num_rounds):
    if round % 100 == 0:
        print("Round: ", round)

    for monkey in monkeys:

        ## TODO loop over this monkey's items by changing 'if' to while
        while len(monkey.items) > 0:
            # increment inspection count
            monkey.inspections += 1
            # find bug
            # get the first item in their list
            item = monkey.items.pop(0)
            # do the operation
            new_item = monkey.Operation(item)

            # Reduce Worry
            if Worry_Cleanup:
                new_item = math.floor(new_item / 3)

            # do the test to find out the next monkey
            target = monkey.Test(new_item)

            # For Rnd2.. gotta keep those numbers small
            # Messing with precision does not work.

            # If we're a monkey that sucks, do some trickery,
            # divide by a common factor.
            # Can we always do this?  Probably, but whatever.
            if not Worry_Cleanup:
                if "old * old" in monkey.op and new_item > factor:
                    new_item = factor + new_item % factor

            # throw
            monkeys[target].items.append(new_item)

if testcase:
    print("Monkey 0:", monkeys[0].inspections)
    print("Monkey 1:", monkeys[1].inspections)
    print("Monkey 2:", monkeys[2].inspections)
    print("Monkey 3:", monkeys[3].inspections)

# Calculate monkey business
ins = []
for monkey in monkeys:
    ins.append(monkey.inspections)
ins.sort(reverse=True)
print("Rnd1 Monkey Business:", (ins[0] * ins[1]))

if testcase:
    print("TESTCASE")
