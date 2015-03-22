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
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import unittest

import test_colormodels
import test_ciexyz
import test_illuminants
import test_blackbody
import test_plots
import test_purecolors
import test_rayleigh
import test_thinfilm

def test ():
    # No test cases for examples - but figures.py will exercise those.
    # Explicitly run the unittest cases in the modules.
    # This is perhaps a bit clumsy.
    # A more conventional way to run all of the tests, is at the command line:
    #     python -m unittest discover
    modules = [
        test_blackbody,
        test_ciexyz,
        test_colormodels,
        test_illuminants,
        test_rayleigh,
        test_plots,
        test_purecolors,
        test_thinfilm,
    ]
    for module in modules:
        result = unittest.TestResult()
        loader = unittest.TestLoader()
        suite  = loader.loadTestsFromModule(module)
        suite.run(result)
        # Print results.
        msg = 'Module: %s    Errors: %s    Failures: %s' % (
            module.__name__, result.errors, result.failures)
        print (msg)
        print (str(result))
        # Raise an exception if there were problems.
        ok = (len(result.errors) == 0) and (len(result.failures) == 0)
        if not ok:
            # Perhaps not the right exception type...
            raise ValueError(msg)


if __name__ == '__main__':
    test()
