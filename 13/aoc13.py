#!/usr/bin/env python3

import json
import copy


def Compare(one, two):

    ## I think this check is only relevant at the top layer.
    # except we also need to know when to proceed...
    # seems like it's relevant if we ever run out of items between two lists.
    # print("Comparing:", one, "\n            ", two)

    if len(one) != len(two):
        if len(one) == 0:
            return 1
        elif len(two) == 0:
            return 0

    while len(one) > 0 and len(two) > 0:
        left = one.pop(0)
        right = two.pop(0)
        if type(left) == type(right):
            if isinstance(left, int):
                # Integers
                # we can compare this shit
                # print("Comparing:", left, right)
                if left < right:
                    # correct order
                    return 1
                elif right < left:
                    # incorrect order
                    return 0
                else:
                    continue
            else:
                # they are lists

                # both lists to compare are empty
                if len(left) == 0 and len(right) == 0:
                    continue

                val = Compare(left, right)
                if val == 1:
                    return 1
                elif val == 0:
                    return 0
                # else, do nothing

        else:
            if isinstance(left, int):
                one = [left]
                val = Compare(one, right)
            else:
                two = [right]
                val = Compare(left, two)

            if val == 1:
                return 1
            elif val == 0:
                return 0
            # print("Type conversion, continue")
            # continue

    if len(one) == 0:
        return 1
    elif len(two) == 0:
        return 0
    return 2  # do nothing


def Sorty_McSorter(Rnd2, Output):
    """Rnd2"""

    """ Wait.. why do I care about efficiency?  Just compare all of them each time """
    while len(Rnd2) > 0:
        nPacket = Rnd2.pop(0)
        for i in range(len(Output)):

            if Compare(copy.deepcopy(Output[i]), copy.deepcopy(nPacket)):
                # we're at the end, add it.
                if i == len(Output) - 1:
                    Output.insert(i + 1, nPacket)
            else:
                Output.insert(i, nPacket)
                break


#  Unfinished binary sort, screw that!  Make the computer work!
#    while len(Rnd2) > 0:
#        nPacket = Rnd2.pop(0)
#        print(nPacket)
#        half = int(len(Output) / 2)
#        print("start here:", half)
#        if Compare(copy.deepcopy(Output[half]), copy.deepcopy(nPacket)):
# new packet goes after this index.
#            if(len(half)<=1):
#                Output.insert(half + 1, nPacket)
#                return
#        else:
#            if(len(half)<=1)
#                Output.insert(half, nPacket)
#                return

testcase = False
if testcase:

    inputfile = "test_rnd2.txt"
else:
    inputfile = "input_rnd2.txt"

with open(inputfile, "r") as stuff:
    lines = stuff.read().splitlines()

    total = len(lines)
    i = 0
    pair_index = 1
    Rnd1_total = 0
    while i < total:
        one = json.loads(lines[i])
        two = json.loads(lines[i + 1])
        i += 3

        val = Compare(one, two)
        if val == 1:
            # print("Correct order")
            Rnd1_total += pair_index
        #        elif val == 0:
        # print("Incorrect order")
        #        else:
        #            print("Error, top level should never get here")
        pair_index += 1
        #        print("\n======NEXT======\n")

        # blaa = input("\nwait...")

    # change input files if we need this
    # print("Rnd1 Total:", Rnd1_total)

    # Rnd2:  Re-read fresh input, we kinda screwed up those lists
    i = 0
    Rnd2 = []
    while i < total:
        one = json.loads(lines[i])
        two = json.loads(lines[i + 1])
        i += 3

        Rnd2.append(one)
        Rnd2.append(two)

    Output = []
    # give it a starting element
    Output.append(Rnd2.pop(0))
    Sorty_McSorter(Rnd2, Output)

    for i in range(len(Output)):
        if Output[i] == [[2]]:
            two = i + 1
        elif Output[i] == [[6]]:
            six = i + 1
    #        print(n)

    print("Rnd2: ", two * six)


# TODO Remember index count starts at 1!
