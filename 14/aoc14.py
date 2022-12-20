#!/usr/bin/env python3


# class Location:
#    def __init__(self, x, y, material):
#        self.x = x
#        self.y = y
#        self.material = "."  # air


class Map:
    def __init__(self):
        self.minx = -1
        self.maxx = 0
        self.miny = 0  # stays zero
        self.maxy = 0
        self.locations = {(500, 0): "+"}


def Draw_Lines(my_map, coords):

    for i in range(len(coords) - 1):

        # draw rock line from i to i+1
        (x1, y1) = coords[i].split(",")
        (x2, y2) = coords[i + 1].split(",")
        x1 = int(x1)
        x2 = int(x2)
        y1 = int(y1)
        y2 = int(y2)

        if x1 == x2:
            if y1 < y2:
                y0 = y1
                yn = y2
            else:
                y0 = y2
                yn = y1
            while y0 <= yn:
                if (x1, y0) not in my_map.locations:
                    my_map.locations[(x1, y0)] = "#"
                y0 += 1
        else:
            if x1 < x2:
                x0 = x1
                xn = x2
            else:
                x0 = x2
                xn = x1
            while x0 <= xn:
                if (x0, y1) not in my_map.locations:
                    my_map.locations[(x0, y1)] = "#"
                x0 += 1


def Build_Map(lines):

    my_map = Map()
    for line in lines:
        # maybe I shouldn't use "line" since we'll be drawing lines later...
        coords = []
        coords = line.split(" -> ")
        Draw_Lines(my_map, coords)

    # find min/max
    for (x, y) in my_map.locations:
        if y > my_map.maxy:
            my_map.maxy = y
        if x < my_map.minx or my_map.minx == -1:
            my_map.minx = x
        if x > my_map.maxx:
            my_map.maxx = x

    return my_map


def Make_Sand_Happen(my_map):
    # sand always starts at (500,0)

    count = 0

    while 1:

        # Enter new sand...
        sandx = 500
        sandy = 0
        # loop over shit until sand falls off the map
        while 1:
            if (sandx, sandy + 1) not in my_map.locations:  # air below, keep going.
                sandy += 1
                if sandy > my_map.maxy:
                    return count
                continue

            # directly below is solid
            elif (sandx - 1, sandy + 1) not in my_map.locations:
                # left/down is available
                sandx -= 1
                sandy += 1

                if sandx < my_map.minx:
                    print("nuh uh")
                    return count
                continue
            elif (sandx + 1, sandy + 1) not in my_map.locations:
                # Can't go left, try right.
                sandx += 1
                sandy += 1
                if sandx > my_map.maxx:
                    print("nuh uh 2")
                    return count
                continue

            else:  # this is our resting spot
                my_map.locations[(sandx, sandy)] = "O"
                break

        count += 1


def Print_Map(my_map):
    print("Min/Max X: ", my_map.minx, my_map.maxx)
    print("Min/Max Y: ", my_map.miny, my_map.maxy)
    print()

    minx = list(str(my_map.minx))
    maxx = list(str(my_map.maxx))

    yloc = 0
    ylen = len(str(my_map.maxy))
    xlen = my_map.maxx - my_map.minx + 1
    # print header
    for i in range(3):
        line = " " * ylen + " "
        line += minx[i]

        xloc = my_map.minx + 1
        # every 10 we can print another coord number
        while xloc < my_map.maxx:
            if xloc % 10 == 0:
                locx = list(str(xloc))
                line += locx[i]
            else:
                line += " "
            xloc += 1

        line += maxx[i]
        print(line)

        # if (x,y) not in my_map.locations print air "."
    y = 0
    while y <= my_map.maxy:
        print(y, end="")
        spaces = " " * (ylen - int(len(str(y))) + 1)
        print(spaces, end="")
        x = my_map.minx
        while x <= my_map.maxx:
            if (x, y) in my_map.locations:
                print(my_map.locations[(x, y)], end="")
            else:
                print(".", end="")
            x += 1
        print()
        y += 1


testcase = False
if testcase:
    file = "test.txt"
else:
    file = "input.txt"

with open(file, "r") as stuff:
    lines = stuff.read().splitlines()

    my_map = Build_Map(lines)

    count = 0
    count = Make_Sand_Happen(my_map)
    Print_Map(my_map)

    print("Rnd1 Count:", count)
