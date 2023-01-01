#!/usr/bin/env python3

import re

class Cube:
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z
        self.open_sides = 0

def Check_Sides(cubes):
    ''' Run through the cubes and check for open sides '''
    total = 0
    for cube in cubes:
        open_sides = 0
        (x,y,z) = cube
        if( (x-1,y,z) not in cubes):
            open_sides += 1
        if( (x+1,y,z) not in cubes):
            open_sides += 1
        if( (x,y-1,z) not in cubes):
            open_sides += 1
        if( (x,y+1,z) not in cubes):
            open_sides += 1 
        if( (x,y,z-1) not in cubes):
            open_sides += 1
        if( (x,y,z+1) not in cubes):
            open_sides += 1

        cubes[cube].open_sides = open_sides
        total += open_sides     
    return total

testcase = False
if testcase:
    file = "test.txt"
else:
    file = "input.txt"

with open(file, "r") as stuff:
    lines = stuff.read().splitlines()

    cubes = {}
    
    for line in lines:
        (sx,sy,sz) = line.split(",")
        x = int(sx)
        y = int(sy)
        z = int(sz)
        cubes[(x,y,z)] = Cube(x,y,z)

    print("Num cubes:",len(cubes))

    total_open_sides = Check_Sides(cubes)

    print("Rnd1 Total Open Sides:",total_open_sides)

