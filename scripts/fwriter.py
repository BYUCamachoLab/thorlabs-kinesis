#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © Thorlabs-Kinesis Project Contributors
# Licensed under the terms of the GNU GPLv3+ License
# (see thorlabs_kinesis/__init__.py for details)

"""
Function Writer
===============

This script can create the bound functions by parsing copied and pasted 
documentation.
"""

docs = ""

funcs = [a for a in docs.split() if a.startswith('CC_') or a.startswith('TLI_')]
for f in funcs:
    print(f)
