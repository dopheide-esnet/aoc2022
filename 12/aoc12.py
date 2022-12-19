#!/usr/bin/env python3

"""
Oh sure, my tricorder can't talk to the elves, but it can provide a detailed topigraphical map no problem!
"""

import sys

# Welp...  if this doesn't work we can try saving state and restarting
sys.setrecursionlimit(2000)


class Location:
    def __init__(self, x, y, loc, distance):
        self.x = x
        self.y = y
        self.smallest_distance = distance


op_counter = 0


def Build_Map(*argv):
    """
    Build our map from the input, but also convert it to integers to make comparisons easier
    """
    my_map = []

    if len(argv) == 0:
        stuff = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
"""
        lines = stuff.splitlines()

    else:
        lines = argv[0]

    row = 0
    for line in lines:
        # watch out for start and end positions, S and E
        ess = line.find("S")
        eee = line.find("E")
        if ess != -1:
            start = [ess, row]
        if eee != -1:
            end = [eee, row]
        line = list(line)
        my_map.append(line)
        row += 1

    my_map[start[1]][start[0]] = "a"
    my_map[end[1]][end[0]] = "z"

    return my_map, start, end


def Print_Map(my_map, locations):
    for y in range(len(my_map)):
        for x in range(len(my_map[0])):
            if (x, y) in locations:
                print(".", end="")
            else:
                print(my_map[y][x], end="")
        print()
    return


def Go_Next(distance, prevx, prevy, x, y, my_map, locations):
    """Try going to our surrounding locations, ignoring where we just came from"""

    if distance > 500:
        # Yeah.. unlikely, stop trying.
        # Also if we let it go we'll overrun the stack.
        return

    # Go Up
    if y < len(my_map) - 1 and (y + 1) != prevy:
        if (ord(my_map[y + 1][x]) - ord(my_map[y][x])) <= 1:
            Go(distance + 1, x, y, x, y + 1, my_map, locations)
    # Go Down
    if y > 0 and (y - 1) != prevy:
        if (ord(my_map[y - 1][x]) - ord(my_map[y][x])) <= 1:
            Go(distance + 1, x, y, x, y - 1, my_map, locations)
    # Go Right
    if x < len(my_map[0]) - 1 and (x + 1) != prevx:
        if (ord(my_map[y][x + 1]) - ord(my_map[y][x])) <= 1:
            Go(distance + 1, x, y, x + 1, y, my_map, locations)
    # Go Left
    if x > 0 and (x - 1) != prevx:
        if (ord(my_map[y][x - 1]) - ord(my_map[y][x])) <= 1:
            Go(distance + 1, x, y, x - 1, y, my_map, locations)

    return


def Go(distance, prevx, prevy, x, y, my_map, locations):
    global op_counter
    op_counter += 1

    # basically is b - a <= 1
    if (x, y) not in locations:
        locations[(x, y)] = Location(x, y, (x, y), distance)
        # continue going this way
        Go_Next(distance, prevx, prevy, x, y, my_map, locations)
    else:
        # we're in locations, if distance is less, update, if it's more, quit.
        # print("already been here, need to Go_Next")
        # also if it's less, we have to keep exploring from here since everything from here
        # will also be less (UH OH)
        if distance < locations[(x, y)].smallest_distance:
            locations[(x, y)].smallest_distance = distance
            Go_Next(distance, prevx, prevy, x, y, my_map, locations)
    return


##########
#  MAIN  #
##########

testcase = False
if testcase:
    (my_map, start, end) = Build_Map()
else:
    with open("input.txt", "r") as stuff:
        lines = stuff.read().splitlines()
        (my_map, start, end) = Build_Map(lines)

print("Start:", start)
print("End:", end)

locations = {}  #  (x,y) tuple
attempts = []
distance = 0

# We always start on the left edge, pretend previous x was off the edge
Go_Next(distance, -1, start[1], start[0], start[1], my_map, locations)

if testcase:
    for loc in locations:
        print(loc, locations[loc].smallest_distance)

# Find quickest way to any given location.  Update if a shorter distance is found.

## once we've explored the whole map, check the End location for smallest_distance.

print("Operations: ", op_counter)
Print_Map(my_map, locations)

print("Rnd1 Shortest Path: ", locations[(end[0], end[1])].smallest_distance)
