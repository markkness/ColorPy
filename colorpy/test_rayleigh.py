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
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import math
import numpy
import random
import unittest

import rayleigh
import illuminants


class TestRayleigh(unittest.TestCase):
    ''' Test cases for Rayleigh scattering. '''

    def test_red_blue(self, verbose=False):
        ''' Test that blue light scatters more than red. '''
        wl_blue = 400.0
        wl_red  = 700.0
        sc_blue = rayleigh.rayleigh_scattering(wl_blue)
        sc_red  = rayleigh.rayleigh_scattering(wl_red)
        msg = 'Blue %.1f nm scatters: %g    Red %.1f scatters: %g' % (
            wl_blue, sc_blue, wl_red, sc_red)
        if verbose:
            print (msg)
        self.assertGreater(sc_blue, sc_red)

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
        illum = illuminants.get_illuminant_D65()
        spect = rayleigh.get_rayleigh_illuminated_spectrum (illum)
        # Both color calculations should give the same result.
        xyz1 = spect.get_xyz()
        xyz2 = rayleigh.get_rayleigh_illuminated_color (illum)
        atol = 1.0e-16
        self.check_color(xyz1, xyz2, atol, verbose)

    def check_color(self, xyz1, xyz2, tolerance, verbose):
        ''' Check if the colors match. '''
        msg = 'xyz1: %s    xyz2: %s' % (str(xyz1), str(xyz2))
        if verbose:
            print (msg)
        ok = numpy.allclose(xyz1, xyz2, atol=tolerance)
        self.assertTrue(ok)

    def check_old_spectrum(self, old_spect, new_spect, tolerance):
        ''' Old-style and new-style spectra should return the same values. '''
        ok = numpy.allclose(old_spect[:,0], new_spect.wavelength, atol=tolerance)
        self.assertTrue(ok)
        ok = numpy.allclose(old_spect[:,1], new_spect.intensity, atol=tolerance)
        self.assertTrue(ok)

    def test_old(self, verbose=False):
        ''' Test the old-style functions. '''
        tolerance = 0.0
        # Scattering spectrum should match.
        ray_old = rayleigh.rayleigh_scattering_spectrum_old()
        ray_new = rayleigh.get_rayleigh_scattering_spectrum()
        self.check_old_spectrum(ray_old, ray_new, tolerance)
        # Spectrum under illumination should match.
        illum_old = illuminants.get_illuminant_D65_old()
        illum_new = illuminants.get_illuminant_D65()
        spec_old = rayleigh.rayleigh_illuminated_spectrum_old (illum_old)
        spec_new = rayleigh.get_rayleigh_illuminated_spectrum (illum_new)
        self.check_old_spectrum(spec_old, spec_new, tolerance)
        # Color under illumination should match.
        color_old = rayleigh.rayleigh_illuminated_color_old (illum_old)
        color_new = rayleigh.get_rayleigh_illuminated_color (illum_new)
        self.check_color(color_old, color_new, tolerance, verbose)


if __name__ == '__main__':
    unittest.main()
