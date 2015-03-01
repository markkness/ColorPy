'''
test_thinfilm.py - Test module for thinfilm.py.

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

import numpy
import random
import unittest

import illuminants
import thinfilm


class TestThinFilm(unittest.TestCase):
    ''' Test cases for thin film scattering. '''

    def get_films(self, num):
        ''' Get some thin films. '''
        films = []
        for i in range(num):
            n1 = 5.0 * random.random()
            n2 = 5.0 * random.random()
            n3 = 5.0 * random.random()
            thickness_nm = 10000.0 * random.random()
            film = thinfilm.thin_film (n1, n2, n3, thickness_nm)
            films.append(film)
        return films

    def get_wls(self, num):
        ''' Get some wavelengths. '''
        wls = []
        for i in range(num):
            wl_nm = 1000.0 * random.random()
            wls.append(wl_nm)
        return wls

    def test_coverage(self):
        ''' A coverage test of thin film scattering. '''
        illum = illuminants.get_illuminant_D65()
        films = self.get_films(20)
        for film in films:
            wls = self.get_wls(20)
            for wl in wls:
                film.get_interference_reflection_coefficient (wl)
            film.get_reflection_spectrum ()
            film.get_illuminated_spectrum (illum)
            film.get_illuminated_color (illum)

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
        illum = illuminants.get_illuminant_D65()
        illum_old = illuminants.get_illuminant_D65_old()
        films = self.get_films(20)
        for film in films:
            # Reflection spectrum should match.
            spect_old = film.reflection_spectrum_old()
            spect_new = film.get_reflection_spectrum()
            self.check_old_spectrum(spect_old, spect_new, tolerance)
            # Spectrum under illumination should match.
            spect_old = film.illuminated_spectrum_old (illum_old)
            spect_new = film.get_illuminated_spectrum (illum)
            self.check_old_spectrum(spect_old, spect_new, tolerance)
            # Color under illumination should match.
            color_old = film.illuminated_color_old (illum_old)
            color_new = film.get_illuminated_color (illum)
            self.check_color(color_old, color_new, tolerance, verbose)


if __name__ == '__main__':
    unittest.main()
