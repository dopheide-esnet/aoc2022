#!/usr/bin/env python3

import re
import copy

class MyStuff:
    def __init__(self):
        self.ore = 0
        self.clay = 0
        self.obsidian = 0
        self.geode = 0
        self.robots = {"ore": 1, "clay": 0, "obsidian": 0, "geode": 0}

class Blueprint:
    def __init__(self,b_num, ore1,ore2,ore3, clay, ore4, obsidian):
        self.num = b_num
        self.ore_robot = ore1
        self.clay_robot = ore2
        self.obsidian_robot = (ore3, clay)
        self.geode_robot = (ore4, obsidian)
        self.max_geodes = 0
        self.quality = 0
    def print(self):
        print(self.ore_robot)
        print(self.clay_robot)
        print(self.obsidian_robot)
        print(self.geode_robot)
        print(self.max_geodes)
        print(self.quality)

def Calculate_Blueprint(blueprint,max_time,maximums):
#    blueprint.print()

    # Init my pile of stuff
    my_pile = MyStuff()
    Make_Decisions2(blueprint,my_pile,1,max_time,maximums)


def Run_Clock(blueprint,pile,clock,max_time,maximums,rtype):

    while(clock <= max_time):
        # collecting takes the whole minute, so we see if we have enough now
        build = "none"
        if(rtype == "ore") and (blueprint.ore_robot <= pile.ore):
            build = "ore"
        elif(rtype == "clay") and (blueprint.clay_robot <= pile.ore):
            build = "clay"
        elif(rtype == "obsidian"):
            (o,c) = blueprint.obsidian_robot
            if(o <= pile.ore and c <= pile.clay):
                build = "obsidian"
        elif(rtype == "geode"):
            (o,ob) = blueprint.geode_robot
            if(o <= pile.ore and ob <= pile.obsidian):
                build = "geode"

        # Collect
        pile.ore += pile.robots["ore"]
        pile.clay += pile.robots["clay"]
        pile.obsidian += pile.robots["obsidian"]
        pile.geode += pile.robots["geode"]

#        if(clock == max_time):
#            print("debug:",pile.robots)

        if(clock == max_time):
            if(blueprint.num not in maximums):
                maximums[blueprint.num] = pile.geode
            else:
                if(maximums[blueprint.num]) < pile.geode:
                    maximums[blueprint.num] = pile.geode

        if(build == "ore"):
            pile.ore -= blueprint.ore_robot
            pile.robots["ore"] += 1
            build = "done"
        elif(build == "clay"):
            pile.ore -= blueprint.clay_robot
            pile.robots["clay"] += 1
            build = "done"
        elif(build == "obsidian"):
            (o,c) = blueprint.obsidian_robot
            pile.ore -= o
            pile.clay -= c
            pile.robots["obsidian"] += 1
            build = "done"
        elif(build == "geode"):
            (o,ob) = blueprint.geode_robot
            pile.ore -= o
            pile.obsidian -= ob
            pile.robots["geode"] += 1
            build = "done"

        # Advance the clock
        clock += 1
        if(build == "done"):
            pile2 = copy.deepcopy(pile)
            blueprint2 = copy.deepcopy(blueprint)
            Make_Decisions2(blueprint2,pile2,clock,max_time,maximums)
            break


def Make_Decisions2(my_blueprint,my_pile,my_clock,max_time,maximums):
    ''' Recursively try different robots until we're out of time '''

    # pick our next robot type
    # But remember, we can't make robots for types we can't produce resources for
    # Let's also prioritize.

    # max cost of any robot in ore is our ore robot limit.
    # max cost of an obsidian robot in clay is our clay robot limit.
    (o3,c) = my_blueprint.obsidian_robot
    (o4,o) = my_blueprint.geode_robot
    max_ore = max([my_blueprint.ore_robot,my_blueprint.clay_robot,o3,o4])
    max_clay = c
    max_obsidian = o

    # It _seems_ like, once we can build the best type robot we should never go
    # back to ore.
    options = list()
    if(my_pile.robots["obsidian"] >= 1):
        options.append("geode")
    if(my_pile.robots["clay"] >= 1) and (my_pile.robots["obsidian"] < max_obsidian):
        options.append("obsidian")
    if(my_pile.robots["clay"] < max_clay):
        options.append("clay")
    if(my_pile.robots["ore"] < max_ore):
        options.append("ore")

    # Override:
    # Once we're at a point where we produce enough material to produce
    # a geode robot every round, do nothing else.
    if(my_pile.robots["ore"] >= o4 and my_pile.robots["obsidian"] >= o):
        options = ["geode"]

    for rtype in options:
        pile = copy.deepcopy(my_pile)
        blueprint = copy.deepcopy(my_blueprint)
        clock = my_clock

        Run_Clock(blueprint,pile,clock,max_time,maximums,rtype)


testcase = False
if testcase:
    file = "test.txt"
    max_time = 32
else:
    file = "input.txt"
    max_time = 32

with open(file, "r") as stuff:
    lines = stuff.read().splitlines()

    blueprints = {}
    for line in lines:
        #                         B_num    ore     ore     ore    clay     ore    obsidian
        m = re.search(r'Blueprint (\d+).* (\d+).* (\d+).* (\d+).* (\d+).* (\d+).* (\d+)',line)
        if(m):
            b_num = int(m.group(1))
            ore1 = int(m.group(2))
            ore2 = int(m.group(3))
            ore3 = int(m.group(4))
            clay = int(m.group(5))
            ore4 = int(m.group(6))
            obsidian = int(m.group(7))
            blueprints[b_num] = Blueprint(b_num,ore1, ore2, ore3, clay, ore4, obsidian)
        else:
            print("Error, regex fail")

    maximums = {}

#    for bp in blueprints:
#        Calculate_Blueprint(blueprints[bp],max_time,maximums)    
#        print(maximums)

    # Change up for Rnd2, only need the first 3 blueprints
    for i in range(1,4):
        if(i in blueprints):
            Calculate_Blueprint(blueprints[i],max_time,maximums)
            print(maximums)

    quality_total = 0
    rnd2_max_mult = 1
    for m in maximums:
        quality_total += m * maximums[m]
        rnd2_max_mult *= maximums[m]

    print("Rnd1 Quality:", quality_total)
    print("Rnd2:",rnd2_max_mult)


