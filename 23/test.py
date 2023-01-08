
import pytest
from aoc23 import Get_Monkeys, Decision

def test_input():
    lines = ['....#..', '..###.#', '#...#.#', '.#...##', '#.###..', '##.#.##', '.#..#..']
    (monkeys,map) = Get_Monkeys(lines)
    answer = [(0, 4), (1, 2), (1, 3), (1, 4), (1, 6), (2, 0), (2, 4), (2, 6), (3, 1), (3, 5), (3, 6), (4, 0), (4, 2), (4, 3), (4, 4), (5, 0), (5, 1), (5, 3), (5, 5), (5, 6), (6, 1), (6, 4)]
    
    blaa = []
    for mon in monkeys:
        blaa.append(mon)
    
    assert blaa == answer

def test_monkey_decisions():
    directions = ['north', 'south', 'west', 'east']
    lines = ['....#..', '..###.#', '#...#.#', '.#...##', '#.###..', '##.#.##', '.#..#..']
    (monkeys,map) = Get_Monkeys(lines) 
    for mon in monkeys:
        decision = Decision(mon,monkeys,directions)
        monkeys[mon].action = decision[0]
    
    output = {}
    for mon in monkeys:
        output[mon] = vars(monkeys[mon])

    assert output == {(0, 4): {'y': 0, 'x': 4, 'action': 'north', 'target': (-1, 4)}, (1, 2): {'y': 1, 'x': 2, 'action': 'north', 'target': (0, 2)}, (1, 3): {'y': 1, 'x': 3, 'action': 'nothing', 'target': None}, (1, 4): {'y': 1, 'x': 4, 'action': 'east', 'target': (1, 5)}, (1, 6): {'y': 1, 'x': 6, 'action': 'north', 'target': (0, 6)}, (2, 0): {'y': 2, 'x': 0, 'action': 'north', 'target': (1, 0)}, (2, 4): {'y': 2, 'x': 4, 'action': 'nothing', 'target': None}, (2, 6): {'y': 2, 'x': 6, 'action': 'east', 'target': (2, 7)}, (3, 1): {'y': 3, 'x': 1, 'action': 'nothing', 'target': None}, (3, 5): {'y': 3, 'x': 5, 'action': 'nothing', 'target': None}, (3, 6): {'y': 3, 'x': 6, 'action': 'south', 'target': (4, 6)}, (4, 0): {'y': 4, 'x': 0, 'action': 'west', 'target': (4, -1)}, (4, 2): {'y': 4, 'x': 2, 'action': 'nothing', 'target': None}, (4, 3): {'y': 4, 'x': 3, 'action': 'north', 'target': (3, 3)}, (4, 4): {'y': 4, 'x': 4, 'action': 'nothing', 'target': None}, (5, 0): {'y': 5, 'x': 0, 'action': 'west', 'target': (5, -1)}, (5, 1): {'y': 5, 'x': 1, 'action': 'nothing', 'target': None}, (5, 3): {'y': 5, 'x': 3, 'action': 'nothing', 'target': None}, (5, 5): {'y': 5, 'x': 5, 'action': 'nothing', 'target': None}, (5, 6): {'y': 5, 'x': 6, 'action': 'north', 'target': (4, 6)}, (6, 1): {'y': 6, 'x': 1, 'action': 'south', 'target': (7, 1)}, (6, 4): {'y': 6, 'x': 4, 'action': 'south', 'target': (7, 4)}}