#!/usr/bin/env python3

import copy

def c2n(c):
    if(c == "="):
        return -2
    elif(c == "-"):
        return -1
    else:
        return int(c)

def Convert_to_Decimal(line):
    snafu = list(line)
    num = 0
    while(len(snafu) > 0):
        char = snafu.pop(0)
        num += c2n(char) * 5**(len(snafu))
    return num

def lm(p):
    tot = 0
    for i in range(p+1):
        tot += 2 * (5**i)
    return tot

def Convert_to_Snafu(total):
    maxp = 0
    snafu = ""

    # find highest power
    while(total / (5**maxp) > 1):
            maxp+=1

    lower_max = lm(maxp-1)
    if(total < lower_max):
        maxp -= 1

    print('p',maxp)

    p = maxp
    while(p >= 0):

        lower = lm(p-1)

        if(total > 0):
            one = 5**p
            if(one + lower < total ):  # if this is true, we'll have to subtract later
                snafu = snafu + '2'
                total -= 2*(5**p)
            elif(lower < total): 
                snafu = snafu + '1'
                total -= 5**p

            else:
                snafu = snafu + "0" 

        elif(total < 0):
            one = 5**p
            if(one + lower < abs(total)):
                snafu = snafu + '='
                total += (2*(5**p))
            elif(lower < abs(total)):
                snafu = snafu + '-'
                total += 5**p

            else:
                snafu = snafu + "0"

        else:
            snafu = snafu + "0"

        p -= 1

    return snafu

testcase = False
if testcase:
    file = "test.txt"
else:
    file = "input.txt"

with open(file, "r") as stuff:
    lines = stuff.read().splitlines()

    total = 0
    for line in lines:
        total += Convert_to_Decimal(line)

#    snafu = Convert_to_Snafu(total)

#    print("We want", Convert_to_Decimal('1-0---0'))

#    snafu = Convert_to_Snafu(12345)
    snafu = Convert_to_Snafu(total)

    print("Rnd1:",total)
    print("Rnd1 SNAFU:",snafu)

