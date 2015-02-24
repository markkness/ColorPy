'''
test_illuminants.py - Test module for illuminants.py.

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

import numpy
import unittest

import illuminants


class TestIlluminants(unittest.TestCase):
    ''' Test cases for illuminants. '''

    def test_illuminant_A(self, verbose=False):
        ''' Test that Illuminant A matches the correct blackbody. '''
        T_A = 2856.0
        i1 = illuminants.get_illuminant_A()
        i2 = illuminants.get_blackbody_illuminant (T_A)
        # Wavelengths should match.
        tol = 1.0e-16
        ok = numpy.allclose (i1.wavelength, i2.wavelength, atol=tol)
        self.assertTrue(ok)
        # Intensity should match
        tol = 1.0e-16
        ok = numpy.allclose (i1.intensity, i2.intensity, atol=tol)
        self.assertTrue(ok)

    def check_Y(self, illum, expect, tolerance, verbose):
        ''' Check that Y=1.0 for the illuminant. '''
        xyz = illum.get_xyz()
        Y = xyz[1]
        msg = 'Y: %g    expected: %g' % (Y, expect)
        if verbose:
            print (msg)
        self.assertAlmostEqual(Y, expect, delta=tolerance)

    def test_Y(self, verbose=False):
        ''' Test that standard illuminants have Y=1.0. '''
        tolerance = 1.0e-14
        expect = 1.0
        # D65
        D65 = illuminants.get_illuminant_D65()
        self.check_Y(D65, expect, tolerance, verbose)
        # A
        A = illuminants.get_illuminant_A()
        self.check_Y(A, expect, tolerance, verbose)
        # Constant
        c = illuminants.get_constant_illuminant()
        self.check_Y(c, expect, tolerance, verbose)
        # Neon lamp.
        neon = illuminants.get_neon_illuminant()
        self.check_Y(neon, expect, tolerance, verbose)
        # Blackbodies of a few temperatures.
        T_list = [100.0, 1000.0, 5000.0, 9000.0, 1.0e6]
        for T in T_list:
            black = illuminants.get_blackbody_illuminant (T)
            self.check_Y(black, expect, tolerance, verbose)
        # But T=0 should return pure black without trouble.
        black = illuminants.get_blackbody_illuminant (0.0)
        expect = 0.0
        self.check_Y(black, expect, tolerance, verbose)

    def check_old_illuminant(self, old_illum, new_illum, tolerance):
        ''' Old-style and new-style illuminants should return exactly the same values. '''
        ok = numpy.allclose(old_illum[:,0], new_illum.wavelength, atol=tolerance)
        self.assertTrue(ok)
        ok = numpy.allclose(old_illum[:,1], new_illum.intensity, atol=tolerance)
        self.assertTrue(ok)

    def test_old_illuminants(self, verbose=False):
        ''' Old-style and new-style illuminants should return exactly the same values. '''
        tol = 0.0
        # D65
        new_D65 = illuminants.get_illuminant_D65()
        old_D65 = illuminants.get_illuminant_D65_old()
        self.check_old_illuminant(old_D65, new_D65, tol)
        # A
        new_A = illuminants.get_illuminant_A()
        old_A = illuminants.get_illuminant_A_old()
        self.check_old_illuminant(old_A, new_A, tol)
        # constant
        new_const = illuminants.get_constant_illuminant()
        old_const = illuminants.get_constant_illuminant_old()
        self.check_old_illuminant(old_const, new_const, tol)
        # Blackbodies of a few temperatures.
        T_list = [1000.0, 9000.0]
        for T in T_list:
            new_black = illuminants.get_blackbody_illuminant (T)
            old_black = illuminants.get_blackbody_illuminant_old (T)
            self.check_old_illuminant(old_black, new_black, tol)


if __name__ == '__main__':
    unittest.main()
