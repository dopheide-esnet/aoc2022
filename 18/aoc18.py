#!/usr/bin/env python3

import re
import sys
sys.setrecursionlimit(10000)

class Cube:
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z
        self.open_sides = 0
        self.x_p = False  # side next to x+1 is not exposed
        self.x_m = False
        self.y_p = False
        self.y_m = False
        self.z_p = False
        self.z_m = False

class Air:
    def __init__(self, exp):
        self.exposed = exp  # unused

def Check_Sides(cubes):
    ''' Run through the cubes and check for open sides '''
    total = 0
    for cube in cubes:
        open_sides = 0
        (x,y,z) = cube
        if( (x-1,y,z) not in cubes):
            open_sides += 1
            cubes[cube].x_m = True
        if( (x+1,y,z) not in cubes):
            open_sides += 1
            cubes[cube].x_p = True
        if( (x,y-1,z) not in cubes):
            open_sides += 1
            cubes[cube].y_m = True
        if( (x,y+1,z) not in cubes):
            open_sides += 1 
            cubes[cube].y_p = True
        if( (x,y,z-1) not in cubes):
            open_sides += 1
            cubes[cube].z_m = True
        if( (x,y,z+1) not in cubes):
            open_sides += 1
            cubes[cube].z_p = True

        cubes[cube].open_sides = open_sides
        total += open_sides     
    return total

def FillAir(air,cubes,x,y,z,extents):
    ''' Starting at our minimum extents, try to fill every open space '''

    (minx,miny,minz,maxx,maxy,maxz) = extents

    air[(x,y,z)] = Air(True)
    # Try right:
    if( x+1 <= maxx and (x+1,y,z) not in air and (x+1,y,z) not in cubes):
        FillAir(air,cubes,x+1,y,z, extents)
    # Try left:
    if( x-1 >= minx and (x-1,y,z) not in air and (x-1,y,z) not in cubes):
        FillAir(air,cubes,x-1,y,z, extents)

    # Try up:
    if( y+1 <= maxy and (x,y+1,z) not in air and (x,y+1,z) not in cubes):
        FillAir(air,cubes,x,y+1,z, extents)
    # Try down:
    if( y-1 >= miny and (x,y-1,z) not in air and (x,y-1,z) not in cubes):
        FillAir(air,cubes,x,y-1,z, extents)

    # Try in:
    if( z+1 <= maxz and (x,y,z+1) not in air and (x,y,z+1) not in cubes):
        FillAir(air,cubes,x,y,z+1, extents)
    # Try out:
    if( z-1 >= minz and (x,y,z-1) not in air and (x,y,z-1) not in cubes):
        FillAir(air,cubes,x,y,z-1, extents)  


def Find_Trapped_Air(air,cubes,trapped,extents):
    (minx,miny,minz,maxx,maxy,maxz) = extents
    for x in range(minx,maxx+1):
        for y in range(miny,maxy+1):
            for z in range(minz,maxz+1):
                if( (x,y,z) not in air and (x,y,z) not in cubes):
                    trapped[(x,y,z)] = 1

def Print_Cube(x,y,z):
    print("Cube:",x,y,z)
    print("Open Sides:",cubes[(x,y,z)].open_sides)
    print("Side X-plus:",cubes[(x,y,z)].x_p)
    print("Side X-minus:",cubes[(x,y,z)].x_m)
    print("Side Y-plus:",cubes[(x,y,z)].y_p)
    print("Side Y-minus:",cubes[(x,y,z)].y_m)
    print("Side Z-plus:",cubes[(x,y,z)].z_p)
    print("Side Z-minus:",cubes[(x,y,z)].z_m)

def Explore_Trapped(cubes, trapped):
    ''' Explored the trapped air, see where it touches cubes. '''
    ''' When this is done we'll need to recalculate the open_sides '''
    for air in trapped:
        (x,y,z) = air

        # Try right:
        if( (x+1,y,z) in cubes ):
            cubes[(x+1,y,z)].x_m = False
        # Try left:
        if( (x-1,y,z) in cubes ):
            cubes[(x-1,y,z)].x_p = False

        # Try up:
        if( (x,y+1,z) in cubes ):
            cubes[(x,y+1,z)].y_m = False
        # Try down:
        if( (x,y-1,z) in cubes ):
            cubes[(x,y-1,z)].y_p = False

        # Try in:
        if( (x,y,z+1) in cubes ):
            cubes[(x,y,z+1)].z_m = False
        # Try out:
        if( (x,y,z-1) in cubes ):
            cubes[(x,y,z-1)].z_p = False

    total_open_sides = 0
    for cube in cubes:
        open_sides = 0
        if(cubes[cube].x_p == True):
            open_sides += 1
        if(cubes[cube].x_m == True):
            open_sides += 1
        if(cubes[cube].y_p == True):
            open_sides += 1
        if(cubes[cube].y_m == True):
            open_sides += 1
        if(cubes[cube].z_p == True):
            open_sides += 1
        if(cubes[cube].z_m == True):
            open_sides += 1
        cubes[cube].open_sides = open_sides
        total_open_sides += open_sides
        
    return total_open_sides

testcase = False
if testcase:
    file = "test.txt"
else:
    file = "input.txt"

with open(file, "r") as stuff:
    lines = stuff.read().splitlines()

    cubes = {}
    
    # Find extents
    maxx = -1
    maxy = -1
    maxz = -1
    minx = -1
    miny = -1
    minz = -1 
    for line in lines:
        (sx,sy,sz) = line.split(",")
        x = int(sx)
        y = int(sy)
        z = int(sz)
        cubes[(x,y,z)] = Cube(x,y,z)
        if(x > maxx):
            maxx = x
        if(minx == -1 or x < minx):
            minx = x
        if(y > maxy):
            maxy = y
        if(miny == -1 or y < miny):
            miny = y
        if(z > maxz):
            maxz = z
        if(minz == -1 or z < minz):
            minz = z

    ## hhmm.. things don't add up.  There may be "pockets" of air on the surface of our "cube"
    ## Expand the extents to surround the whole thing by air.  (That wasn't the problem)
    extents = (minx,miny,minz,maxx,maxy,maxz)
    print("Num cubes:",len(cubes))

    total_open_sides = Check_Sides(cubes)

    print("Rnd1 Total Open Sides:",total_open_sides)

    total_space = ((maxx - minx + 1) * (maxy - miny + 1) * (maxz - minz + 1))
    print("Space:", total_space )

    # Rnd2 consider the possibility of a cube completely surrounded by air inside a pocket.

    # Let's recursively try to fill everything with water/steam.
    air = {}
    FillAir(air,cubes,minx,miny,minz,extents)

    print("Rnd2 Steam:",len(air))
    
    trapped = {}
    Find_Trapped_Air(air,cubes,trapped, extents)

    print("Rnd2 Trapped:", len(trapped))

    ## I think we need to go back and note for each cube which of it's surfaces are exposed
    #  Done
    # Print_Cube(1,2,2)

    total_open_sides = Explore_Trapped(cubes,trapped)
    print("Rnd2 Total Open:", total_open_sides)





