#!/usr/bin/env python3

import re


class Sensor:
    def __init__(self, x, y, bx, by):
        self.bx = bx
        self.by = by
        self.range = abs(bx - x) + abs(by - y)  # calculate manhattan distance.


testcase = False
Rnd1 = False
if testcase:
    file = "test.txt"
    testy = 10
else:
    file = "input.txt"
    testy = 2000000

with open(file, "r") as stuff:
    lines = stuff.read().splitlines()

    # establish classes for Beacons and Sensors.
    # Sensors should store the distance to their Beacon, this becomes their current sensor range.
    # for each position in the row in question, Calculate it's distance to each sensor, if it's further
    # than all of them, it could be a beacon.  We want the inverse of that, positions that can't be beacons and are
    # IN range of a sensor, but not the sensor's beacon itself (skip known beacon locations)

    # Assuming we need to start counting our row somewhere in negative X space, so we also need to determine
    # what our most negative X range actually IS based on the further range of the sensors.

    sensors = {}
    beacons = {}

    for line in lines:
        m = re.search(r"x=(-?\d+), y=(-?\d+).*x=(-?\d+), y=(-?\d+)", line)
        if m:
            sensorx = int(m.group(1))
            sensory = int(m.group(2))
            beaconx = int(m.group(3))
            beacony = int(m.group(4))

            sensors[(sensorx, sensory)] = Sensor(sensorx, sensory, beaconx, beacony)
            beacons[(beaconx, beacony)] = 1
        else:
            print("error, regex failed", line)
            exit()

    # Figure out the size of our field.
    first = 1
    for sensor in sensors:
        (x, y) = sensor
        srange = sensors[(x, y)].range
        if first:
            minx = x - srange
            maxx = x + srange
            miny = y - srange
            maxy = y + srange
            first = 0
            continue
        if x - srange < minx:
            minx = x - srange
        if x + srange > maxx:
            maxx = x + srange
        if y - srange < miny:
            miny = y - srange
        if y + srange > maxy:
            maxy = y + srange

    if Rnd1:
        print("X", minx, maxx)
        print("Y", miny, maxy)
        i = minx
        not_a_beacon = 0
        while i <= maxx:
            # current = (i,testy)

            # for each position, check to see if we're within range of each sensor.
            # this will not scale.
            for sensor in sensors:
                (x, y) = sensor
                distance = abs(x - i) + abs(y - testy)
                if distance <= sensors[sensor].range:
                    # cannot be a beacon (or already is)
                    if (i, testy) not in beacons:
                        not_a_beacon += 1
                        #                    print("Not a beacon")
                        break
            i += 1

        print("Rnd1 (not a beacon):", not_a_beacon)

    ## Rnd2 ##

    minx = 0
    miny = 0
    if testcase:
        maxx = 20
        maxy = 20
    else:
        maxx = 4000000
        maxy = 4000000

    print("X", minx, maxx)
    print("Y", miny, maxy)

    # so I move until I find a sensor.  calculate it's distance, but also veritcal distance from me.
    # (figure out where in the diamond I am).  Then skip the rest of the diamond.
    # Keep in mind I might not enter a sensor range right at the edge.

    y = 0
    while y < maxy:

        x = 0
        while x < maxx:

            # find closest sensor

            # TODO, maybe my dist vs smallest is wrong?

            shortest = None
            for sensor in sensors:
                (sx, sy) = sensor
                dist = abs(x - sx) + abs(y - sy)
                if (
                    dist <= sensors[sensor].range
                ):  # only do diffs if we're inside the range.
                    if shortest == None:
                        shortest = dist
                        current_sensor = (sx, sy)
                    elif dist < shortest:
                        shortest = dist
                        current_sensor = (sx, sy)

            if shortest == None:
                print("Holy Crap!")
                print("Rnd2:", (x, y))
                print("Rnd2 Freq: ", x * 4000000 + y)
                exit()
            #            print("X, Y", x, y)
            #            print("Dist:", shortest)
            #            print("Current Sensor:", current_sensor)
            #            print("Sensor Range: ", sensors[current_sensor].range)
            if x < 0:
                print("Error x<0, Exit")
                exit()
            #
            (cx, cy) = current_sensor
            xdiff = abs(cx - x)
            ydiff = abs(cy - y)
            #            print("Xdiff:", xdiff)
            #            print("Ydiff:", ydiff)

            ## At the closest sensor we can skip to it's furtherest edge at this 'height'

            if x > cx:
                # Move X + range at the level of y we're at.
                #                x += sensors[current_sensor].range - ydiff
                change = sensors[current_sensor].range - xdiff - ydiff
                if change == 0:
                    x += 1
                elif change < 0:
                    print("error 3")
                    exit()
                else:
                    x += change

                #                print("New X:", x)
                continue
            elif x < cx:
                x += xdiff + sensors[current_sensor].range - ydiff
                #                x += 2 * sensors[current_sensor].range - ydiff * 2
                #                print("New 2X:", x)
                continue

            x += 1

            # this is the closest sensor to us, find out where in it's range we are.
            # then skip to it's edge.
        y += 1
    # use pypy3
