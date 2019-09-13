#!/usr/bin/env python

# OMR - Optical mark regognition
# Copyright (C) 2019 Joppe Blondel
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import argparse

from read import *
from create import *

parser = argparse.ArgumentParser(description='Parse a form with ORM')
parser.add_argument('input', metavar='I', help='The input file')
parser.add_argument('output', metavar='O', help='The output file')

def main():
    args = parser.parse_args()

if __name__ == "__main__":
    main()
