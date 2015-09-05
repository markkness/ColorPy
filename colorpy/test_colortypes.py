'''
test_colortypes.py - Test routines for colortypes.py.

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
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import unittest

import colortypes


class TestColorpyConstructors(unittest.TestCase):
    ''' Test cases for colortypes constructors. '''

    def test_construct_xyz(self, verbose=True):
        ''' Test of xyz color constructors. '''
        xyz1 = colortypes.xyz_color(0.1, 0.2, 0.3)
        xyz2 = colortypes.xyz_color_from_xyY(0.33, 0.55, 0.8)
        # Test sum normalization.
        colortypes.xyz_normalize(xyz1)
        sum_xyz = xyz1[0] + xyz1[1] + xyz1[2]
        self.assertAlmostEqual(sum_xyz, 1.0)
        # Test Y normalization.
        colortypes.xyz_normalize_Y1(xyz2)
        self.assertAlmostEqual(xyz2[1], 1.0)

    def test_coverage_rgb(self, verbose=True):
        ''' Coverage test of rgb color constructors. '''
        rgb = colortypes.rgb_color(-0.1, 0.7, 2.4)
        irgb = colortypes.irgb_color(14, -9, 325)
        del rgb, irgb

    def test_coverage_percept(self, verbose=True):
        ''' Coverage test of lab,luv color constructors. '''
        lab = colortypes.lab_color(0.8, -0.15, 0.23)
        luv = colortypes.luv_color(0.36, 0.33, -0.5)
        del lab, luv


if __name__ == '__main__':
    unittest.main()
