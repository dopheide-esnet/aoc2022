#!/usr/bin/env python3

import re

bonus = {"X": 1, "Y": 2, "Z": 3}  # rock, paper, scissors


def get_points(them, me):
    points = 0

    if them == "A":
        if me == "X":
            points += 3
        elif me == "Y":
            points += 6
    elif them == "B":
        if me == "Y":
            points += 3
        elif me == "Z":
            points += 6
    else:
        if me == "Z":
            points += 3
        elif me == "X":
            points += 6

    points += bonus[me]
    return points


with open("input.txt", "r") as stuff:
    sacks = stuff.readlines()

    r1_total = 0
    r2_total = 0
    for line in rounds:
        m = re.search(r"^([ABC])\s([XYZ])", line)
        if m:
            them = m.group(1)
            me = m.group(2)
        r1_total += get_points(them, me)

        # round 2
        # X = lose, Y = draw, Z = win
        # then convert to the letter we useds as an item in rd1
        if me == "X":
            if them == "A":
                me = "Z"
            elif them == "B":
                me = "X"
            else:
                me = "Y"
        elif me == "Y":
            if them == "A":
                me = "X"
            elif them == "B":
                me = "Y"
            else:
                me = "Z"
        elif me == "Z":
            if them == "A":
                me = "Y"
            elif them == "B":
                me = "Z"
            else:
                me = "X"

        r2_total += get_points(them, me)


print("round 1 total: ", r1_total)
print("round 2 total: ", r2_total)
