#!/usr/bin/env python3

import regex  # needed for multiple captures
import pprint

class Position:
    def __init__(self, x, y, facing, face):
        self.x = x
        self.y = y
        self.facing = facing
        self.face = face

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


def Process_Commands_Rnd1(map,commands,pos):
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

def Set_Orientation(faces,o,f,dir):
    '''
    We know how we got to each face and that helps define the orientation to the other faces
    '''
    # I'm only going to code the orientations we need for our current input.
    if(dir == 'down'):
        if(o == 1 and f == 4):
            faces[4]['orientation'] = 'up'
        elif(o == 4 and f == 6):
            faces[6]['orientation'] = 'up'  # even though it's on the bottom, that's how we'll think of it.
        else:
            print("We're missing",o,f)
    elif(dir == 'right'):
        if(o == 1 and f == 2):
            faces[2]['orientation'] = 'right'  # ie, it's laying on it's right side.
        elif(o == 6 and f == 2):
            faces[2]['orientation'] = 'left'
        else:
            print("We're missing",o,f)
    elif(dir == 'left'):
        if(o == 4 and f==5):
            faces[5]['orientation'] = 'up'            
        elif(o == 5 and f == 3):
            if(faces[5]['orientation'] == 'right'):
                faces[3]['orientation'] = 'right'
            else:
                faces[3]['orientation'] = 'up'
        elif(o == 6 and f == 5):
            faces[5]['orientation'] = 'right'
        else:
            print("We're missing",o,f, dir)


def Try_Right(faces,f,map, size):
    rights = {1: 2, 2: 3, 3: 5, 4: 2, 5: 4, 6: 2}

    if('origin' in faces[f] and faces[f]['origin'] == "right"):
        return False

    if(faces[f]['xx'] + 1 != len(map[faces[f]['oy']]) and map[faces[f]['oy']][faces[f]['xx'] + 1] != ' '):
        #print("There's face to the right")  # there has to be because we didn't pad with spaces
        if(rights[f] not in faces):
            faces[rights[f]] = {'ox': faces[f]['ox']+size, 'oy': faces[f]['oy'], 
                                'xx': faces[f]['xx']+size, 'xy': faces[f]['xy'], 'origin': 'left'}
            Set_Orientation(faces,f,rights[f],'right')
        faces[f]['right'] = rights[f]
        return True
    else:
        return False

def Try_Left(faces,f,map, size):
    lefts = {1: 5, 2: 4, 3: 2, 4: 5, 5: 3, 6: 5}

    if('origin' in faces[f] and faces[f]['origin'] == "left"):
        return False

#    print("face  face.ox",f,faces[f]['ox'], faces[f]['oy'], faces[f]['ox'] - size ,map[faces[f]['oy']][faces[f]['ox'] - size] )

    if(faces[f]['ox'] - size >= 0 and map[faces[f]['oy']][faces[f]['ox'] - size] != ' '):
#        print("here")
        if(lefts[f] not in faces):
            faces[lefts[f]] = {'ox': faces[f]['ox']-size, 'oy': faces[f]['oy'], 
                                'xx': faces[f]['xx']-size, 'xy': faces[f]['xy'], 'origin': 'right'}
            Set_Orientation(faces,f,lefts[f],'left')
        faces[f]['left'] = lefts[f]
#        print(faces[5])
        return True
    else:
        return False

def Try_Down(faces,f,map,size):
    downs = {1: 4, 2: 6, 3: 6, 4: 6, 5: 6, 6: 3}

    if('origin' in faces[f] and faces[f]['origin'] == "down"):
        return False

    if(faces[f]['xy'] + 1 != len(map) and map[faces[f]['xy'] + 1][faces[f]['xx']] != ' '):
        # down from 1 on a die is 4
        new_f = downs[f]
        if('orientation' in faces[f]):
            # the 'downs' table doesn't work if our orientation isn't 'up'
                if(faces[f]['orientation'] == 'right'):
                    lefts = {1: 5, 2: 4, 3: 2, 4: 5, 5: 3, 6: 5}
                    new_f = lefts[f]

        if(new_f not in faces):
            faces[new_f] = {'ox': faces[f]['ox'], 'oy': faces[f]['oy']+size, 
                            'xx': faces[f]['xx'], 'xy': faces[f]['xy']+size, 'origin': 'up'}
            if('orientation' in faces[f] and faces[f]['orientation'] == 'right'):
                Set_Orientation(faces,f,new_f,'left')
            else:
                Set_Orientation(faces,f,new_f,'down')
        faces[f]['down'] = new_f

        return True
    else:
        return False

def Cube_Next(faces, f, map, size):

    # stop when len(faces) == 6
    if(len(faces) == 6):
        return

    if(Try_Right(faces, f, map, size)):
        Cube_Next(faces, faces[f]['right'], map, size)

    if(Try_Down(faces, f, map, size)):
        Cube_Next(faces, faces[f]['down'], map, size)

    if(Try_Left(faces, f, map, size)):
        Cube_Next(faces, faces[f]['left'], map, size)

def Cube_Edges(map,size):
    '''
    Try to figure out which edges of the map fit together as a cube like a die
      /-----/|
     /  1  / |
    /_____/  |
    |     | 2/
    |  4  | /
    |_____|/    
    '''
    maxx = 0
    for i in range(len(map)):
        if(len(map[i]) > maxx):
            maxx = len(map[i])
    
    first_face = map[0].index('>') # index on our starting position
    
    where_factor = int(((first_face) / size))
    ox = 0 + where_factor * size
    oy = 0
    xx = ox + (size - 1)
    xy = oy + (size - 1)
    faces = {}
    faces[1] = {'ox': ox, 'oy': oy, 'xx': xx, 'xy': xy, 'origin': 'self', 'orientation': 'up'}  # need right, left, up, down faces

    # okay, we know there's no face to the left of face1
    # try right
    if(Try_Right(faces, 1, map, size)):
        Cube_Next(faces, faces[1]['right'], map, size)
    if(Try_Down(faces, 1, map, size)):
        Cube_Next(faces, faces[1]['down'], map, size)

    # At this point we have all of our faces figured out for a specific 
    # orientation where '1' is on top, 2,3,4,5 all 'stand' vertically
    # and 6 is on the bottom.

    # The tricky part now is figuring out the coordinate orientation of the edges.
    # (so you could argue the faces aren't standing vertically)
    # For instance, in both our input and the test input, going down from Face 1 you
    # end up directly at the top of Face 4.  However, right from Face 1 in our input
    # puts the 'top' of Face 2 on the y=0 to y=49 line.  In the test input, the top
    # of Face 2 is on the y=149 to y=99 line.

    return faces


def Process_Commands_Rnd2(faces, map,commands,pos):
    '''
    Process movement commands, remember we wrap around.

    My input shape condensed:
      1122
      1122
      44
      44
    5566
    5566
    33
    33
    '''
    downs = {1: 4, 2: 6, 3: 6, 4: 6, 5: 6, 6: 3}
    ups = {1: 3, 2: 1, 3: 1, 4: 1, 5: 1, 6: 4}
    rights = {1: 2, 2: 3, 3: 5, 4: 2, 5: 4, 6: 2}
    lefts = {1: 5, 2: 4, 3: 2, 4: 5, 5: 3, 6: 5}

    while(len(commands) > 0):
        command = commands.pop(0)
        if(command == 'R' or command == 'L'):
            pos = Facing(map,pos,command)
        else:
            command = int(command)
            # move
            steps = 1
            while(steps <= command):

# Okaaaay, for Rnd2 we can move normally until we hit the edge of our current face.
# So... track current face.  Added a face to the Position class.

# Given the test input, if we go right from Face 1, we hit Face 2 which is oriented left.
# There's a couple ways we might be able to do this, but I definitely want to keep drawing
# on the actual 2D map.

# First, let's figure out how to define the extents of our face to know if we need to wrap.
# (checking 'up' is now in scope unlike when defining out cube edges)
                face = pos.face 
                min_x_edge = faces[face]['ox']
                max_x_edge = faces[face]['xx']
                min_y_edge = faces[face]['oy']
                max_y_edge = faces[face]['xy']

                if(pos.facing == ">" or pos.facing == "<"):
                    if(pos.facing == ">"):
                        newx = pos.x + 1
                        newy = pos.y
                        new_face = pos.face

                        if(newx > max_x_edge):
                            print("Wrap right", face, pos.x, pos.y)

                            new_face = rights[face]
                            x_diff = pos.x - min_x_edge
                            y_diff = pos.y - min_y_edge

                            if(face == 1):
                                if(faces[face]['orientation'] == 'up' and
                                   faces[new_face]['orientation'] == 'left'):
                                    newx = faces[new_face]['xx']
                                    newy = faces[new_face]['xy'] - y_diff
                                    pos.facing = "<"
                                    exit()
                                elif(faces[face]['orientation'] == 'up' and
                                   faces[new_face]['orientation'] == 'right'):
                                    print("1 to 2")
                                    # nothing else changes
                                else:
                                    print("ugh3")
                                    exit()
                            elif(face == 4):
                                if(faces[face]['orientation'] == 'up' and
                                   faces[new_face]['orientation'] == 'left'):
                                    newx = faces[new_face]['xx'] - y_diff
                                    newy = faces[new_face]['oy']
                                    pos.facing = "v"
                                    print("4 to 2")
                                    print("Steps",steps)
                                elif(faces[face]['orientation'] == 'up' and
                                   faces[new_face]['orientation'] == 'right'):
                                   newx = faces[new_face]['ox'] + y_diff
                                   newy = faces[new_face]['xy'] 
                                   pos.facing = '^'
                                else:
                                    print("ugh4")
                                    exit()
                            elif(face == 2):
                                if(faces[face]['orientation'] == 'left'):
                                    new_face = 1
                                    newx = faces[new_face]['xx']
                                    newy = faces[new_face]['xy'] - y_diff
                                    pos.facing = "<"
                                elif(faces[face]['orientation'] == 'right'):
                                    new_face = 6
                                    newx = faces[new_face]['xx']
                                    newy = faces[new_face]['xy'] - y_diff
                                    pos.facing = '<'
                                   
                            elif(face == 6):
                                if (faces[face]['orientation'] == 'up' and
                                    faces[new_face]['orientation'] == 'left'):
                                    newx = faces[new_face]['ox']
                                    # newy stays the same
                                    # pos.facing stays the same
                                elif (faces[face]['orientation'] == 'up' and
                                    faces[new_face]['orientation'] == 'right'):
                                    newx = faces[new_face]['xx']
                                    newy = faces[new_face]['xy'] - y_diff
                                    pos.facing = '<'
                                    # this changed recently..
                                else:
                                    print("ugh5")
                                    exit()
                            else:
                                if (faces[face]['orientation'] == 'up' and
                                    faces[new_face]['orientation'] == 'up'):
                                    print("nothing happens")
                                elif(face == 3) and (faces[face]['orientation'] == 'right'):
                                    new_face = 6
                                    newx = faces[new_face]['ox'] + y_diff
                                    newy = faces[new_face]['xy']
                                    pos.facing = '^'
                                elif(face == 5) and (faces[face]['orientation'] == 'right'):
                                    new_face = 6
                                    # nothing else changes
                                else:
                                    print("ugh6", face)
                                    exit()

                        # check for wall, spaces are no longer an issue
                        if(map[newy][newx] == '#'):
                            pos.facing = ">"
                            break
                        else:
                            # set new face and new position.
                            pos.face = new_face
                            pos.y = newy
                            pos.x = newx
                            map[pos.y][pos.x] = pos.facing
                                

                    elif(pos.facing == "<"):
                        newx = pos.x - 1
                        newy = pos.y
                        new_face = pos.face

                        # wrap
                        if(newx < min_x_edge):
                            print("Wrap Left", face, pos.x, pos.y, command)
                            new_face = lefts[face]
                            x_diff = pos.x - min_x_edge
                            y_diff = pos.y - min_y_edge

                            if(face == 1):
                                if(faces[face]['orientation'] == 'up' and
                                   faces[new_face]['orientation'] == 'up'):
                                   newx = faces[new_face]['ox']+y_diff
                                   newy = faces[new_face]['oy']
                                   pos.facing = "v"
                                   print("1 to 5")
                                   exit()
                                elif(faces[face]['orientation'] == 'up' and
                                   faces[new_face]['orientation'] == 'right'):
                                   newx = faces[new_face]['ox']
                                   newy = faces[new_face]['xy']-y_diff
                                   pos.facing = '>'

                            elif(face == 2):
                                if(faces[2]['orientation'] == 'left'):
                                    new_face = 6
                                    newx = faces[new_face]['xx']
                                    # newy doesn't change
                                    # pos.facing doesn't change
                                elif(faces[2]['orientation'] == 'right'):
                                    new_face = 1
                                    if(faces[new_face]['orientation']=='up'):
                                        print("2 to 1, do nothing else")
                                else:
                                    print("regular 2")
                                    exit()
                            elif(face == 3):
                                if(faces[face]['orientation'] == 'up' and
                                   faces[new_face]['orientation'] == 'left'):
                                    newx = faces[new_face]['xx'] - y_diff
                                    newy = faces[new_face]['oy']
                                    pos.facing = '^'
                                    print("3 to 2")
                                    exit()
                                elif(faces[face]['orientation'] == 'right'):
                                    new_face = 1
                                    newx = faces[new_face]['ox'] + y_diff
                                    newy = faces[new_face]['oy']
                                    pos.facing = "v"

                            elif(face == 4 or face == 5) and (faces[face]['orientation'] == 'up' and
                                   faces[new_face]['orientation'] == 'left'):
                                print("4 to 5 or 5 to 3")
                            elif(face == 4 and faces[face]['orientation'] == 'up'):
                                if(faces[new_face]['orientation'] == 'right'):
                                    newx = faces[new_face]['ox'] + y_diff
                                    newy = faces[new_face]['oy']
                                    pos.facing = 'v'
                            elif(face == 5 and faces[face]['orientation'] == 'right'):
                                new_face = 1
                                newx = faces[new_face]['ox']
                                newy = faces[new_face]['xy'] - y_diff
                                pos.facing = ">"
                            elif(face == 6) and (faces[face]['orientation'] == 'up' and
                                   faces[new_face]['orientation'] == 'up'):
                                newx = faces[new_face]['xx'] - y_diff
                                newy = faces[new_face]['xy']
                                pos.facing = '^'
                                print("6 to 5")
                                exit()
                            elif(face == 6) and (faces[face]['orientation'] == 'up' and
                                   faces[new_face]['orientation'] == 'right'):
                                newx = faces[new_face]['xx']
                                newy = faces[new_face]['oy']+y_diff
                                pos.facing = "<"
                            else:
                                print("ugh face",face)
                                exit()

                    # check for wall, spaces are no longer an issue
                    if(map[newy][newx] == '#'):
                        pos.facing = "<"
                        break
                    else:
                        # set new face and new position.
                        pos.face = new_face
                        pos.y = newy
                        pos.x = newx
                        map[pos.y][pos.x] = pos.facing

                else:
                    if(pos.facing == "v"):
                        newy = pos.y + 1
                        newx = pos.x
                        new_face = pos.face
                        #wrap

                        if(newy > max_y_edge):
                            print("Wrap Down", face, pos.x, pos.y, command)
                            new_face = downs[face]

#                            1 to 4 or 4 to 6 no changes in test case
                            if(face == 1 or face == 4) and (faces[face]['orientation'] == 'up' and 
                                faces[new_face]['orientation'] == 'up'):
                                    print("1 to 4 or 4 to 6")

                            elif(face == 3):  # 3 to 6

                                if(faces[face]['orientation'] == 'up' and 
                                    faces[new_face]['orientation'] == 'up'):
                                    # 3 down becomes 6 up reversed
                                    x_diff = pos.x - min_x_edge
                                    y_diff = pos.y - min_y_edge
                                    newx = faces[new_face]['xx'] - x_diff
                                    newy = faces[new_face]['xy']
                                    print("3 to 6", pos.x, pos.y, newx, newy)
                                    pos.facing = "^"  # new facing
                                    exit()
                                elif(faces[face]['orientation'] == 'right'):
                                    new_face = 2
                                    if(faces[new_face]['orientation'] == 'right'):
                                    # down from 3 on it's right is 2 (which is also on it's right in our input)

                                        x_diff = pos.x - min_x_edge
                                        y_diff = pos.y - min_y_edge

                                        newx = faces[new_face]['ox'] + x_diff
                                        newy = faces[new_face]['oy']
                                        pos.facing="v"  # still down
                                    
                                else:
                                    print("here, newface",face, new_face)
                                    print("ugh") 
                                    exit()
                            elif(face == 5):  # 5 to 6
                                if(faces[face]['orientation'] == 'up' and 
                                    faces[new_face]['orientation'] == 'up'):    
                                    x_diff = pos.x - min_x_edge
                                    y_diff = pos.y - min_y_edge
                                    newx = faces[new_face]['xx'] - x_diff
                                    newy = faces[new_face]['xy']
                                    pos.facing = ">"
                                    print("5 to 6", pos.x, pos.y, newx, newy)
                                    exit()          
                                elif(faces[face]['orientation'] == 'right'):
                                    new_face = 3

                                else:
                                    print("ugh2")
                                    exit()
                            elif(face == 6):   # 6 to 3
                                if(faces[face]['orientation'] == 'up' and 
                                    faces[new_face]['orientation'] == 'up'):
                                    x_diff = pos.x - min_x_edge
                                    y_diff = pos.y - min_y_edge
                                    newy = faces[new_face]['xy']
                                    newx = faces[new_face]['xx'] - x_diff
                                    pos.facing = '^'
                                    print("6 to 3")
                                    print("x_dff",x_diff)
                                    print("steps",steps, new_face)
                                elif(faces[face]['orientation'] == 'up' and 
                                    faces[new_face]['orientation'] == 'right'):
                                    x_diff = pos.x - min_x_edge
                                    y_diff = pos.y - min_y_edge
                                    newy = faces[new_face]['oy'] + x_diff
                                    newx = faces[new_face]['xx']
                                    pos.facing = '<'

                                else:
                                    print("ugh7")
                                    exit()

                            elif(face == 2):
                                if(faces[face]['orientation'] == 'right'):
                                    new_face = 4
                                    if(faces[new_face]['orientation'] == 'up'):
                                        x_diff = pos.x - min_x_edge
                                        y_diff = pos.y - min_y_edge
                                        newx = faces[new_face]['xx']
                                        newy = faces[new_face]['oy'] + x_diff
                                        pos.facing = '<'
                            else:
#                                PrintMap(map)
                                print("We still need down from 6 and 2, 2 is going to change new_face)")
                                exit()                        
                        # check for wall, spaces are no longer an issue
                        if(map[newy][newx] == '#'):
                            pos.facing = "v"
                            break
                        else:
                            # set new face and new position.
                            pos.face = new_face
                            pos.y = newy
                            pos.x = newx
                            map[pos.y][pos.x] = pos.facing


                    elif(pos.facing == "^"):
                        newy = pos.y - 1
                        newx = pos.x
                        new_face = pos.face
                        #wrap

                        if(newy < min_y_edge):
                            print("Wrap Up", face, pos.x, pos.y, command)
                            new_face = ups[face]
                            x_diff = pos.x - min_x_edge
                            y_diff = pos.y - min_y_edge

                            if(face == 4 or face == 6) and (faces[face]['orientation'] == 'up' and 
                                faces[new_face]['orientation'] == 'up'):
                                print("6 to 4 or 4 to 1")

                            elif(face == 1):
                                if(faces[face]['orientation'] == 'up' and 
                                faces[new_face]['orientation'] == 'up'):
                                    newx = faces[new_face]['xx'] - x_diff
                                    newy = faces[new_face]['xy']
                                    pos.facing = "v"
                                elif(faces[face]['orientation'] == 'up' and 
                                faces[new_face]['orientation'] == 'right'):
                                    newx = faces[new_face]['ox']
                                    newy = faces[new_face]['oy'] + x_diff
                                    pos.facing = '>'
                                else:
                                    print(new_face)
                                    print("ugh9")
                                    exit()
                            
                            elif(face == 2):  # special case
                                if(faces[face]['orientation'] == 'left'):
                                    new_face = 4
                                    if(faces[new_face]['orientation'] == 'up'):
                                        newx = faces[new_face]['xx']
                                        newy = faces[new_face]['xy'] - x_diff
                                        pos.facing = "<"
                                elif(faces[face]['orientation'] == 'right'):
                                    new_face = 3
                                    newx = faces[new_face]['ox'] + x_diff
                                    newy = faces[new_face]['xy']
                                    #pos.facing doesn't change

                                else:
                                    print("ugh10 need 2 up orientation (or right?)")                            

                            elif(face == 3):
                                if(faces[face]['orientation'] == 'up' and 
                                faces[new_face]['orientation'] == 'up'):
                                    newx = faces[new_face]['xx'] - x_diff
                                    newy = faces[new_face]['oy']
                                    pos.facing = "v"
                                elif(faces[face]['orientation'] == 'right'):
                                    new_face = 5
                                    # no other changes
                                else:
                                    print("ugh11") 

                            elif(face == 5):
                                if(faces[face]['orientation'] == 'up' and 
                                faces[new_face]['orientation'] == 'up'):
                                    newx = faces[new_face]['ox']
                                    newy = faces[new_face]['oy'] + x_diff
                                    pos.facing = ">"
                                elif(faces[face]['orientation'] == 'right'):
                                    new_face = 4
                                    newx = faces[new_face]['ox']
                                    newy = faces[new_face]['oy'] + x_diff
                                    pos.facing = ">"

                                else:
                                    print("ugh12") 
                                    exit()

                            else:
                                print("missing some stuff with up")
                                exit()
#                            PrintMap(map)
#                            input("continue?")
                        # check for wall, spaces are no longer an issue
                        if(map[newy][newx] == '#'):
                            pos.facing = '^'
                            break
                        else:
                            # set new face and new position.
                            pos.face = new_face
                            pos.y = newy
                            pos.x = newx
                            map[pos.y][pos.x] = pos.facing

                steps += 1
    return pos



testcase = False
if testcase:
    file = "test.txt"
    cube_size = 4
else:
    file = "input.txt"
    cube_size = 50

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
position = Position(dot, 0, '>', 1)
map[0][dot] = ">"
PadMap(map)


# Rnd2
# Need to figure out how our cube folds.
# The input is simple enough we could just define it, but that's cheating.
faces = Cube_Edges(map,cube_size)
# I should have cheated and just input the data.

pprint.pprint(faces)
pos = Process_Commands_Rnd2(faces, map,commands,position)

# For final calculation, remember we're indexed at 0 this time.
facing_math = [0,1,2,3]
facing = ['>','v','<','^']



print("Rnd2:",(pos.y+1)*1000+((pos.x+1) * 4)+facing_math[facing.index(pos.facing)])

#PrintMap(map)

