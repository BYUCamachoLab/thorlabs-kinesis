# -*- coding: utf-8 -*-
#
# Copyright © Thorlabs-Kinesis Project Contributors
# Licensed under the terms of the GNU GPLv3+ License
# (see thorlabs_kinesis/__init__.py for details)

"""
Utilities
---------

Utility functions.
"""

from ctypes import (
    CDLL,
    CFUNCTYPE,
    c_ushort,
    c_ulong,
)
from typing import (
    Any,
    List,
)

c_word = c_ushort
c_dword = c_ulong


def bind(lib: CDLL, func: str,
         argtypes: List[Any]=None, restype: Any=None) -> CFUNCTYPE:
    _func = getattr(lib, func, null_function)
    _func.argtypes = argtypes
    _func.restype = restype

    return _func


def null_function():
    pass


def not_implemented():
    raise NotImplementedError


__all__ = [
    "bind",
    "null_function",
    "c_word",
    "c_dword",
]
