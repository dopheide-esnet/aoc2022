#!/usr/bin/env python3

import re

# Tail follows Head


class Knot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visited = [",".join([str(x), str(y)])]  # we won't use this for the Head


def adjacent(head, tail):
    diff = abs(head.x - tail.x)
    if diff > 1:
        return False
    diff = abs(head.y - tail.y)
    if diff > 1:
        return False
    return True


def check_tail(tail):
    new = ",".join([str(tail.x), str(tail.y)])
    if new not in tail.visited:
        tail.visited.append(new)


def move_tail(head, tail):
    # if on the same orthagonal line, easy.
    # if not on the same orthagonal line, move diagonally in the direction where the difference is greater

    # x is the same, move y
    if head.x == tail.x:
        if head.y < tail.y:
            tail.y -= 1
        else:
            tail.y += 1
        check_tail(tail)
        return
    elif head.y == tail.y:
        if head.x < tail.x:
            tail.x -= 1
        else:
            tail.x += 1
        check_tail(tail)
        return

    # Welp, I guess we have to move diagonally, which way?
    if head.x > tail.x:
        tail.x += 1
    else:
        tail.x -= 1
    if head.y > tail.y:
        tail.y += 1
    else:
        tail.y -= 1
    check_tail(tail)

    return


with open("input.txt", "r") as stuff:
    lines = stuff.read().splitlines()

    # initialize
    # head = Knot(0, 0)
    # tail = Knot(0, 0)

    # rope length = 10 for Rnd2
    rope = []
    for i in range(10):
        rope.append(Knot(0, 0))

    for line in lines:
        (direction, num) = line.split(" ")
        num = int(num)

        # move Head num times in this direction, after each move check Tail
        for i in range(num):
            if direction == "L":
                rope[0].x -= 1
            elif direction == "R":
                rope[0].x += 1
            elif direction == "U":
                rope[0].y += 1
            elif direction == "D":
                rope[0].y -= 1
            else:
                print("WHUT?")
                exit()

            for x in range(len(rope) - 1):
                if not adjacent(rope[x], rope[x + 1]):
                    move_tail(rope[x], rope[x + 1])

    print("Rnd1 Visited Locations:", len(rope[1].visited))  # 6030
    print("Rnd2 Visited Locations:", len(rope[len(rope) - 1].visited))
