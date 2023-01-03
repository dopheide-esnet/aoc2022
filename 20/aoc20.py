#!/usr/bin/env python3

import re

testcase = False
if testcase:
    file = "test2.txt"
else:
    file = "input.txt"

def Unmix(lines):
    the_list = []
    for line in lines:
        the_list.append({'num': int(line), 'moved': False})

    # need to keep track of an index that may be shifting on me...
    i = 0
    list_len = len(the_list)
    while(i < len(the_list)):

#        print(the_list)

        # Being careful, the instructions say if you go off either end of the list you wrap
        # so if we would 'insert' at index 0, we instead add to the end and vice versa.
        # The test sample only shows this in one direction so we're assuming matching behavior

        # Still not sure about adding onto the end.

        # But none of that should really matter since we're checking for coordinates after
        # the position of the '0' value and it should all be relative.

        if(the_list[i]['moved'] == False):
            val = the_list.pop(i)
            val['moved'] = True
            if(val['num'] > 0):
                if(val['num'] == 20):
                    print("breakpoint")
                # when we start skipping, remember the list is one shorter now.
                how_many = val['num'] % (list_len -1 )
#                print("Move this many:",how_many)
                if(i + how_many < list_len -1 ):  # removed -1 
                    the_list.insert(i+how_many,val)
                    # i stays the same
                elif(i + how_many == list_len -1):  
                    # wrap
                    print("wrap to index 0")
                    the_list.insert(0,val)
#                    the_list.insert( how_many + i - list_len + 1, val)
#                    i += 1
                else:
                    the_list.insert( how_many + i - list_len + 1, val)
                    # i should increase
                    i += 1

            elif(val['num'] < 0):
                how_many = abs(val['num']) % (list_len - 1)
                if(i - how_many > 0):
                    the_list.insert(i - how_many, val)
                    # i should increase
                    i += 1
                elif(i - how_many == 0):  # the test case actually wraps this to the end
                    # wrap to end
                    the_list.append(val)
                    i += 1
                else:
                    the_list.insert(i - how_many + list_len - 1, val)
                    # i stays the same
#                print("move negative:",how_many)
            else:
                the_list.insert(i,val)
                i += 1
                # i should increase
        else:
            # moved == True
            # We've already handled this number, skip it.
            i += 1
        
    return the_list

def Coordinates(the_list):
    # could keep track of this during the loop, but I didn't so...
    for i in range(len(the_list)):
        if(the_list[i]['num'] == 0):
            zero_index = i
        if(the_list[i]['moved'] == False):
            print("whut")
            exit()

    # calculate grove coordinates
    r1 = (1000 + zero_index) % len(the_list)
    r2 = (2000 + zero_index) % len(the_list)
    r3 = (3000 + zero_index) % len(the_list)

    return the_list[r1]['num'] + the_list[r2]['num'] + the_list[r3]['num']

with open(file, "r") as stuff:
    lines = stuff.read().splitlines()
    the_list = Unmix(lines)

    print("Rnd1:",Coordinates(the_list))

#    print(the_list)
    # 1000th after the zero