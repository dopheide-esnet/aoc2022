#!/usr/bin/env python3

import re
import copy

class Rock:
    def __init__(self, shape, x, y):
        self.width = len(shape[0])
        self.height = len(shape)
        self.x = x
        self.y = y
        self.shape = copy.copy(shape)

def Check_Path_Left(rock, fuck_shit_stack, c_width):  # Reggie Watts reference
#    print("check left")
    result = True
    y = rock.y

    if(rock.x == 1):
        # up against the left edge already
        result = False
    elif y <= len(fuck_shit_stack):
        # We're lower than the top of the stack
        rock_edge = []
        stack_x = rock.x - 2  # -1 for index, -1 for position
        for i in range(len(rock.shape)):
            rock_edge.append(rock.shape[i][0])
        
#        print("Rock Edge:",rock_edge, y)
        row = len(rock_edge) - 1
        while(y <= len(fuck_shit_stack)):
#            print("Comp", rock_edge[row], stack[y-1][stack_x])
            if(rock_edge[row]) == '#' and fuck_shit_stack[y-1][stack_x] == '#':
                result = False
            elif(rock_edge[row] == '.'):
                # check further
                j = 0
                while(rock.shape[row][j] == '.' and j < len(rock.shape[0])):
                    next_edge = rock.shape[row][j+1]
                    if(next_edge == "#" and fuck_shit_stack[y-1][stack_x+j+1] == "#"):
                        result = False
                    j += 1

            row -= 1
            y += 1
            if(row < 0):
                break

    return result

def Check_Path_Right(rock, fuck_shit_stack, c_width):  # Reggie Watts reference
#    print("check right")
    result = True
    y = rock.y

    if(rock.x + rock.width - 1) == c_width:
        # up against the right edge already
        result = False
    elif y <= len(fuck_shit_stack):
        # We're lower than the top of the stack
        rock_edge = []
        stack_x = rock.x + rock.width - 1
        for i in range(len(rock.shape)):
            rock_edge.append(rock.shape[i][rock.width - 1])
        
        row = len(rock_edge) - 1
        while(y <= len(fuck_shit_stack)):
            if(rock_edge[row]) == '#' and fuck_shit_stack[y-1][stack_x] == '#':
                result = False

            elif(rock_edge[row] == '.'):
                # check further
                # this bit for moving right is not thoroughly tested
                j = 0
                while(rock.shape[row][j] == '.' and j < len(rock.shape[0])):
                    next_edge = rock.shape[row][rock.width - j - 2]
                    if(next_edge == "#" and fuck_shit_stack[y-1][stack_x-j-1] == "#"):
                        result = False
                    j += 1


            row -= 1
            y += 1

            if(row < 0):
                break

    # else, we've higher than the stack and have room, just return
    return result

    
def Check_Path_Down(rock, fuck_shit_stack, c_width):  # Reggie Watts reference
    ''' okay, so the simple case is looking if we mesh with the top of the stack.
        But a long rock could fall down many layers without running into anything.
        So the stack itself should contain the shape. '''
    # may need to compare multiple rows.
    result = True
    y = rock.y
    pre = rock.x - 1
    remainder = c_width - (len(rock.shape[rock.height-1]) + pre)
    row = 1
    while(y <= len(fuck_shit_stack) + 1):
        comp = ""
        try:
            comp += ("." * pre) + rock.shape[rock.height-row]
        except:
            breakpoint()

#        comp += ("." * pre) + rock.shape[rock.height-row]
        comp += '.' * remainder

        # compare w/ the stack row below this y-level (important for '+' shape)
        comp_row = list(comp)
        stack_row = fuck_shit_stack[y-2]  # -1 for index 0, -1 for one level below

        for j in range(c_width):
            if(comp_row[j] == '#' and stack_row[j] == '#'):
                result = False
        y += 1
        row += 1
        if(row > rock.height):
            break
    return result


def Add_to_Stack(rock,stack,c_width):

    while(len(rock.shape) > 0):
        shape = rock.shape.pop()
        pre = rock.x - 1
        new_row = ""
        new_row += "." * pre
        new_row += shape
        remainder = c_width - (len(shape) + pre)
        new_row += "." * remainder
        new_row = list(new_row)
        if(rock.y >= len(stack) + 1):
            # Easy add, no merging
            # for the stack itself we want a full list since we'll need to check
            # bounds within it later
            stack.append(new_row)
            rock.y += 1  # new bottom of shape since we shaved off a layer.
        else:

            # "add" shape #'s to whatever stack[y-1] has.
            # then update stack[y-1]
            merge_row = []
            for i in range(len(new_row)):
                if(new_row[i] == '#' or stack[rock.y-1][i] == '#'):
                    merge_row.append('#')
                else:
                    merge_row.append('.')
            stack[rock.y-1] = merge_row
            rock.y += 1

def Print_Stack(stack):
    ''' Print stack top-down (in reverse) '''
    for i in reversed(range(len(stack))):
        row = stack[i]
        row = ('').join(row)
        print("|%s|" % row)
    print("+-------+")

def Print_TopBot_Stack(stack):
    ''' Print stack top-down (in reverse) '''

    for i in reversed(range(len(stack))):
        if(i >= 0 and i<=5) or (i <= len(stack) and i >= len(stack)-5):
            row = stack[i]
            row = ('').join(row)
            print("|%s|" % row)
    print("+-------+")

def Print_Top_Stack(stack):
    ''' Print stack top-down (in reverse) '''

    for i in reversed(range(len(stack))):
        if(i <= len(stack) and i >= len(stack)-20):
            row = stack[i]
            row = ('').join(row)
            print("|%s|" % row)
    print("+-------+")

testcase = True
if testcase:
    file = "test.txt"
    c_width = 7
    num_rocks = 2022
else:
    file = "input.txt"
    c_width = 7
    num_rocks = 2022

# Initialize Rocks, we split these later, but this is easier to see.
shapes = []
shapes.append(['####'])
shapes.append(['.#.',
               '###',
               '.#.'])
shapes.append(['..#',
               '..#',
               '###'])
shapes.append(['#',
               '#',
               '#',
               '#'])
shapes.append(['##',
               '##'])


def Calculate_Stack(multiple,cur_stack,remainder):
    with open(file, "r") as stuff:
        lines = stuff.read().splitlines()

        stack = []  # stack of rocks (list of lists)
        active = False  # is there an active rock?
        next_shape = 0
        air = list(lines[0])
        next_air = 0
        cur_rock = 0

        # Rnd2 calculate repeating num of rocks
        if(remainder == -1):
            num_rocks = len(air) * len(shapes) * multiple
        else:
            num_rocks = remainder
            stack = cur_stack


        while(cur_rock <= num_rocks):
            if(not active):
                # Generate new rock
                cur_rock += 1
                The_Rock = Rock(shapes[next_shape], 3, len(stack)+4, )
                next_shape += 1
                if(next_shape == len(shapes)):
                    next_shape = 0
                active = True
        
            #######
            # AIR #
            #######

            if(air[next_air] == "<"):
                # try left.
                if(Check_Path_Left(The_Rock, stack, c_width)):
                    The_Rock.x -= 1
            else:
                # try right
                if(Check_Path_Right(The_Rock, stack, c_width)):
                    The_Rock.x += 1

            next_air += 1
            if(next_air == len(air)):
                next_air = 0

            ##################
            # The Rock falls #
            ##################

            if(The_Rock.y > len(stack) + 1):
                # just fall
                The_Rock.y -= 1
            elif(The_Rock.y == 1 and len(stack) == 0):   # move logic lower, this only happens once or twice
                # stop falling
                Add_to_Stack(The_Rock, stack, c_width)
                active = False
            else:
                if(Check_Path_Down(The_Rock, stack, c_width)):
                    The_Rock.y -= 1
                else:
                    Add_to_Stack(The_Rock, stack, c_width)
                    active = False
#    print("Rnd1 Stack Height:",len(stack))

    return stack, num_rocks

#    Print_Stack(stack)
#    print("Rnd1 Stack Height:",len(stack))


    # Okay, we can't keep track of the whole stack, but...
    # We can be confident rocks won't proceed if there is a solid left to right blockage
    # which doesn't have to be all on one level.
    # convert stack to dict so it's indexes are still right?
    # len(stack) will no longer work.

    # Nope, screw that. 
    # The input loops and the rocks loop.
    # Calculate a stack that's len(input) * number of shapes.
    # That's approx 50000, then just sit it on top of a copy of itself.
    # (no wind shifting when that happens)
    # figure out the total after that and just multiply.

#    Print_TopBot_Stack(stack)

    ## Bah, not that simple, some shapes could slip through the gaps and change the
    ## next height

    ## Maybe we can search for a multiple that repeats exactly and then add the new remainder

    # Okay, we're going to track the 'top' of the stack for each mulitple of fully repeating
    # input.  If we find a place where the top's match, that series will repeat forever.
    # It looks like this happens in the test input at 1 + (7 * x)

#    Print_Top_Stack(stack)

test = False
m = 1
stacks = {}
while(not test):
    if(m % 10 == 0):
        print("Multiple",m)

    (m_stack, num_rocks) = Calculate_Stack(m,[],-1)

    # Assumption: comparing the top 20 rows of the stack will be sufficient.
    t_stack = m_stack[-20:]
#    Print_Stack(m_stack)

    if(len(stacks) > 0):
        for s in stacks:
            (st,l) = stacks[s]
            if(st == t_stack):
#                print("Match",s,m)
                test = True
                break
    stacks[m] = (t_stack,len(m_stack))

    if(not test):
        m += 1

total_size = 0
(st,start_size) = stacks[s]
total_size += start_size
(st,match_size) = stacks[m]
diff_size = match_size - start_size
rocks_per_loop = num_rocks / m

big_multi = int (( 1000000000000 - (rocks_per_loop * s)) / (rocks_per_loop * (m-s)))
remainder = ( 1000000000000 - (rocks_per_loop * s)) % (rocks_per_loop * (m-s))

total_size += diff_size * big_multi

print("Rnd2 Rocks / Loop:",rocks_per_loop)
print("Start multiple:",s)
print("Repeat multiple:",m)
print("Diff Size", diff_size)
print("Big Multiple", big_multi)
print("Remaining rocks", remainder)
print("Almost Total Size:",total_size)

# okay, we still need to add the remainder to the stack.

(s_stack, x) = Calculate_Stack(s,[],-1)

s_len = len(s_stack)
print("Length s_stack", s_len)

(a_stack, num_rocks) = Calculate_Stack(0,[],s*rocks_per_loop + remainder)

print("Len a_stack",len(a_stack))
final_adds = len(a_stack) - s_len
print("Final", final_adds)

print("Total Size:",total_size+final_adds)





