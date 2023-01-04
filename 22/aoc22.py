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

def PadMap(map):
    '''
    For shorter map lines, we need to pad them to max length with spaces so that
    our path wrapping works correctly.
    '''
    maxx = 0
    for i in range(len(map)):
        if(len(map[i]) > maxx):
            maxx = len(map[i])
    for i in range(len(map)):
        if(len(map[i]) < maxx):
            space = " " * (maxx - len(map[i]))
            map[i].extend(list(space))

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

def SkipSpaces(map,pos):
    spaces = 1
    y = pos.y
    x = pos.x
    print("x:",x)
    while(1):
        if(pos.facing == ">" or pos.facing == "<"):
            if(pos.facing == ">"):
                newx = x + spaces
                # wrap
                if(newx == len(map[pos.y])):
                    newx = 0      
                    x = 0
                    spaces = 1       
            elif(pos.facing == "<"):
                newx = x - spaces
                # wrap
                if(newx == -1):
                    newx = len(map[pos.y]) - 1
                    x = newx
                    spaces = 0
#            print("newx",newx)
            if(map[pos.y][newx] != ' '):
                return newx
        else:
            if(pos.facing == "v"):
                newy = y + spaces
                #wrap
                if(newy == len(map)):
                    newy = 0
                    y = 0
                    spaces = 1
            elif(pos.facing == "^"):
                newy = y - spaces
                #wrap
                if(newy == -1):
                    newy = len(map) - 1
                    y = newy
                    spaces = 0
            if(map[newy][pos.x] != ' '):
                return newy
        spaces += 1


def Process_Commands(map,commands,pos):
    '''
    Process movement commands, remember we wrap around.
    '''
    while(len(commands) > 0):
        command = commands.pop(0)
        if(command == 'R' or command == 'L'):
            pos = Facing(map,pos,command)
        else:
            command = int(command)
            # move
            steps = 1
            while(steps <= command):

                if(pos.facing == ">" or pos.facing == "<"):
                    if(pos.facing == ">"):
                        newx = pos.x + 1
                        # wrap
                        if(newx == len(map[pos.y])):
                            newx = 0                
                    elif(pos.facing == "<"):
                        newx = pos.x - 1
                        # wrap
                        if(newx == -1):
                            newx = len(map[pos.y]) - 1

                    if(map[pos.y][newx] == ' '):
                        print("newx",newx)
                        newx = SkipSpaces(map,pos)
                        print("after",newx)

                    if(map[pos.y][newx] in ['.','>','v','<','^']):
                        pos.x = newx
                        map[pos.y][pos.x] = pos.facing
                    elif(map[pos.y][newx] == '#'):
                        break

                else:
                    if(pos.facing == "v"):
                        newy = pos.y + 1
                        #wrap
                        if(newy == len(map)):
                            newy = 0
                    elif(pos.facing == "^"):
                        newy = pos.y - 1
                        #wrap
                        if(newy == -1):
                            newy = len(map) - 1

                    if(map[newy][pos.x] == ' '):
                        newy = SkipSpaces(map,pos)
                    
                    if(map[newy][pos.x] in ['.','>','v','<','^']):
                        pos.y = newy
                        map[pos.y][pos.x] = pos.facing
                    elif(map[newy][pos.x] == '#'):
                        break

                steps += 1
    return pos


testcase = False
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

PadMap(map)
#print(commands)
pos = Process_Commands(map,commands,position)

# For final calculation, remember we're indexed at 0 this time.
facing_math = [0,1,2,3]
facing = ['>','v','<','^']
print("Rnd1:",(pos.y+1)*1000+((pos.x+1) * 4)+facing_math[facing.index(pos.facing)])

PrintMap(map)

