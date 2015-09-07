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

    def check_irgb_string(self, irgb, verbose):
        ''' Convert back and forth from irgb and irgb_string. '''
        irgb_string = clipping.irgb_string_from_irgb (irgb)
        irgb2 = clipping.irgb_from_irgb_string (irgb_string)
        irgb_string2 = clipping.irgb_string_from_irgb (irgb2)
        # Values should match.
        self.assertEqual(irgb[0], irgb2[0])
        self.assertEqual(irgb[1], irgb2[1])
        self.assertEqual(irgb[2], irgb2[2])
        # String should match.
        self.assertEqual(irgb_string, irgb_string2)
        msg = 'irgb: %s    irgb2: %s        irgb_string: %s    irgb_string2: %s' % (
            str(irgb), str(irgb2), irgb_string, irgb_string2)
        if verbose:
            print (msg)

    def test_irgb_string(self, verbose=False):
        ''' Convert back and forth from irgb and irgb_string. '''
        for i in range (20):
            ir = random.randrange (0, 256)
            ig = random.randrange (0, 256)
            ib = random.randrange (0, 256)
            irgb = colortypes.irgb_color (ir, ig, ib)
            self.check_irgb_string(irgb, verbose)


if __name__ == '__main__':
    unittest.main()
