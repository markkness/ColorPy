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
from __future__ import print_function

import unittest

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
    test_rayleigh.test()
    test_thinfilm.test()
    # Explicitly run the unittest cases in the modules.
    # This is perhaps a bit clumsy.
    result = unittest.TestResult()
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(test_blackbody)
    suite.run(result)
    result_txt = str(result)
    print (result_txt)
    # Raise an exception if there were problems.
    ok = (len(result.errors) == 0) and (len(result.failures) == 0)
    if not ok:
        msg = 'Test Suite Errors: %s    Failures: %s' % (
            result.errors, result.failures)
        # Perhaps not the right exception type...
        print (msg)
        raise ValueError(msg)

if __name__ == '__main__':
    test()
