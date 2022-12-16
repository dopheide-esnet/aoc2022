#!/usr/bin/env python3

import re


def check_four(four):
    """are the four characters different?"""
    while len(four) > 1:
        c = four.pop()
        if c in four:
            return False
    return True


def find_start_of_packet(stream, howmany):
    """track the last four characters and test if they last four aren't equal"""
    last_four = list()
    for i in range(len(stream)):
        last_four.append(stream[i])
        if len(last_four) == howmany:
            # Make a copy or else!!!
            if check_four(last_four.copy()):
                return i + 1
            del last_four[0]


with open("input.txt", "r") as stuff:
    lines = stuff.read().splitlines()

    # only one line this time
    stream = list(lines[0])

    start = find_start_of_packet(stream, 4)
    print("Rnd1 start: ", start)

    msg_start = find_start_of_packet(stream, 14)
    print("Rnd2 start: ", msg_start)
