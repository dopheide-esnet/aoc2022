
import pytest

from aoc20 import Unmix,Coordinates

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
