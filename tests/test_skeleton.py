#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from BFXLight.skeleton import fib

__author__ = "Flávio Codeço Coelho"
__copyright__ = "Flávio Codeço Coelho"
__license__ = "gpl3"


def test_fib():
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(7) == 13
    with pytest.raises(AssertionError):
        fib(-10)
