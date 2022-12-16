#!/usr/bin/env python3

import re
import copy

"""
Reading the input stepped up a little in difficulty

    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2

"""


def learn_stacks(lines):
    """
    First, collapse all the formatting out of the stacks

     D
    NC
    ZMP
    123
    """
    stacks = {}
    i = 0
    while 1:
        lines[i] = re.sub(r"\s\s\s\s", " ", lines[i])
        lines[i] = re.sub(r"\] \[", "", lines[i])
        lines[i] = re.sub(r"\]\s(\s*)\[", r"\1", lines[i])
        lines[i] = re.sub(r"[\]\[]", "", lines[i])
        if re.match(r"^ 1", lines[i]):
            bottom = i
            lines[i] = re.sub(r"\s", "", lines[i])
            break
        else:
            i += 1
    print("Bottom of stacks at: ", bottom)
    num_stacks = len(lines[bottom])
    print("Num Stacks: ", num_stacks)

    # initialize stacks
    for i in range(num_stacks):
        stacks[i + 1] = list()

    for i in reversed(range(bottom)):
        chars = list(lines[i])
        for c in range(len(chars)):
            # c is the stack -1
            if chars[c] != " ":
                stacks[c + 1].append(chars[c])

    return stacks


with open("input.txt", "r") as stuff:
    lines = stuff.read().splitlines()

    # Populate the 'stacks' data structure
    stacks = learn_stacks(lines)

    # Remember, we can't just copy a list or dict directly very easily.
    stacks2 = copy.deepcopy(stacks)  # Just prep for Rnd 2

    # Rnd1
    for line in lines:
        m = re.search(r"move\s(\d+)\sfrom\s(\d+)\sto\s(\d+)", line)
        if m:
            moves = int(m.group(1))
            f_stack = int(m.group(2))
            t_stack = int(m.group(3))
            # for # of moves
            for i in range(moves):
                crate = stacks[f_stack].pop()
                stacks[t_stack].append(crate)

    output = ""
    for i in range(len(stacks)):
        output += stacks[i + 1].pop()

    print("Rnd1 top crates: ", output)

    # Rnd2
    for line in lines:
        m = re.search(r"move\s(\d+)\sfrom\s(\d+)\sto\s(\d+)", line)
        if m:
            moves = int(m.group(1))
            f_stack = int(m.group(2))
            t_stack = int(m.group(3))

            # Take moves # of crates off a stack and append them to the other.
            crates = stacks2[f_stack][-moves:]
            del stacks2[f_stack][-moves:]
            stacks2[t_stack].extend(crates)

    output = ""
    for i in range(len(stacks2)):
        if len(stacks2[i + 1]) > 0:
            output += stacks2[i + 1].pop()

    print("Rnd2 top crates: ", output)
