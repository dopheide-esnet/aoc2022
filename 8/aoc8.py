#!/usr/bin/env python3

import re

# Visible Trees


class Tree:
    def __init__(self, height, x, y):
        self.height = int(height)
        self.x = int(x)
        self.y = int(y)
        self.visible = True
        # what's the highest tree in each direction?
        # may save time later by letting us just run through a row left/right and col up/down all at once.
        self.left = 0
        self.right = 0
        self.up = 0
        self.down = 0


def Build_Forest(lines):
    """Take our input and build a 2D array of Trees"""
    y = 0
    x = 0
    all_trees = list()
    for line in lines:
        row = list(line)
        treeline = list()
        x = 0
        for r in row:
            treeline.append(Tree(r, x, y))
            x += 1
        all_trees.append(treeline)
        y += 1
    return all_trees


with open("input.txt", "r") as stuff:
    lines = stuff.read().splitlines()

    # Start by building a 2D grid of class Tree
    forest = Build_Forest(lines)
    maxX = len(forest[0])
    maxY = len(forest)
    print("MaxX, MaxY: ", maxX, maxY)
