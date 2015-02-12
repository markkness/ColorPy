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
from __future__ import print_function

import random
import unittest

import illuminants
import thinfilm


class TestThinFilm(unittest.TestCase):
    ''' Test cases for thin film scattering. '''

    def test_coverage(self):
        ''' A coverage test of thin film scattering. '''
        illuminant = illuminants.get_illuminant_D65()
        for j in range (20):
            n1 = 5.0 * random.random()
            n2 = 5.0 * random.random()
            n3 = 5.0 * random.random()
            thickness_nm = 10000.0 * random.random()
            film = thinfilm.thin_film (n1, n2, n3, thickness_nm)
            for k in range (20):
                wl_nm = 1000.0 * random.random()
                film.get_interference_reflection_coefficient (wl_nm)
            film.reflection_spectrum ()
            film.illuminated_spectrum (illuminant)
            film.illuminated_color (illuminant)


if __name__ == '__main__':
    unittest.main()
