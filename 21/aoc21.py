#!/usr/bin/env python3

import re

class Monkey:   # tree node, get it... monkey's in a tree?  I'm hilarious.
    def __init__(self, val, lc, rc, op):
        self.val = val
        self.parent = ""  # we will populate this later when we climb down the tree
        self.left_child = lc
        self.right_child = rc
        self.operator = op

def Print_Monkeys(monkeys):
    for name in monkeys:
        print("Name:",name)
        print("Value:",monkeys[name].val)
        print("Parent:",monkeys[name].parent)
        print("Children:",monkeys[name].left_child, monkeys[name].right_child)
        print("Operator:",monkeys[name].operator,"\n")

def Monkeys_Need_Parents_Too(monkeys, name):
    '''
    Start at the 'root' monkey and walk the tree populating the parent values,
    that should/might help us later.
    '''    
    monkeys[monkeys[name].left_child].parent = name
    monkeys[monkeys[name].right_child].parent = name
    if(monkeys[monkeys[name].left_child].val == None):
        Monkeys_Need_Parents_Too(monkeys, monkeys[name].left_child)
    if(monkeys[monkeys[name].right_child].val == None):
        Monkeys_Need_Parents_Too(monkeys, monkeys[name].right_child)

def Climb_Tree(monkeys,name):
    '''
    Climb down the tree and calculate the values
    '''
    if(monkeys[monkeys[name].left_child].val == None):
        Climb_Tree(monkeys,monkeys[name].left_child)
        if(monkeys[monkeys[name].left_child].val == None):
            print("Error, this should not be the case, left child has no value")
    if(monkeys[monkeys[name].right_child].val == None):
        Climb_Tree(monkeys,monkeys[name].right_child)
        if(monkeys[monkeys[name].right_child].val == None):
            print("Error, this should not be the case, right child has no value")           
    
    lv = monkeys[monkeys[name].left_child].val
    rv = monkeys[monkeys[name].right_child].val
    op = monkeys[name].operator
    if(op == "+"):
        monkeys[name].val = lv + rv
    elif(op == "-"):
        monkeys[name].val = lv - rv
    elif(op == "/"):
        monkeys[name].val = lv / rv
    else:
        monkeys[name].val = lv * rv
    
testcase = False
if testcase:
    file = "test.txt"
else:
    file = "input.txt"

with open(file, "r") as stuff:
    lines = stuff.read().splitlines()

    monkeys = {}
    for line in lines:
        m = re.search(r'^(\w+): (\d+)', line)
        if(m):
            name = m.group(1)
            val = int(m.group(2))
            monkeys[name] = Monkey(val,"","","")
        else:
            n = re.search(r'(\w+): (\w+) ([+-/*]) (\w+)', line)
            if(n):
                name = n.group(1)
                lc = n.group(2)
                op = n.group(3)
                rc = n.group(4)
                monkeys[name] = Monkey(None,lc,rc,op)
            else:
                print("Regex error")
                exit()

    Monkeys_Need_Parents_Too(monkeys,"root")
    Climb_Tree(monkeys,"root")

#    Print_Monkeys(monkeys)
    print("Rnd1:",int(monkeys["root"].val))

