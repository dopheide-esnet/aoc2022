#!/usr/bin/env python3

import re

"""
$ cd /
$ ls
187585 dgflmqwt.srm
dir gnpd
200058 hbnlqs
dir jsv
dir mfhzl
dir nljtr
dir nwzp
61949 qdswp.wfj
21980 rbq.hpj
dir rfwwwgr
dir sbnhc
dir zhfl
136762 zwg
$ cd gnpd
$ ls
dir dcqq
dir dnscfz
dir dwqbhgc
dir lsrb
167581 ndwfr.pbv
"""

Rnd1_total = 0
Rnd2 = {"name": "", "size": 0}


class Dir:
    def __init__(self, name, parent):
        self.name = name
        self.type = "dir"
        self.parent = parent
        self.size = 0
        self.contents = dict()


class File:
    def __init__(self, name, size):
        self.name = name
        self.type = "file"
        self.size = size


def calculate_dir_size(tree):
    # is moving around in this tree going to screw up my current location?
    l_size = 0
    for item in tree.contents:
        if tree.contents[item].type == "file":
            l_size += tree.contents[item].size
        if tree.contents[item].type == "dir":
            l_size += calculate_dir_size(tree.contents[item])
    tree.size = l_size
    if l_size <= 100000:
        global Rnd1_total
        Rnd1_total += l_size
    return l_size


def Find_That_Shit(tree, ns):
    global Rnd2
    for item in tree.contents:
        if tree.contents[item].type == "dir":
            if tree.contents[item].size >= ns:
                if Rnd2["name"] != "":
                    if tree.contents[item].size < Rnd2["size"]:
                        Rnd2["name"] = tree.contents[item].name
                        Rnd2["size"] = tree.contents[item].size
                else:
                    Rnd2["name"] = tree.contents[item].name
                    Rnd2["size"] = tree.contents[item].size
            Find_That_Shit(tree.contents[item], ns)


with open("input.txt", "r") as stuff:
    lines = stuff.read().splitlines()
    listing = 0
    location = Dir("/", None)
    for line in lines:
        if line == "$ cd /":
            # skip the first one, we've already initialized it
            # print("cd /")
            continue

        ## we never do a 'cd' before an ls, so we can use ls to populate the data
        m = re.search(r"^\$\scd\s([\w\.]+)", line)
        if m:
            listing = 0
            # print("Change Dir: ", m.group(1))
            if m.group(1) == "..":
                location = location.parent  # ???
            else:
                # shit.. probably need the contents to be a dict.
                location = location.contents[m.group(1)]
            continue

        if re.match(r"^\$\sls", line):
            listing = 1
            continue

        if listing == 1:
            # add stuff to the current location
            m = re.search(r"dir\s([\w\.]+)", line)
            if m:
                # add directory
                name = m.group(1)
                # print("     Dir:", name)
                location.contents[name] = Dir(name, location)
            else:
                n = re.search(r"(\d+)\s([\w\.]+)", line)
                if n:
                    fname = n.group(2)
                    fsize = int(n.group(1))
                    # print("     File:", fsize, fname)
                    location.contents[fname] = File(fname, fsize)

    # Okay, in theory our directory structure is built.
    # Now we need to traverse the whole thing and recursively calculate the directory sizes.
    # Can also go ahead and add the Rnd1 information to a list as we go.

    # Where are we in the structure?  Get back to root.
    while location.parent != None:
        location = location.parent

    location.size = calculate_dir_size(location)
    # size is already be set in the structure by this point, would be interesting to check
    print(location.size)

    print("Rnd1 Total: ", Rnd1_total)

    disk_size = 70000000
    required_space = 30000000
    free_space = disk_size - location.size
    needed_space = required_space - free_space
    print("Needed Space:", needed_space)

    # Choose directory with smallest size that's at least needed_space big
    Find_That_Shit(location, needed_space)
    print("Rnd2 Dir Name:", Rnd2["name"], Rnd2["size"])
