import pytest
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