'''
test_ciexyz.py - Test module for ciexyz.py.

License:

Copyright (C) 2008 Mark Kness

Author - Mark Kness - mkness@alumni.utexas.net

This file is part of ColorPy.

ColorPy is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as
published by the Free Software Foundation, either version 3 of
the License, or (at your option) any later version.

ColorPy is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with ColorPy.  If not, see <http://www.gnu.org/licenses/>.
'''
from __future__ import print_function

import random
import unittest

import ciexyz


class TestCiexyz(unittest.TestCase):
    ''' Test cases for CIE XYZ conversions. '''

    def test_coverage_1(self, verbose=False):
        ''' A coverage test. '''
        for i in range (100):
            wl_nm = 1000.0 * random.random()
            xyz = ciexyz.xyz_from_wavelength (wl_nm)
            msg = 'wl_nm = %7.3f, xyz = %s' % (wl_nm, str (xyz))
            if verbose:
                print (msg)

    def test_coverage_2(self, verbose=False):
        ''' Another coverage test. '''
        empty = ciexyz.empty_spectrum ()
        xyz = ciexyz.xyz_from_spectrum (empty)
        if verbose:
            print ('black = %s' % (str (xyz)))
        xyz_555 = ciexyz.xyz_from_wavelength (555.0)
        if verbose:
            print ('555 nm = %s' % (str (xyz_555)))


if __name__ == '__main__':
    unittest.main()
