'''
test.py - Run all ColorPy test cases.

Functions:

test() -
    Run all the test cases.

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
import test_colormodels
import test_ciexyz
import test_illuminants
import test_blackbody
import test_rayleigh
import test_thinfilm

def test ():
    # no test cases for plots/misc - but figures.py will exercise those.
    test_colormodels.test()
    test_ciexyz.test()
    test_illuminants.test()
    test_blackbody.test()
    test_rayleigh.test()
    test_thinfilm.test()
    
    
