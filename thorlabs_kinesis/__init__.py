# -*- coding: utf-8 -*-
# Copyright © 2020 Thorlabs-Kinesis Project Contributors and others (see AUTHORS.txt).
# The resources, libraries, and some source files under other terms (see NOTICE.txt).
#
# This file is part of Thorlabs-Kinesis.
#
# Thorlabs-Kinesis is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Thorlabs-Kinesis is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Thorlabs-Kinesis. If not, see <https://www.gnu.org/licenses/>.

"""
Thorlabs-Kinesis
================

Python bindings for Thorlabs Kinesis DLLs. 
"""

import os
import platform
import sys
from pathlib import Path

if sys.version_info < (3, 6, 0):
    raise Exception(
        "Thorlabs-Kinesis requires Python 3.6+ (version "
        + platform.python_version()
        + " detected)."
    )

__author__ = "Ertugrul Karademir"
__copyright__ = "Copyright 2020, The Thorlabs-Kinesis Project"
__version__ = "0.1.0"
__license__ = "GPLv3+"
__maintainer__ = "Sequoia Ploeg"
__maintainer_email__ = "sequoia.ploeg@ieee.org"
__status__ = "Development" # "Production"
__project_url__ = "https://github.com/BYUCamachoLab/thorlabs-kinesis"


class Configuration:
    def __init__(self):
        self._libdir = ""

    @property
    def libdir(self):
        return self._libdir

    @libdir.setter
    def libdir(self, dirs):
        self._libdir = dirs
        os.environ['PATH'] = dirs + ";" + os.environ['PATH']

config = Configuration()


if sys.platform.startswith('java'):
    import platform
    os_name = platform.java_ver()[3][0]
    if os_name.startswith('Windows'): # "Windows XP", "Windows 7", etc.
        system = 'win32'
    elif os_name.startswith('Mac'): # "Mac OS X", etc.
        system = 'darwin'
    else: # "Linux", "SunOS", "FreeBSD", etc.
        # Setting this to "linux2" is not ideal, but only Windows or Mac
        # are actually checked for and the rest of the module expects
        # *sys.platform* style strings.
        system = 'linux2'
else:
    system = sys.platform

if system != 'win32':
    raise Exception('Thorlabs-Kinesis only runs on Windows machines.')

_DEFAULT_DIR = Path('C:/Program Files/Thorlabs/Kinesis')
_DEFAULT_USER_DIR = Path('')
if _DEFAULT_DIR.exists():
    config.libdir = str(_DEFAULT_DIR)
elif _DEFAULT_USER_DIR.exists():
    config.libdir = str(_DEFAULT_USER_DIR)
else:
    import warnings
    warnings.warn('ThorLabs Kinesis installation not located, be sure to \
        add the required DLLs to the system path or set the \
        `thorlabs_kinesis.config.libdir` attribute BEFORE importing any \
        submodules from thorlabs_kinesis')
