#!/usr/bin/env python3

import re

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

def Embiggen_and_Prep(lines):
    '''
    We could just add this to the original list, but I'd like to keep
    all of those test cases working separately for Rnd1
    '''
    big_list = []
    for i in range(len(lines)):
        # now we have to keep track of the original order
        big_list.append({'num': int(lines[i]) * 811589153,
                         'moved': False,
                         'order': i})
    return big_list


def Find_Next(big_list,next):
    '''
    Searching through the list for the next index to work on.
    There's probably a more efficient way, but 5000*10 isn't really that many
    especially since we'll average half that.
    '''
    for i in range(len(big_list)):
        if(big_list[i]['order'] == next):
            return i

def Big_Unmixer(big_list,rounds):
    '''
    The large numbers shouldn't matter too much since we're already using modulus
    operations.  However, we do have to keep searching for where the next number is to move
    as we can't rely on the index anymore for the original order.  Just keeping track of the
    new index won't work because other operations will shift them around.
    (Can probably ditch the 'order' T/F value.)
    '''

    list_len = len(big_list)
    for rnd in range(rounds):
        print("Round ",rnd+1,"... Fight!")
        next = 0  # next up in the sorting priority

        while(next < list_len):
            i = Find_Next(big_list,next)

            # Copy in our previous Unmix function, but replace 'i' increments with Find_Next
            val = big_list.pop(i)
            val['moved'] = True
            if(val['num'] > 0):

                # when we start skipping, remember the list is one shorter now.
                how_many = val['num'] % (list_len -1 )
                if(i + how_many < list_len -1 ):  # removed -1 
                    big_list.insert(i+how_many,val)
                elif(i + how_many == list_len -1):  
                    # wrap
                    big_list.insert(0,val)
                else:
                    big_list.insert( how_many + i - list_len + 1, val)

            elif(val['num'] < 0):
                how_many = abs(val['num']) % (list_len - 1)
                if(i - how_many > 0):
                    big_list.insert(i - how_many, val)
                    # i should increase
                elif(i - how_many == 0):  # the test case actually wraps this to the end
                    # wrap to end
                    big_list.append(val)
                else:
                    big_list.insert(i - how_many + list_len - 1, val)
            else:
                big_list.insert(i,val)

            next += 1

testcase = False
if testcase:
    file = "test.txt"
    num_rounds = 10
else:
    file = "input.txt"
    num_rounds = 10

with open(file, "r") as stuff:
    lines = stuff.read().splitlines()
    the_list = Unmix(lines)
    print("Rnd1:",Coordinates(the_list))

    ## Rnd2
    big_list = Embiggen_and_Prep(lines)

#    Big_Unmixer(big_list, num_rounds)
    Big_Unmixer(big_list, num_rounds)

    print("Rnd2 Coordinates:",Coordinates(big_list))


