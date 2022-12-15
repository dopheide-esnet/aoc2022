#!/usr/bin/env python3

import re

with open("input.txt", "r") as stuff:
    pairs = stuff.readlines()

    rnd1_total = 0
    rnd2_total = 0
    for line in pairs:
        line = line.strip()
        (set1, set2) = line.split(",")
        (cmin1, cmax1) = set1.split("-")
        (cmin2, cmax2) = set2.split("-")

        min1 = int(cmin1)
        max1 = int(cmax1)
        min2 = int(cmin2)
        max2 = int(cmax2)

        # Rnd1: one group entirely part of the other
        if ((min2 <= min1) and (max2 >= max1)) or ((min1 <= min2) and (max1 >= max2)):
            print(min1, max1, min2, max2, "True")
            rnd1_total += 1
        else:
            print(min1, max1, min2, max2)
        #            if rnd1_total == 10:
        #                exit(1)

        # Rnd2: any overlap
        if not ((max1 < min2) or (max2 < min1)):
            rnd2_total += 1

    print("Rnd1_total: ", rnd1_total)
    print("Rnd2_total: ", rnd2_total)
