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

import random

import rayleigh
import illuminants

def test ():
    '''Mainly call some functions.'''
    for i in range (0, 100):
        wl_nm = 1000.0 * random.random()
        rayleigh.rayleigh_scattering (wl_nm)
    rayleigh.rayleigh_scattering_spectrum()
    illum = illuminants.get_illuminant_D65()
    rayleigh.rayleigh_illuminated_spectrum (illum)
    rayleigh.rayleigh_illuminated_color (illum)
    print ('test_rayleigh.test() passed.')  # didnt exception


if __name__ == '__main__':
    test()
