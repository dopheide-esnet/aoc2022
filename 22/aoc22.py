#!/usr/bin/env python3

import regex  # needed for multiple captures

class Position:
    def __init__(self, x, y, facing):
        self.x = x
        self.y = y
        self.facing = facing

def PrintMap(map):
    for row in map:
        print("".join(row))

def Facing(map,pos,new):
    '''
    Update facing in position and in the map.
    '''
    faces = ['>','v','<','^']
    i = faces.index(pos.facing)
    if(new == 'R'):
        if(i == len(faces)-1):
            i = 0
        else:
            i += 1
    else:
        if(i == 0):
            i = len(faces) - 1
        else:
            i -= 1
    pos.facing = faces[i]
    map[pos.y][pos.x] = pos.facing
    return pos


def Process_Commands(map,commands,pos):
    '''
    Process movement commands, remember we wrap around.
    '''
    while(len(commands) > 0):
        command = commands.pop(0)
        if(command == 'R' or command == 'L'):
            pos = Facing(map,pos,command)
        else:
            # move
            print("Move:",command)



testcase = True
if testcase:
    file = "test.txt"
else:
    file = "input.txt"

with open(file, "r") as stuff:
    lines = stuff.read().splitlines()

    map = []
    for line in lines:
        if "." in line:
            level = list(line)
            map.append(level)
        elif(len(line) > 0):
            commands = line

    m = regex.match(r'((\d+)|[LR])+',commands)
    if(m):
        commands = m.captures(1)

dot = map[0].index('.')
position = Position(dot, 0, '>')
map[0][dot] = ">"

#PrintMap(map)

Process_Commands(map,commands,position)


# For final calculation, remember we're indexed at 0 this time.
