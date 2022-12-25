#!/usr/bin/env python3

import re
import copy
import pprint


class Valve:
    def __init__(self, name, tunnels, rate):
        self.name = name
        self.tunnels = tunnels
        self.rate = rate
        self.state = "closed"
        self.paths = {}  # shortest path to each other valve


def Calculate_Paths(valves):
    """Pre-Calculate the shortest path between each valve to any other valve
    Since we're only doing this once it doesn't need to be very efficient"""
    for name in valves:
        ## go down each tunnel, and count the distance, populate paths.
        valves[name].paths[name] = 0
        for tunnel in valves[name].tunnels:
            if tunnel not in valves[name].paths:
                valves[name].paths[tunnel] = 1

    depth = 1
    while depth <= len(valves):
        for name in valves:
            tmp_paths = copy.deepcopy(valves[name].paths)
            for path in tmp_paths:
                # Calculate_Deeper_Paths...
                for path2 in valves[path].paths:
                    #                    print(path2)
                    if path2 not in valves[name].paths:
                        valves[name].paths[path2] = valves[path].paths[path2] + 2
                    elif (
                        valves[path].paths[path2] + valves[name].paths[path]
                        < valves[name].paths[path2]
                    ):
                        valves[name].paths[path2] = (
                            valves[path].paths[path2] + valves[name].paths[path]
                        )
        depth += 1


def Calculate_Paths_New(valves):
    """Pre-Calculate the shortest path between each valve to any other valve
    Since we're only doing this once it doesn't need to be very efficient"""
    for name in valves:
        ## go down each tunnel, and count the distance, populate paths.
        valves[name].paths[name] = 0
        for tunnel in valves[name].tunnels:
            if tunnel not in valves[name].paths:
                valves[name].paths[tunnel] = 1

    depth = 1
    while depth <= len(valves):
        for name in valves:
            tmp_paths = copy.deepcopy(valves[name].paths)
            for path in tmp_paths:
                # Calculate_Deeper_Paths...

                # current distance to this next one is valves[name].paths[path]

                for path2 in valves[path].paths:
                    #                    print(path2)
                    if path2 not in valves[name].paths:
                        valves[name].paths[path2] = (
                            valves[path].paths[path2] + valves[name].paths[path]
                        )
                    elif (
                        valves[path].paths[path2] + valves[name].paths[path]
                        < valves[name].paths[path2]
                    ):

                        valves[name].paths[path2] = (
                            valves[path].paths[path2] + valves[name].paths[path]
                        )
        depth += 1


#    print(valves["JJ"].paths)
# {'JJ': 0, 'II': 1, 'AA': 2, 'DD': 3, 'BB': 3, 'CC': 4, 'EE': 4, 'FF': 5, 'GG': 6, 'HH': 7}


def Potentials(location, useful, valves, potentials, min_rem):
    """Calculate the pressure relief potential of each valve given our current location
    it's distance, state, etc"""

    for valve in useful:
        if valves[valve].state == "closed":
            # potential = rate * (min_rem - distance)
            potentials[valve] = valves[valve].rate * (
                min_rem - valves[location].paths[valve]
            )
        else:
            # already open, it's additive potential is zero
            potentials[valve] = 0


def Best_Rate(depth, rates, location, useful, valves, mrem):

    #    rates = copy.deepcopy(ratez)
    if depth not in rates:
        rates[depth] = dict()

    for i in range(len(useful)):

        min_rem = mrem
        cur_useful = copy.deepcopy(useful)
        #        print(cur_useful)
        valve = cur_useful[i]

        ## WHY IS JJ ALWAYS LAST?

        dict_useful = {}
        for c in cur_useful:
            dict_useful[c] = 0

        del dict_useful[valve]

        ### TODO... still seeing duplicates

        min_rem = min_rem - valves[location].paths[valve]

        if min_rem < 1:
            # Ya, done!
            # Rates don't change

            #            print("End", rates)
            return
        else:
            # open
            min_rem -= 1  # takes 1 min to open valve
            pressure = min_rem * valves[valve].rate

            # breakpoint()

            # TODO
            if depth > 0:
                #### FUUUUUCKK....  this is adding to everything, not just the path that got us here.

                for r in rates[depth - 1]:  # rates[depth] is a dict
                    rate = rates[depth - 1][r]
                    new_rate = rate + pressure
                    new_path = r + valve  # str
                    rates[depth][new_path] = new_rate
            else:
                rates[depth][valve] = pressure

            if len(dict_useful) == 0 or min_rem < 2:
                # Nowhere to go or we don't have time to get anywhere and do something.
                #                print("End2", rates)
                return
            else:
                Best_Rate(
                    depth + 1, rates, valve, list(dict_useful.keys()), valves, min_rem
                )
    #                print(rates)

    return


def Dammit(depth, rates, location, useful, valves, mrem, p2h):

    #    rates = copy.deepcopy(ratez)
    if depth not in rates:
        rates[depth] = dict()

    for i in range(len(useful)):
        min_rem = mrem
        cur_useful = copy.deepcopy(useful)
        #        print(cur_useful)
        valve = cur_useful[i]

        dict_useful = {}
        for c in cur_useful:
            dict_useful[c] = 0
        del dict_useful[valve]

        # we lose minutes traveling to the valve
        min_rem = min_rem - valves[location].paths[valve]

        if min_rem < 1:
            # Ya, done!
            continue
        else:
            # open
            min_rem -= 1  # takes 1 min to open valve
            pressure = min_rem * valves[valve].rate

            if depth == 0:
                rates[depth][valve] = pressure
                new_path = valve
            else:

                rate = rates[depth - 1][p2h]
                new_rate = rate + pressure
                new_path = p2h + valve  # str
                rates[depth][new_path] = new_rate

                # this is too big, how did it happen?
                # (Pdb) valves['RT'].paths['UH']
                # 6
                # (Pdb) valves['PG'].paths['UH']
                # 5
                # (Pdb) valves['XT'].paths['UH']   # ah ha!
                # 5

                ## RT to UH should be 7

                if new_rate == 1862:
                    print(new_path)
                    print(valves["AA"].paths)
                    breakpoint()

        if min_rem < 2:
            # not enough time to do anything
            continue

        if len(dict_useful) > 0:
            #            #             print(list(dict_useful.keys()))
            Dammit(
                depth + 1,
                rates,
                valve,
                list(dict_useful.keys()),
                valves,
                min_rem,
                new_path,
            )


testcase = False
if testcase:
    file = "test.txt"
else:
    file = "input.txt"

with open(file, "r") as stuff:
    lines = stuff.read().splitlines()

    all_valves = {}
    open_valves = {}
    closed_valves = {}
    total_pressure = 0
    pressure_level = 0
    for line in lines:
        m = re.search(r"^Valve (\w\w).*rate=(\d+);.*valves? (.*)$", line)
        if m:
            vname = m.group(1)
            vrate = int(m.group(2))
            vtunnels = m.group(3).split(", ")
            #            print(vname, vrate, vtunnels)
            # build valve
            all_valves[vname] = Valve(vname, vtunnels, vrate)
        else:
            print("regex error")
            exit()

    # Is it worth pre-calculating a valve's shortest distance from all other valves?
    # But that might not even be the optimal path because we could turn on a good valve on
    # the way via a different path.  Ugh.

    # What about a valve's "potential value" being it's rate * (minutes remaining - distance)
    #  (assuming it's still closed)
    #
    # Let's start here, but I really think there's a problem of the 'valuable' middle valve on a path.

    Calculate_Paths_New(all_valves)

    # Remove useless valves from further consideration.
    # Okay, we have the paths, but most of these valves are useless to open with rate=0
    # We can ignore all of those when figuring out which one to open next.
    useful_valves = []
    for valve in all_valves:
        if all_valves[valve].rate != 0:
            useful_valves.append(valve)

    # Since we've removed the useless valves, I think we can just recursively figure out the best path.

    location = "AA"
    #    minute = 0
    #    potentials = {}
    #    while minute < 30:
    #        Potentials(location, useful_valves, all_valves, potentials, (30 - minute))
    #        print(potentials)
    #                 minute += 1

    rates = {}

    path_to_here = ""
    Dammit(0, rates, location, useful_valves, all_valves, 30, path_to_here)
    # Best_Rate(0, rates, location, useful_valves, all_valves, 30)

    # pprint.pprint(rates)
    best = 0
    bestpath = ""
    for i in range(len(rates)):
        if len(rates[i]) > 0:
            m = max(rates[i], key=rates[i].get)
            mr = rates[i][m]
            if mr > best:
                best = mr
                bestpath = m

    print("Rnd1:", best, bestpath)
# maybe pypy3 again?
