#!/usr/bin/env python3

import re

testcase = False
if testcase:
    file = "test.txt"
    
else:
    file = "input.txt"

with open(file, "r") as stuff:
    lines = stuff.read().splitlines()
