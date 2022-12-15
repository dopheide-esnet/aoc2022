#!/usr/bin/env python3

import re

with open("input.txt", "r") as calories:
    clist = calories.readlines()

    e = 0
    elves = (
        {}
    )  # could do a list, but I want to use sort which would screw up the elf numbers.
    total = 0

    for line in clist:
        if re.match(r"^\s*\n$", line):
            elves[e] = total
            e += 1
            total = 0
            continue
        total += int(line.strip())

s_elves = sorted(elves.items(), key=lambda x: x[1], reverse=True)

print("Top elf calories = ", s_elves[0][1])

top_three = s_elves[0][1] + s_elves[1][1] + s_elves[2][1]

print("Top three elves calories = ", top_three)
