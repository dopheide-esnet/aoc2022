
import pytest

from aoc20 import Unmix,Coordinates,Embiggen_and_Prep,Big_Unmixer

def test_truth():
    assert True

def test_test_input():
    lines = ['1','2','-3','3','-2','0','4']
    my_list = Unmix(lines)
    assert my_list == [{'num': 1, 'moved': True}, {'num': 2, 'moved': True}, {'num': -3, 'moved': True}, {'num': 4, 'moved': True}, {'num': 0, 'moved': True}, {'num': 3, 'moved': True}, {'num': -2, 'moved': True}]

def test_coordinates():
    my_list = [{'num': 1, 'moved': True}, {'num': 2, 'moved': True}, {'num': -3, 'moved': True}, {'num': 4, 'moved': True}, {'num': 0, 'moved': True}, {'num': 3, 'moved': True}, {'num': -2, 'moved': True}]
    assert Coordinates(my_list) == 3

def test_multi_wrap():
    lines = ['1','2','-3','3','-2','0','20']
    my_list = Unmix(lines)
    assert my_list == [{'num': 1, 'moved': True}, {'num': 20, 'moved': True}, {'num': 2, 'moved': True}, {'num': -3, 'moved': True}, {'num': 0, 'moved': True}, {'num': 3, 'moved': True}, {'num': -2, 'moved': True}]

def test_embiggen():
    lines = ['1','2','-3','3','-2','0','4']
    my_list = Embiggen_and_Prep(lines)
    assert my_list == [{'num': 811589153, 'moved': False, 'order': 0}, {'num': 1623178306, 'moved': False, 'order': 1}, {'num': -2434767459, 'moved': False, 'order': 2}, {'num': 2434767459, 'moved': False, 'order': 3}, {'num': -1623178306, 'moved': False, 'order': 4}, {'num': 0, 'moved': False, 'order': 5}, {'num': 3246356612, 'moved': False, 'order': 6}]

def test_big_unmix_1():
    lines = ['1','2','-3','3','-2','0','4']
    my_list = Embiggen_and_Prep(lines)
    Big_Unmixer(my_list, 1)
    assert my_list == [{'num': 0, 'moved': True, 'order': 5}, {'num': -2434767459, 'moved': True, 'order': 2}, {'num': 3246356612, 'moved': True, 'order': 6}, {'num': -1623178306, 'moved': True, 'order': 4}, {'num': 2434767459, 'moved': True, 'order': 3}, {'num': 1623178306, 'moved': True, 'order': 1}, {'num': 811589153, 'moved': True, 'order': 0}]
