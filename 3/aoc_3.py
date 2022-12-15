#!/usr/bin/env python3

import re

value_str = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def find_common(one, two):
    first = list(one)
    for char in first:
        if char in two:
            return char


def find_all_common(one, two):
    first = list(one)
    out = ""
    for char in first:
        if char in two:
            out += char
    return out


with open("input.txt", "r") as stuff:
    sacks = stuff.readlines()

    total = 0
    for line in sacks:
        line = line.strip()
        half = int(len(line) / 2)

        one = line[:half]
        two = line[half:]
        common = find_common(one, two)

        total += value_str.find(common) + 1

    rnd1_total = total
    total = 0
    # groups of three.
    i = 0
    while i < len(sacks):
        one = sacks[i].strip()
        two = sacks[i + 1].strip()
        three = sacks[i + 2].strip()
        common_a = find_all_common(one, two)
        common = find_common(common_a, three)
        total += value_str.find(common) + 1
        i += 3


print("Rnd1 total: ", rnd1_total)
print("Rnd2 total: ", total)
