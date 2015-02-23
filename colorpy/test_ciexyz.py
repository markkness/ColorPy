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
import colormodels
import illuminants


class TestCiexyz(unittest.TestCase):
    ''' Test cases for CIE XYZ conversions. '''

    def test_coverage(self, verbose=False):
        ''' Coverage test of xyz from wavelength. '''
        for i in range (40):
            wl_nm = 1000.0 * random.random()
            xyz = ciexyz.xyz_from_wavelength (wl_nm)
            msg = 'wl_nm = %7.3f, xyz = %s' % (wl_nm, str (xyz))
            if verbose:
                print (msg)
        # And one specific wavelength.
        xyz_555 = ciexyz.xyz_from_wavelength (555.0)
        if verbose:
            print ('555 nm = %s' % (str (xyz_555)))

    def check_color(self, xyz1, xyz2, tolerance, verbose):
        ''' Check that the colors are the same. '''
        self.assertAlmostEqual(xyz1[0], xyz2[0], delta=tolerance)
        self.assertAlmostEqual(xyz1[1], xyz2[1], delta=tolerance)
        self.assertAlmostEqual(xyz1[2], xyz2[2], delta=tolerance)

    def test_black(self, verbose=False):
        ''' Test that empty spectra are black. '''
        black = colormodels.xyz_color (0.0, 0.0, 0.0)
        spect = ciexyz.Spectrum()
        xyz1 = spect.get_xyz()
        tolerance = 1.0e-12
        self.check_color(xyz1, black, tolerance, verbose)
        # Also for old-style.
        array = ciexyz.empty_spectrum()
        xyz2 = ciexyz.xyz_from_spectrum (array)
        self.check_color(xyz2, black, tolerance, verbose)

    def test_color(self, verbose=False):
        ''' Test the conversions to xyz colors for consistency. '''
        spect = illuminants.get_illuminant_A()
        # Fast and slow color calculations should match.
        xyz1 = spect.get_xyz_color_any()
        xyz2 = spect.get_xyz_color_standard()
        xyz3 = spect.get_xyz()
        tolerance = 1.0e-12
        self.check_color(xyz1, xyz2, tolerance, verbose)
        self.check_color(xyz1, xyz3, tolerance, verbose)
        # Old-style array calculation should also match.
        array = spect.to_array()
        xyz4 = ciexyz.xyz_from_spectrum (array)
        self.check_color(xyz3, xyz4, tolerance, verbose)

    def test_array_conversions(self, verbose=False):
        ''' Test conversions between Spectrum and arrays. '''
        spect1 = illuminants.get_illuminant_A()
        xyz1   = spect1.get_xyz()
        # Round-trip to array and back should not change color.
        array  = spect1.to_array()
        spect2 = ciexyz.Spectrum_from_array (array)
        xyz2   = spect2.get_xyz()
        tolerance = 1.0e-12
        self.check_color(xyz1, xyz2, tolerance, verbose)
        # Spectrum copy should not change color.
        spect3 = ciexyz.Spectrum_copy (spect1)
        xyz3   = spect3.get_xyz()
        self.check_color(xyz1, xyz3, tolerance, verbose)


if __name__ == '__main__':
    unittest.main()
