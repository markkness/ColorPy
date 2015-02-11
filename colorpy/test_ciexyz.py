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
import random

import ciexyz

def test (verbose=0):
    '''Test the CIE XYZ conversions.  Mainly call some functions.'''
    for i in range (0, 100):
        wl_nm = 1000.0 * random.random()
        xyz = ciexyz.xyz_from_wavelength (wl_nm)
        if verbose >= 1:
            print 'wl_nm = %g, xyz = %s' % (wl_nm, str (xyz))
    for i in range (0, 10):
        empty = ciexyz.empty_spectrum ()
        xyz = ciexyz.xyz_from_spectrum (empty)
        if verbose >= 1:
            print 'black = %s' % (str (xyz))
        xyz_555 = ciexyz.xyz_from_wavelength (555.0)
        if verbose >= 1:
            print '555 nm = %s' % (str (xyz_555))
    print 'test_ciexyz.test() passed.'
