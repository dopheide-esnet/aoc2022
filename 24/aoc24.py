#!/usr/bin/env python3

import copy

def BuildMap(lines):
    '''
    Build map from the input.  Each map location is a list of things that are there.
    Choices are '#' border, '.' empty, 'E' expedition, or any number of blizzards.
    The key is that we need to allow multiple blizzards in different directions to overlap.
    '''
    map = []
    for y in range(len(lines)):
        map.append(list())
        chars = list(lines[y])
        for x in range(len(chars)):
            map[y].append( list(chars[x] ))
    return map

def PrintMap(e,map):
    (ey,ex) = e
    for y in range(len(map)):
        for x in range(len(map[y])):
            if(y == ey and x == ex):
                print('E',end='')
            elif(len(map[y][x]) == 1):
                print(map[y][x][0],end='')
            else:
                print(len(map[y][x]),end='')
        print()

def Blizzards(map):
    '''
    Determine all of the blizzards' new positions.  A little tricky because we only want to move
    each blizzard once.  Maybe try writing them to a new map.
    '''

    # build new empty map (there's gotta be a better way)
    new_map = []
    for y in range(len(map)):
        new_map.append(list())
        for x in range(len(map[y])):
            new_map[y].append(list())

    # Can ignore the map border, but it's easier to just copy them.
    for y in range(len(map)):
        for x in range(len(map[y])):
            if(map[y][x][0] != '.' and map[y][x][0] != '#'):

#                while(len(map[y][x]) > 0):
#                    bliz = map[y][x].pop()
                for i in range(len(map[y][x])):
                    bliz = map[y][x][i]
                    if(bliz == '<'):
                        # check for edge
                        if(x - 1 == 0):
                            new_map[y][len(map[y])-2].append(bliz)
                        else:
                            new_map[y][x-1].append(bliz)
                    elif(bliz == '>'):
                        if(x + 1 == len(map[y])-1):
                            new_map[y][1].append(bliz)
                        else:
                            new_map[y][x+1].append(bliz)
                    elif(bliz == '^'):
                        if(y - 1 == 0):
                            new_map[len(map)-2][x].append(bliz)
                        else:
                            new_map[y-1][x].append(bliz)
                    elif(bliz == 'v'):
                        if(y + 1 == len(map) - 1):
                            new_map[1][x].append(bliz)
                        else:
                            new_map[y+1][x].append(bliz)

            elif(map[y][x][0] != '.'):
                new_map[y][x] = map[y][x]

    # need to populate now empty spots with '.'
    for y in range(len(new_map)):
        for x in range(len(new_map[y])):
            if(len(new_map[y][x]) == 0):
                new_map[y][x].append('.')

    return new_map

def Search_Moves(e, map):
    '''
    options are stay, up, down, left, right
    keep in mind a blizzard may move to where we are now.
    if there are no options, staying may not be one either ending this path.
    '''
    (y, x) = e

    options = []

    if(y < len(map)-1):
        if(map[y+1][x][0] == '.'):
            options.append('down')

    if(map[y][x+1][0] == '.'):
        options.append('right')
    if(map[y][x-1][0] == '.'):
        options.append('left')

#    if(map[y-1][x][0] == '.' and y>1):  # don't move up from home
    if(map[y-1][x][0] == '.'):
        options.append('up')
    #do 'stay' last, it's the least likely to help in the long run.
    if(map[y][x][0] == '.'):
        options.append('stay')

    return options

def Move(map,cycles,positions,never, goal):
    '''
    TODO: optimization, if clock > any successful return count, end that attempt

    Assumption, it appears we're allowed to move 'through' a blizzard as long as
    we don't end up in the same space.
    '''

#    if(len(options) == 0):
#        print("Dead End")
#        return -1

#    if(clock > 20):
#        print("Max clock reached")
#        return -1

    clock = max(cycles.keys())
    new_map = Blizzards(map)
    clock += 1
    cycles[clock] = list()
    for e in cycles[clock-1]:

        options = Search_Moves(e, new_map)
        (y, x) = e
        min_ret = 0
        for op in options:

            if(op == 'down'):
                e = (y+1,x)
            elif(op == 'left'):
                e = (y,x-1)
            elif(op == 'right'):
                e = (y,x+1)
            elif(op == 'up'):
                e = (y-1,x)
            elif(op == 'stay'):
                e = (y,x)

            if(e not in never):
                if(e not in positions):
                    positions[e]=list()
                positions[e].append(clock)
                if(e not in cycles[clock]):
                    cycles[clock].append(e)

            if(e == goal):
                print("Found the End!",clock)
                return {'map': new_map, 'res': True}

    return {'map': new_map, 'res': False}


testcase = False
if testcase:
    file = "test.txt"
else:
    file = "input.txt"

with open(file, "r") as stuff:
    lines = stuff.read().splitlines()

map = BuildMap(lines)

# don't add the 'E' to the actual data structure, it's annoying to deal with.
#map[0][1][0] = 'E'  # not that it really matters, but our input doesn't have this

e = (0,1) # expedition starting location

# map = Blizzards(map)

# Things are working now I think, but real slow. I think if we keep track of where we've been
# we can start to eliminate edge cases of returning to the same spot over and over.

# This is taking FOREVER.

# Change to breadth-first search.

# only really need to keep the last one, but it might be useful for debugging to have them
# all for now.
cycles = {}          # dict of clock cycles and every position we are in at that time.
cycles[0] = list()
cycles[0].append(e)   

positions = {}    # dict of positions
positions[e] = list()
positions[e] = [0]

never_going_back_again = []
goal = (len(map)-1,len(map[0])-2)

while(1):

    r = Move(map, cycles, positions, never_going_back_again, goal)
    map = r['map']
    if(r['res'] == True):
        break

    # Cleanup
    clock = max(cycles.keys())
    killlist = []

    ### change this to a never go here again list and put it up in Move()
    for e in cycles[clock]:
        if(len(positions[e]) > 10):
            killlist.append(e)
            if(e not in never_going_back_again):
                never_going_back_again.append(e)
    for e in killlist:
        i = cycles[clock].index(e)
        cycles[clock].pop(i)

if(r['res'] == False):
    print("oops")
    exit()
#print(cycles)
#print(positions)
print("Rnd1:",max(cycles.keys()))

# For Rnd2 I'm just gonna copy some code cause I'm tired of this day.

e = (len(map)-1, len(map[0])-2)    
clock = max(cycles.keys())
cycles = {}
cycles[clock] = list()   # reset cycles
cycles[clock].append(e)

positions = {}    # dict of positions
positions[e] = list()
positions[e] = [0]

never_going_back_again = []
goal = (0,1)

while(1):
#for i in range(35):
    r = Move(map, cycles, positions, never_going_back_again, goal)
    map = r['map']
    if(r['res'] == True):
        break

    # Cleanup
    clock = max(cycles.keys())
    killlist = []

    for e in cycles[clock]:
        if(len(positions[e]) > 20):  # had to adjust this
            killlist.append(e)
            if(e not in never_going_back_again):
                never_going_back_again.append(e)
    for e in killlist:
        i = cycles[clock].index(e)
        cycles[clock].pop(i)

if(r['res'] == False):
    print("oops")
    exit()


e = (0,1)    
clock = max(cycles.keys())
cycles = {}
cycles[clock] = list()   # reset cycles
cycles[clock].append(e)

positions = {}    # dict of positions
positions[e] = list()
positions[e] = [0]

never_going_back_again = []
goal = (len(map)-1, len(map[0])-2) 

while(1):
#for i in range(35):
    r = Move(map, cycles, positions, never_going_back_again, goal)
    map = r['map']
    if(r['res'] == True):
        break

    # Cleanup
    clock = max(cycles.keys())
    killlist = []

    for e in cycles[clock]:
        if(len(positions[e]) > 20):  # had to adjust this
            killlist.append(e)
            if(e not in never_going_back_again):
                never_going_back_again.append(e)
    for e in killlist:
        i = cycles[clock].index(e)
        cycles[clock].pop(i)

if(r['res'] == False):
    print("oops")
    exit()




print("Rnd2:",max(cycles.keys()))





