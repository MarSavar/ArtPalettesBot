import pytest
import os

from art_functions import *

def test_clamp():
    assert clamp(50) == 50

def test_clamp2():
    assert clamp(0) == 0

def test_clamp3():
    assert clamp(255) == 255

def test_clamp4():
    assert clamp(1000) == 255

def test_clamp4():
    assert clamp(-100) == 0

def test_get_random_work1():
    work = get_random_work(0,10)
    assert 'id' in work.keys() and 'title' in work.keys() and 'year' in work.keys() and 'artistName' in work.keys()

def test_get_random_work2():
    work = get_random_work(100,200)
    assert 'image' in work.keys()

def test_get_random_work3():
    work = get_random_work(400,2000)
    assert 'width' in work.keys() and 'height' in work.keys()

def test_parse_details1():
    work = get_random_work(0,100)
    keys = work.keys()
    assert 'title' in keys

def test_parse_details2():
    work = get_random_work(0,100)
    keys = work.keys()
    assert 'artist name' in keys

def test_parse_details3():
    work = get_random_work(0,100)
    keys = work.keys()
    assert 'year' in keys

def test_parse_details4():
    work = get_random_work(0,100)
    keys = work.keys()
    assert 'work' in keys