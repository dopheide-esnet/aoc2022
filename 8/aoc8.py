#!/usr/bin/env python3

import re

# Visible Trees


class Tree:
    def __init__(self, height, x, y):
        self.height = int(height)
        self.x = int(x)
        self.y = int(y)
        self.visible = False
        self.left = 0
        self.right = 0
        self.up = 0
        self.down = 0
        self.scenic = 0


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


def Print_Forest(forest):
    total = 0
    smax = 0
    for row in forest:
        for tree in row:
            if tree.scenic > smax:
                smax = tree.scenic
            if tree.visible:
                print("V", end="")
                total += 1
            else:
                print("_", end="")
        print()
    print("Rnd1 Total Visible: ", total)
    print("Rnd2: Best Scenic: ", smax)


def Do_Rows(forest):
    """
    Step through each tree keeping track of the tallest tree along the way.
    Set visible=True if (x==0 or x==maxX) or if the tallest tree is shorter than it.  Then it's the new tallest also.
    """
    maxX = len(forest)

    for row in forest:
        max_tree = 0
        for tree in row:
            if (tree.x == 0) or (tree.x == (maxX - 1)):
                forest[tree.y][tree.x].visible = True  # change the actual forest
            if tree.height > max_tree:
                forest[tree.y][tree.x].visible = True
                max_tree = tree.height

        # now go right to left, we've already checked if it's an edge
        max_tree = 0
        for x in reversed(range(len(row))):
            tree = row[x]
            if tree.height > max_tree:
                forest[tree.y][tree.x].visible = True
                max_tree = tree.height


def Do_Cols(forest):
    maxY = len(forest[0])
    # for each column...
    for x in range(len(forest)):

        # Go down the column first
        max_tree = 0
        for y in range(maxY):
            if (forest[y][x].y == 0) or (forest[y][x].y == (maxY - 1)):
                forest[y][x].visible = True
            if forest[y][x].height > max_tree:
                forest[y][x].visible = True
                max_tree = forest[y][x].height

        # Now go up the column
        max_tree = 0
        for y in reversed(range(maxY)):
            if forest[y][x].height > max_tree:
                forest[y][x].visible = True
                max_tree = forest[y][x].height


def Do_Scenic(forest):
    maxY = len(forest[0])
    maxX = len(forest)

    for x in range(maxX):
        for y in range(maxY):
            height = forest[y][x].height

            # Go left
            distance = 0
            max_height = -1
            i = x - 1
            while i >= 0:
                distance += 1
                if forest[y][i].height >= height or forest[y][i].height == max_height:
                    break
                if forest[y][i].height > max_height and forest[y][i].height >= height:
                    max_height = forest[y][i].height
                i -= 1
            forest[y][x].left = distance

            # Go right
            distance = 0
            max_height = -1
            i = x + 1
            while i < maxX:
                distance += 1
                if forest[y][i].height >= height or forest[y][i].height == max_height:
                    break
                if forest[y][i].height > max_height and forest[y][i].height >= height:
                    max_height = forest[y][i].height
                i += 1
            forest[y][x].right = distance

            # Go up
            distance = 0
            max_height = -1
            i = y - 1
            while i >= 0:
                distance += 1
                if forest[i][x].height >= height or forest[i][x].height == max_height:
                    break
                if forest[i][x].height > max_height and forest[i][x].height >= height:
                    max_height = forest[i][x].height
                i -= 1
            forest[y][x].up = distance

            # Go down
            distance = 0
            max_height = -1
            i = y + 1
            while i < maxY:
                distance += 1
                if forest[i][x].height >= height or forest[i][x].height == max_height:
                    break
                if forest[i][x].height > max_height and forest[i][x].height >= height:
                    max_height = forest[i][x].height
                i += 1
            forest[y][x].down = distance

            # Are we getting far enough right and down?

            debug = 0
            if debug:
                print(
                    forest[y][x].left,
                    forest[y][x].right,
                    forest[y][x].up,
                    forest[y][x].down,
                )
                exit(1)
            # calculate scenic, assume an edge tree having a 0 value gets a 0 scenic value because Math
            forest[y][x].scenic = (
                forest[y][x].left
                * forest[y][x].right
                * forest[y][x].up
                * forest[y][x].down
            )


with open("input.txt", "r") as stuff:
    lines = stuff.read().splitlines()

    # Start by building a 2D grid of class Tree
    forest = Build_Forest(lines)

    Do_Rows(forest)
    Do_Cols(forest)

    # Rnd2 Scenic Score
    # We could try to track this as we do the rows/cols.
    # Probably faster to just make the computer do the work.
    Do_Scenic(forest)

    Print_Forest(forest)


## then count visible
