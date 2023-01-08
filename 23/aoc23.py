#!/usr/bin/env python3

''' LOL, most of part one I forgot the Elves weren't the monkeys. Too late now. '''

import re
import pprint

class Monkey:
    def __init__(self,y,x):
        self.y = y
        self.x = x
        self.action = ""
        self.target = None

class Map:
    def __init__(self, x, y):
        self.minx = 0
        self.miny = 0
        self.maxx = x
        self.maxy = y

def PrintMap(map, monkeys):
    y = map.miny
    while(y <= map.maxy):
        x = map.minx
        while(x <= map.maxx):
            if((y,x) in monkeys):
                print("M",end="")
            else:
                print(".",end="")
                
            x += 1
        print("")
        y += 1    

def Get_Monkeys(lines):
    monkeys = {}
    y = 0
    for line in lines:
        chars = list(line)
        for x in range(len(chars)):
            if(line[x] == '#'):
                # Brass monkey, that funky monkey
                monkeys[(y,x)] = Monkey(y,x)
        y += 1
    map = Map(len(lines[0])-1,len(lines)-1)
    return (monkeys, map)

def Decision(mon,monkeys,directions):
    '''
    Check the directions we could move in reverse order.  Take the last path that's clear
    unless all directions are clear, then do nothing.  Also do nothing if all paths are blocked.

    We've also added tracking which space the monkey is targetting for movement.
    '''
    (y, x) = mon
    dir = ""
    all_clear = True
    target = None
    for d in reversed(range(len(directions))):
        # check directions in reverse order, last one that's 'clear' tasks prescendant
        # unless all directions are clear.
        if(directions[d] == 'north'):
            my = y - 1
            m = False
            for mx in [x-1,x,x+1]:
                if( (my,mx) in monkeys):
                    m = True
                    all_clear = False
            if(m == False):
                dir = 'north'
                target = (y-1,x)
        elif(directions[d] == 'south'):
            my = y + 1
            m = False
            for mx in [x-1,x,x+1]:
                if( (my,mx) in monkeys):
                    m = True
                    all_clear = False
            if(m == False):
                dir = 'south'
                target = (y+1,x)
        elif(directions[d] == 'west'):
            mx = x - 1
            m = False
            for my in [y-1,y,y+1]:
                if( (my,mx) in monkeys):
                    m = True
                    all_clear = False
            if(m == False):
                dir = 'west'
                target = (y,x-1)
        else:
            mx = x + 1
            m = False
            for my in [y-1,y,y+1]:
                if( (my,mx) in monkeys):
                    m = True
                    all_clear = False
            if(m == False):
                dir = 'east'
                target = (y,x+1)
    if(all_clear == True or dir == ''):
        return ['nothing', None]  # fake target, unused.
    else:
        if(dir == 'north'):
            monkeys[(y,x)].target = target
        elif(dir == 'south'):
            monkeys[(y,x)].target = target
        elif(dir == 'west'):
            monkeys[(y,x)].target = target
        else:
            monkeys[(y,x)].target = target

        return [dir, target]

def PrintMonkeys(monkeys):
    for mon in monkeys:
        print(mon, ":", monkeys[mon].action, monkeys[mon].target)


testcase = False
if testcase:
    file = "test.txt"
    rounds = 10
else:
    file = "input.txt"
    rounds = 10

with open(file, "r") as stuff:
    lines = stuff.read().splitlines()

    (monkeys, map) = Get_Monkeys(lines)

    directions = ['north', 'south', 'west', 'east']


    # Do Rounds   
    r = 1
#    while(r <= rounds):
    while(1):
        skip = []
        targets = {}

        if(r % 100 == 0):
            print("Round:",r)

        ######################
        ## First Half of Round
        for mon in monkeys:
            # nothing around me, do nothing.

            stuff = Decision(mon,monkeys,directions)  # [decision, (targety,targetx)]
            monkeys[mon].action = stuff[0]

            ## test_monkey_decisions() happens after this logic for all monkeys is done.

            if(stuff[0] == 'nothing'):
                skip.append(mon)  # we can skip this monkey in the second half
            else:
                # Decision time can also calculate where this monkey would want to go.
                # we can track a table of those and anyone else wanting to go there is refused,
                # plus the monkey that initiated it.
                if(stuff[1] not in targets):
                    targets[stuff[1]] = mon  # this is the first monkey trying to go here.
                else:
                    # target already exists, that's not an allowed action.
                    skip.append(mon)
                    monkeys[mon].action = 'blocked'
                    skip.append(targets[stuff[1]])   # the first monkey can't go there either.
                    monkeys[targets[stuff[1]]].action = 'blocked'

        if(len(skip) == len(monkeys)):
            print("Rnd2:",r)
            exit()

        #######################
        ## Second Half of Round
        for target in targets:

            # check map extents
            (y, x) = target
            if(y < map.miny):
                map.miny = y
            elif(y > map.maxy):
                map.maxy = y
            if(x < map.minx):
                map.minx = x
            elif(x > map.maxx):
                map.maxx = x

            mon = targets[target]
            if mon not in skip:
                monkeys[target] = monkeys[mon]
                del monkeys[mon]

        ###############
        ## End of Round
        r += 1
        # flip directions
        dir = directions.pop(0)
        directions.append(dir)

    PrintMap(map,monkeys)

    if(map.minx >= 0 or map.miny >= 0):
        print("Bad map assumption")
        exit()
    map_size = (map.maxx + abs(map.minx) + 1) * (map.maxy + abs(map.miny) + 1)
    empty = map_size - len(monkeys)
    print(map_size)
    print("Rnd1:",empty)

#    output = {}
#    for mon in monkeys:
#        output[mon] = vars(monkeys[mon])
    
#    print(output)




