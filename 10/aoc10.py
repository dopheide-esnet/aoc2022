#!/usr/bin/env python3

import re


def Get_Instruction(lines, line):
    if lines[line] == "noop":
        return ["noop", 0, 1]
    (inst, val) = lines[line].split(" ")
    if inst == "addx":
        return [inst, int(val), 2]  # instruction, value, # of cycles to complete
    else:
        print("Error, shouldn't be here")


def Draw_Pixel(clock, sprite):
    position = (clock % 40) - 1  # positions are 0-39
    digit_buffer = 4

    # Print left Column
    if position == 0:
        if len(str(clock)) > digit_buffer:
            print("Error, left column is too narrow")
            exit()
        else:
            print()
            spaces = " " * (digit_buffer - len(str(clock)))
        print("Cycle %s%s -> " % (spaces, str(clock)), end="")

    # Print pixel if it lines up with the sprite
    if position >= (sprite - 1) and position <= (sprite + 1):
        print("#", end="")
    else:
        print(".", end="")

    return


with open("input.txt", "r") as stuff:
    lines = stuff.read().splitlines()

    check_strength = [20, 60, 100, 140, 180, 220]
    signal_sum = 0
    registerX = 1

    (inst, val, inst_cycles) = Get_Instruction(lines, 0)
    line = 1  # current line in the instruction set

    # tick tock
    clock = 1
    while 1:
        # During Cycle

        # do our signal strength checks
        # print("Registser during cycle %i: %s" % (clock, registerX))
        if clock in check_strength:
            signal_sum += registerX * clock

        Draw_Pixel(clock, registerX)

        # End of Cycle
        clock += 1

        inst_cycles -= 1
        if inst_cycles == 0:  # end of current instruction cycles
            # do instruction
            if inst != "noop":
                if inst == "addx":
                    registerX += val

            if line < len(lines):  # are there instructions left in the queue?
                (inst, val, inst_cycles) = Get_Instruction(lines, line)
                line += 1
            else:
                break

    print("\nRnd1 Signal Sum:", signal_sum)
