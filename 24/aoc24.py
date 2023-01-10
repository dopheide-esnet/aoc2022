#!/usr/bin/env python3

import re
import pprint


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

def PrintMap(map):
    for y in range(len(map)):
        for x in range(len(map[y])):
            if(len(map[y][x]) == 1):
                print(map[y][x][0],end='')
            else:
                print(len(map[y][x]),end='')
        print()

def Blizzards(map):
    '''
    Determine all of the blizzards' new positions.  A little tricky because we only want to move
    each blizzard once.  Maybe try writing them to a new map.

    TODO: Potential improvement if cpu time becomes an issue.  In exchange for memory we can store the
    map at any given minute so we don't have to recursively recalculate the same minute over and over.
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
                while(len(map[y][x]) > 0):
                    bliz = map[y][x].pop()
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
    (y, x) = e

    # verify extents

    options = []

    print("HERE")
    # need to check extents, but also we're missing some '.'s in the map.
    # where'd they go.

    if(y < len(map)-1):
        if(map[y+1][x][0] == '.'):
            options.append('down')

    if(map[y][x+1][0] == '.'):
        options.append('right')
    if(map[y][x-1][0] == '.'):
        options.append('left')
    if(map[y-1][x][0] == '.'):
        options.append('up')
    #do 'stay' last, it's the least likely to help in the long run.
    if(map[y][x][0] == '.'):
        options.append('stay')

    return options


def Move(e,map,clock):
    '''
    
    TODO: optimization, if clock > any successful return count, end that attempt
    '''
    # options are stay, up, down, left right
    # keep in mind a blizzard may move to where we are now.
    # if there are no options, staying may not be one either ending this path.
    options = Search_Moves(e, map)

    if(len(options) == 0):
        "Dead End"
        return -1

    if(clock > 20):
        print("Max clock reached")
        return -1

    new_map = Blizzards(map) # this is the new blizzard positions at clock + 1
    clock += 1

    (y, x) = e
    min_ret = 0
    for op in options:
        print("do:",op)
        if(op == 'down'):
            e = (y+1,x)
            if(e == (len(map)-1,len(map[0])-2)):
                print("Found the End!",clock-1)
                ret = clock - 1
            else:
                ret = Move(e,new_map,clock)
                if(min_ret == 0):
                    min_ret = ret
                elif(ret < min_ret and ret != -1):
                    min_ret = ret
        if(op == 'left'):
            e = (y,x-1)
            ret = Move(e,new_map,clock)
            if(min_ret == 0):
                min_ret = ret
            elif(ret < min_ret and ret != -1):
                min_ret = ret
        if(op == 'right'):
            e = (y,x-1)
            ret = Move(e,new_map,clock)
            if(min_ret == 0):
                min_ret = ret
            elif(ret < min_ret and ret != -1):
                min_ret = ret            
        if(op == 'up'):
            e = (y-1,x)
            ret = Move(e,new_map,clock)
            if(min_ret == 0):
                min_ret = ret
            elif(ret < min_ret and ret != -1):
                min_ret = ret
        if(op == 'stay'):
            # need to do something to prevent the loop where it stays at home forever.
            if(clock < 10 and e == (0,1)):
                print("skip stay at home")
            else:
                ret = Move(e,new_map,clock)
                if(min_ret == 0):
                    min_ret = ret
                elif(ret < min_ret and ret != -1):
                    min_ret = ret
    return min_ret

testcase = True
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

map = Blizzards(map)
minimum = Move(e, map,1) # map, minute
print("Rnd1:",minimum)

# determine next blizzard positions, we can't stop that from happening.
# since blizzards can overlap and we still have to know where each is headed
# either each map location has to track that or we have to track each individual
# blizzard and generate the map from there.
# I think having that info embedded in the map will make it easier to move the expedition around.
#map = Blizzards(map)


# then see what our options are.







