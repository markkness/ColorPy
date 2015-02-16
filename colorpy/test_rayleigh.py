'''
test_rayleigh.py - Test module for rayleigh.py.

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

import math
import numpy
import random
import unittest

import ciexyz
import rayleigh
import illuminants


class TestRayleigh(unittest.TestCase):
    ''' Test cases for Rayleigh scattering. '''

    def test_wavelength_4(self, verbose=False):
        ''' Test that scattering scales as 1/wl^4. '''
        for i in range(20):
            # Two random wavelengths, avoiding zero.
            wl_1 = 1.0 + 999.0 * random.random()
            wl_2 = 1.0 + 999.0 * random.random()
            # Scattering.
            sc_1 = rayleigh.rayleigh_scattering(wl_1)
            sc_2 = rayleigh.rayleigh_scattering(wl_2)
            # Ratios, avoiding pow() for more independence from implementation.
            r_sc  = sc_1 / sc_2
            r_wl  = wl_2 / wl_1
            r4_wl = r_wl * r_wl * r_wl * r_wl
            # Check.
            actual = r_sc / r4_wl
            expect = 1.0
            error = math.fabs(actual - expect)
            tolerance = 1.0e-12
            self.assertLessEqual(error, tolerance)
            msg = 'Wavelength: %g, %g    Scattering: %g, %g    Ratio of Powers: %.8f' % (
                wl_1, wl_2, sc_1, sc_2, actual)
            if verbose:
                print (msg)

    def test_scattering(self, verbose=False):
        ''' Test of scattering calculations. '''
        # Coverage test of get_rayleigh_scattering_spectrum().
        rayleigh.get_rayleigh_scattering_spectrum()
        illum = illuminants.get_illuminant_D65()
        spect = rayleigh.get_rayleigh_illuminated_spectrum (illum)
        # Both color calculations should give the same result.
        xyz1 = spect.get_xyz()
        xyz2 = rayleigh.get_rayleigh_illuminated_color (illum)
        msg = 'D65 Rayleigh scattered xyz: %s, %s' % (str(xyz1), str(xyz2))
        if verbose:
            print (msg)
        atol = 1.0e-16
        ok = numpy.allclose(xyz1, xyz2, atol=atol)
        self.assertTrue(ok)


if __name__ == '__main__':
    unittest.main()
