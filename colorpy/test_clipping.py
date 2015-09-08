'''
test_clipping.py - Test routines for clipping.py.

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

import random
import unittest

import clipping
import colortypes


class TestClipping(unittest.TestCase):
    ''' Test cases for color clipping and integer conversions. '''

    def get_irgb_values(self, num_range=256, count=20):
        ''' Get some random irgb values. '''
        values = []
        for i in range(count):
            ir = random.randrange (0, num_range)
            ig = random.randrange (0, num_range)
            ib = random.randrange (0, num_range)
            irgb = colortypes.irgb_color (ir, ig, ib)
            values.append(irgb)
        return values

    def check_hexstring_conversions(self, irgb, num_digits, verbose):
        ''' Convert back and forth from irgb and hexstring. '''
        hexstring  = clipping.hexstring_from_irgb (irgb, num_digits)
        irgb2      = clipping.irgb_from_hexstring (hexstring)
        hexstring2 = clipping.hexstring_from_irgb (irgb2, num_digits)
        # Values should match.
        self.assertEqual(irgb[0], irgb2[0])
        self.assertEqual(irgb[1], irgb2[1])
        self.assertEqual(irgb[2], irgb2[2])
        # String should match.
        self.assertEqual(hexstring, hexstring2)
        msg = 'irgb: %-16s    irgb2: %-16s        hexstring: %-10s    hexstring2: %-10s' % (
            str(irgb), str(irgb2), hexstring, hexstring2)
        if verbose: print (msg)

    def test_hexstring_conversions(self, verbose=False):
        ''' Test conversions between irgb and hexstring. '''
        if verbose: print('test_hexstring_conversions():')
        values = self.get_irgb_values(num_range=256, count=10)
        for irgb in values:
            self.check_hexstring_conversions(irgb, 2, verbose)
            self.check_hexstring_conversions(irgb, 3, verbose)
        values = self.get_irgb_values(num_range=16*256, count=10)
        for irgb in values:
            self.check_hexstring_conversions(irgb, 3, verbose)

    def check_hexstring_from_irgb(self, ir, ig, ib, hexstring, num_digits, verbose):
        ''' Check that the rgb values produce the expected hexstring. '''
        irgb = colortypes.irgb_color (ir, ig, ib)
        hexstring_actual = clipping.hexstring_from_irgb (irgb, num_digits)
        msg = 'r: %3d    g: %3d    b: %3d    hexstring: %-10s    expected: %-10s' % (
            ir, ig, ib, hexstring_actual, hexstring)
        if verbose: print (msg)
        self.assertEqual(hexstring_actual, hexstring)

    def test_hexstring_from_irgb(self, verbose=False):
        ''' Test that the rgb values produce the hexstring. '''
        if verbose: print('test_hexstring_from_irgb():')
        # 2-digits per component.
        values2 = [
            ( 255,  255,  255, '#FFFFFF'),
            (0x12, 0x34, 0xEA, '#1234EA'),
            # Test clipping.
            ( 256,  255,   -1, '#FFFF00'),
            ( -12,  666,  -12, '#00FF00'),
        ]
        for ir, ig, ib, hexstring in values2:
            self.check_hexstring_from_irgb(ir, ig, ib, hexstring, 2, verbose)
        # 3-digits per component.
        values3 = [
            (255,  255,  255, '#0FF0FF0FF'),
            (256,  257,  258, '#100101102'),
        ]
        for ir, ig, ib, hexstring in values3:
            self.check_hexstring_from_irgb(ir, ig, ib, hexstring, 3, verbose)


if __name__ == '__main__':
    unittest.main()
