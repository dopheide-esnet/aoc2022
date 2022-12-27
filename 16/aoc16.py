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


def Best_Rate(depth, rates, location, elocation, useful, valves, mrem, erem, p2h, e2h):
    """Rnd2:  Need to track a different number of minutes remaining
    and need the rates data structure to track both paths (m and e)
    We try to do m and e as part of the dict key (which is the path) 
    
    This doesn't work.
    
    """

    #    rates = copy.deepcopy(ratez)
    if depth not in rates:
        rates[depth] = dict()

    for i in range(len(useful)):
        min_rem = mrem
        cur_useful = copy.deepcopy(useful)
        valve = cur_useful[i]

        dict_useful = {}
        for c in cur_useful:
            dict_useful[c] = 0
        del dict_useful[valve]

        # we lose minutes traveling to the valve
        min_rem = min_rem - valves[location].paths[valve]

        if min_rem < 1 and erem < 1:
            # Ya, done!
            continue  # TODO, don't continue until both m and e are done
        else:
            # open
            min_rem -= 1  # takes 1 min to open valve
            pressure = min_rem * valves[valve].rate

            if depth == 0:
                new_path = "m" + valve
                rates[depth][new_path] = pressure
                
                ### rates path name will include who's doing it m or e. (me or elephant)

            else:

                rate = rates[depth - 1][p2h]

                # TODO, need to track mNAME and eNAME

                new_rate = rate + pressure
                new_path = p2h + valve  # str
                rates[depth][new_path] = new_rate

        if min_rem < 2:
            # not enough time to do anything
            print("skip continue2")
            #continue  ## TODO, can't continue until both m and e are done
        
        ##### TODO.  So I think here we loop over dict_useful and pull one for 'e'
        # then continue on with min_rem and el_rem for both...
        el_useful = list(dict_useful.keys())
        for j in range(len(dict_useful)):
            edict_useful = copy.deepcopy(dict_useful)
            el_rem = erem
            evalve = el_useful[j]
            del edict_useful[evalve]
        
            el_rem = el_rem - valves[elocation].paths[evalve]
            
            if el_rem < 1:
                # Ya, done!
                print("skip e continue")
            else:
                el_rem -= 1  # takes 1 min to open valve
                epressure = el_rem * valves[evalve].rate + pressure

                if depth == 0:
                    enew_path = "e" + evalve
                    rates[depth][enew_path] = epressure
                else:
                    rate = rates[depth - 1][e2h]
                    new_rate = rate + epressure
                    enew_path = e2h + evalve  # str
                    rates[depth][enew_path] = new_rate
            
            if el_rem < 2:
                print("skip e continue2")

            if len(edict_useful) > 0:
        ### TODO, potential issue.  If there's only one left, it might be 
        # better for the elephant to get it vs me.

                Best_Rate(
                depth + 1,
                rates,
                valve,
                evalve,
                list(edict_useful.keys()),
                valves,
                min_rem,
                el_rem,
                new_path,
                enew_path
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

    Calculate_Paths(all_valves)

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

    Rnd1 = False
    if Rnd1:
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


    Dammit(0, rates, location, useful_valves, all_valves, 26, path_to_here)
#    pprint.pprint(rates)


    ''' okay, we know Dammit() works
        Let's now just compare the paths that don't contain the same
        letters
        Also, we can probably skip depths 0-2'''

    i = 2
    max = 0
    print("This takes awhile, use pypy3...")
    # real	18m26.561s
    # user	18m17.701s
    # sys	0m8.101s
    # we know from previous runs we can start at at least i=4, max 2542
    while(i < len(rates)):
        ### Big O no no!
        j = i
        print("Comparing Depths:",i,j)
        for r in rates[i]:
            me = []
            mr = r
            while r:
                me.append(r[:2])
                r = r[2:]


            j = i  # already compared lower depths with all higher depths
            while(j < len(rates)):
                for q in rates[i]:
                    you = []
                    mq = q
                    while q:
                        you.append(q[:2])
                        q = q[2:]
                
#                print(me,you)
                    both = list(set().union(me,you))
                    if(len(both) == (len(me) + len(you))):
                        total = rates[i][mr] + rates[i][mq]
                        if(total > max):
                            max = total
                            print("New max:",max)
                j += 1
        i += 1
    print("Rnd2 Max:", max)

  #          union of lists == len of list1 plus list2. after splitting into two char pairs

    exit()

    Best_Rate(0, rates, location, location, useful_valves, all_valves, 26, 26, path_to_here, path_to_here)
    pprint.pprint(rates)
    best = 0
    bestpath = ""
    for i in range(len(rates)):
        if len(rates[i]) > 0:
            m = max(rates[i], key=rates[i].get)
            mr = rates[i][m]
            if mr > best:
                best = mr
                bestpath = m

    # need to add e to m somehwere....
    # try just adding pressure into epressure.

    print("Rnd2:", best, bestpath)




# maybe pypy3 again?
