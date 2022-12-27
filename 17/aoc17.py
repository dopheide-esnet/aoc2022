#!/usr/bin/env python3

import re

class Rock:
    def __init__(self, shape, y, x):
        self.width = len(shape[0])
        self.height = len(shape)
        self.x = x
        self.y = y
        self.shape = shape

testcase = True
if testcase:
    file = "test.txt"
    c_width = 7
    num_rocks = 2022
else:
    file = "input.txt"
    c_width = 7
    num_rocks = 2022

# Initialize Rocks
shapes = []
shapes.append(Rock(['####']))
shapes.append(Rock(['.#.',
                   '###',
                   '.#.']))
shapes.append(Rock(['..#',
                   '..#',
                   '###']))
shapes.append(Rock(['#',
                   '#',
                   '#',
                   '#']))
shapes.append(Rock(['##',
                   '##']))

with open(file, "r") as stuff:
    lines = stuff.read().splitlines()

    stack = []  # stack of rocks
    stack_height = 0
    active = False  # is there an active rock?
    next_shape = 0
    for line in lines:
        print(line)
        print("BLAA")
    exit()

    while(len(stack) <= num_rocks):
        if(not active):
            # Generate new rock
            The_Rock = Rock(shapes[next_shape],stack_height+4, 3)
            next_shape += 1
            if(next_shape == len(shapes)):
                next_shape = 0



