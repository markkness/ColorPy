'''
test_gamma.py - Test routines for gamma.py.

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
import random
import unittest

import colormodels
import gamma


class TestGammaCorrection(unittest.TestCase):
    ''' Test cases for gamma correction functions. '''

    def check_gamma_correction(self, converter, x, verbose):
        ''' Check if the current gamma correction is consistent. '''
        a = converter.linear_from_display (x)
        y = converter.display_from_linear (a)
        b = converter.linear_from_display (y)
        # Check errors.
        abs_err1 = math.fabs (y - x)
        rel_err1 = math.fabs (abs_err1 / (y + x))
        abs_err2 = math.fabs (b - a)
        rel_err2 = math.fabs (abs_err2 / (b + a))
        msg1 = 'x = %g, y = %g, err = %g, rel = %g' % (x, y, abs_err1, rel_err1)
        msg2 = 'a = %g, b = %g, err = %g, rel = %g' % (a, b, abs_err2, rel_err2)
        if verbose:
            print (msg1)
            print (msg2)
        tolerance = 1.0e-14
        self.assertLessEqual(rel_err1, tolerance)
        self.assertLessEqual(rel_err2, tolerance)

    def check_gamma_correction_num(self, converter, num, verbose):
        ''' Check if the current gamma correction is consistent. '''
        for i in range (num):
            x = 10.0 * (2.0 * random.random() - 1.0)
            self.check_gamma_correction(converter, x, verbose)

    def test_gamma_srgb(self, verbose=False):
        ''' Test sRGB gamma correction formula. '''
        msg = 'Testing GammaConverterSrgb():'
        if verbose:
            print (msg)
        converter = gamma.GammaConverterSrgb()
        self.check_gamma_correction_num(converter, 20, verbose)

    def test_gamma_power(self, verbose=False):
        ''' Test simple power law gamma correction (can supply exponent). '''
        gamma_set = [0.1, 0.5, 1.0, 1.1, 1.5, 2.0, 2.2, 2.5, 10.0]
        for gamma_value in gamma_set:
            msg = 'Testing GammaConverterPower(gamma=%g):' % (gamma_value)
            if verbose:
                print (msg)
            converter = gamma.GammaConverterPower(gamma=gamma_value)
            self.check_gamma_correction_num(converter, 5, verbose)

    def test_gamma_function(self, verbose=False):
        ''' Test gamma correction with arbitrary functions. '''
        msg = 'Testing GammaConverterFunction():'
        if verbose:
            print (msg)
        # Use srgb standard functions.
        converter = gamma.GammaConverterFunction(
            display_from_linear_function=gamma.srgb_gamma_invert,
            linear_from_display_function=gamma.srgb_gamma_correct)
        self.check_gamma_correction_num(converter, 20, verbose)

    def check_converters_equal(self,
        converter1, converter2, x, y,
        tolerance1=0.0,
        tolerance2=0.0,
        verbose=True):
        ''' Check that the two GammaCorrector objects give the same result. '''
        # FIXME: Confirm direction consistency.
        # Direction 1.
        y1 = converter1.linear_from_display(x)
        y2 = converter2.linear_from_display(x)
        error1 = math.fabs(y2 - y1)
        msg1 = 'x=%g    y1=%g  y2=%g    error=%g' % (x, y1, y2, error1)
        if verbose:
            print (msg1)
        self.assertLessEqual(error1, tolerance1)
        # Direction 2.
        x1 = converter1.display_from_linear(y)
        x2 = converter2.display_from_linear(y)
        error2 = math.fabs(x2 - x1)
        msg2 = 'y=%g    x1=%g  x2=%g    error=%g' % (y, x1, x2, error2)
        if verbose:
            print (msg2)
        self.assertLessEqual(error2, tolerance2)

    def test_srgb_vs_hybrid(self, verbose=True):
        ''' Test the explicit sRGB converter against a hybrid with the same parameters. '''
        srgb_converter1 = gamma.GammaConverterSrgb()
        srgb_converter2 = gamma.GammaConverterHybrid(
            gamma=2.4, a=0.055, K0=0.03928, Phi=12.92, improve=False)
        num = 20
        for i in range (num):
            x = 1.2 * random.random() - 0.2
            y = 1.2 * random.random() - 0.2
            self.check_converters_equal(
                srgb_converter1, srgb_converter2, x, y, verbose=verbose)
        # Allow K0, Phi adjustment. We will need some tolerance.
        srgb_converter2 = gamma.GammaConverterHybrid(
            gamma=2.4, a=0.055, K0=0.03928, Phi=12.92, improve=True)
        num = 20
        tolerance1 = 1.0e-5
        tolerance2 = 1.0e-2
        for i in range (num):
            x = 1.2 * random.random() - 0.2
            y = 1.2 * random.random() - 0.2
            self.check_converters_equal(
                srgb_converter1, srgb_converter2, x, y,
                tolerance1=tolerance1,
                tolerance2=tolerance2,
                verbose=verbose)

    def test_srgb_coverage(self, verbose=True):
        ''' Coverage test in both linear and exponential regions. '''
        srgb_converter = gamma.GammaConverterHybrid(
            gamma=2.4, a=0.055, K0=0.03928, Phi=12.92)
        x1 = 0.00005    # Linear range.
        self.check_gamma_correction(srgb_converter, x1, verbose)
        x2 = 0.5        # Pseudo-exponential range.
        self.check_gamma_correction(srgb_converter, x2, verbose)

    def test_color_converter_srgb(self, verbose=True):
        ''' Test that conversions via the ColorConverter and GammaConverter are the same. '''
        color_converter = colormodels.ColorConverter(
            gamma_method=gamma.GAMMA_CORRECT_SRGB)
        gamma_converter = gamma.GammaConverterSrgb()
        values = [-0.05, 0.00005, 0.0005, 0.005, 0.05, 0.5, 5.0]
        tolerance = 0.0
        for value in values:
            # Direction 1.
            x1 = color_converter.gamma_display_from_linear_component(value)
            x2 = gamma_converter.display_from_linear(value)
            error1 = math.fabs(x2 - x2)
            msg1 = 'y=%g    x1=%g  x2=%g    error=%g' % (value, x1, x2, error1)
            if verbose:
                print (msg1)
            self.assertLessEqual(error1, tolerance)
            # Direction 2.
            y1 = color_converter.gamma_linear_from_display_component(value)
            y2 = gamma_converter.linear_from_display(value)
            error2 = math.fabs(y2 - y2)
            msg2 = 'x=%g    y1=%g  y2=%g    error=%g' % (value, y1, y2, error2)
            if verbose:
                print (msg2)
            self.assertLessEqual(error2, tolerance)

    # More tests to do:
    # Functions are inverses.
    # Sensible boundary conditions.
    # Matches existing srgb and simple gamma corrections.
    # Consistency of precomputed constants.


if __name__ == '__main__':
    unittest.main()
