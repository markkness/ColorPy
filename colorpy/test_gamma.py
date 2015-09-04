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

    def get_values(self, x0, x1, num):
        ''' Get some random numbers, in the range x0 to x1, for tests. '''
        vals = []
        a, b = x0, x1 - x0
        for i in range(num):
            x = a + b * random.random()
            vals.append(x)
        return vals

    def check_gamma_correct(self, converter, x, verbose):
        ''' Check that gamma correction is consistent. '''
        a = converter.linear_from_display (x)
        y = converter.display_from_linear (a)
        b = converter.linear_from_display (y)
        # Check errors.
        abs_err1 = math.fabs (y - x)
        rel_err1 = math.fabs (abs_err1 / (y + x))
        abs_err2 = math.fabs (b - a)
        rel_err2 = math.fabs (abs_err2 / (b + a))
        msg1 = 'x = %.8f, y = %.8f, err = %.8f, rel = %.8f' % (x, y, abs_err1, rel_err1)
        msg2 = 'a = %.8f, b = %.8f, err = %.8f, rel = %.8f' % (a, b, abs_err2, rel_err2)
        if verbose:
            print (msg1)
            print (msg2)
        tolerance = 1.0e-14
        self.assertLessEqual(rel_err1, tolerance)
        self.assertLessEqual(rel_err2, tolerance)

    def check_gamma_invert(self, converter, a, verbose):
        ''' Check that gamma inversion is consistent. '''
        x = converter.display_from_linear (a)
        b = converter.linear_from_display (x)
        y = converter.display_from_linear (b)
        # Check errors.
        abs_err1 = math.fabs (b - a)
        rel_err1 = math.fabs (abs_err1 / (b + a))
        abs_err2 = math.fabs (y - x)
        rel_err2 = math.fabs (abs_err2 / (y + x))
        msg1 = 'a = %.8f, b = %.8f, err = %.8f, rel = %.8f' % (a, b, abs_err1, rel_err1)
        msg2 = 'x = %.8f, y = %.8f, err = %.8f, rel = %.8f' % (x, y, abs_err2, rel_err2)
        if verbose:
            print (msg1)
            print (msg2)
        tolerance = 1.0e-14
        self.assertLessEqual(rel_err1, tolerance)
        self.assertLessEqual(rel_err2, tolerance)

    def check_gamma_converter(self, converter, num, verbose):
        ''' Check that gamma correction and inversion are consistent. '''
        half_num = num // 2
        values_1 = self.get_values(-10.0, +10.0, half_num)
        values_2 = self.get_values(-10.0, +10.0, half_num)
        for value in values_1:
            self.check_gamma_correct(converter, value, verbose)
        for value in values_2:
            self.check_gamma_invert(converter, value, verbose)

    # Test the non-hybrid GammaConverter classes.

    def test_gamma_srgb(self, verbose=False):
        ''' Test sRGB gamma correction formula. '''
        if verbose: print ('test_gamma_srgb():')
        converter = gamma.GammaConverterSrgb()
        self.check_gamma_converter(converter, 10, verbose)

    def test_gamma_power(self, verbose=False):
        ''' Test simple power law gamma correction (can supply exponent). '''
        if verbose: print ('test_gamma_power():')
        gamma_set = [0.17, 0.5, 1.0, 1.3, 2.5, 10.24]
        for gamma_value in gamma_set:
            msg = 'Testing GammaConverterPower(gamma=%g):' % (gamma_value)
            if verbose:
                print (msg)
            converter = gamma.GammaConverterPower(gamma=gamma_value)
            self.check_gamma_converter(converter, 4, verbose)

    def test_gamma_function(self, verbose=False):
        ''' Test gamma correction with arbitrary functions. '''
        if verbose: print ('Testing GammaConverterFunction():')
        # Use convenient srgb standard functions.
        converter = gamma.GammaConverterFunction(
            display_from_linear_function=gamma.srgb_gamma_invert,
            linear_from_display_function=gamma.srgb_gamma_correct)
        self.check_gamma_converter(converter, 10, verbose)

    # Test GammaConverterHybrid.

    def check_gamma_converter_hybrid(self, converter, num, verbose):
        ''' Test a GammaConverterHybrid() for:
            1) That gamma correction and inversion are consistent,
               specifically over the two domains of the conversion function.
            2) That pre-computed values are consistent. '''
        # Gamma correction.
        # Pick values in linear, pseudo-exponential, and large range.
        cutoff = converter.K0
        values_1 = self.get_values(0.0, cutoff, num)
        values_2 = self.get_values(cutoff, 1.0, num)
        values_3 = self.get_values(-5.0, +10.0, num)
        for value in (values_1 + values_2 + values_3):
            self.check_gamma_correct(converter, value, verbose)
        # Gamma inversion.
        # Pick values in linear, pseudo-exponential, and large range.
        cutoff = converter.K0_over_Phi
        values_1 = self.get_values(0.0, cutoff, num)
        values_2 = self.get_values(cutoff, 1.0, num)
        values_3 = self.get_values(-5.0, +10.0, num)
        for value in (values_1 + values_2 + values_3):
            self.check_gamma_invert(converter, value, verbose)
        # Check consistency of pre-computed values.
        tolerance = 1.0e-14
        self.assertAlmostEqual(
            converter.one_plus_a, 1.0 + converter.a, delta=tolerance)
        self.assertAlmostEqual(
            converter.inv_gamma, 1.0 / converter.gamma, delta=tolerance)
        self.assertAlmostEqual(
            converter.K0_over_Phi, converter.K0 / converter.Phi, delta=tolerance)

    def test_gamma_converter_hybrid(self, verbose=False):
        if verbose: print ('test_gamma_converter_hybrid():')
        num = 6
        converters = [
            # Srgb with improved K0, Phi.
            gamma.GammaConverterHybrid(
                gamma=2.4, a=0.055, K0=0.03928, Phi=12.92, improve=True),
            # Srgb with original K0, Phi.
            gamma.GammaConverterHybrid(
                gamma=2.4, a=0.055, K0=0.03928, Phi=12.92, improve=False),
            # Explicitly defined converters.
            gamma.srgb_gamma_converter,
            gamma.uhdtv10_gamma_converter,
            gamma.uhdtv12_gamma_converter,
        ]
        for converter in converters:
            self.check_gamma_converter_hybrid(converter, num, verbose)

    # Test hybrid srgb against a reference implementation.

    def check_converters_equal(self,
        converter1,    # First GammaConverter to test.
        converter2,    # Second GammaConverter to test.
        num,           # Number of values to test.
        tolerance1,    # Tolerance for gamma correction.
        tolerance2,    # Tolerance for gamma inversion.
        verbose):
        ''' Check that the two GammaCorrector objects give the same result. '''
        # Gamma correction.
        values = self.get_values(-0.2, 1.2, num)
        for x in values:
            y1 = converter1.linear_from_display(x)
            y2 = converter2.linear_from_display(x)
            error1 = math.fabs(y2 - y1)
            msg1 = 'x=%.8f    y1=%.8f  y2=%.8f    error=%.8f' % (x, y1, y2, error1)
            if verbose:
                print (msg1)
            self.assertLessEqual(error1, tolerance1)
        # Gamma inversion.
        values = self.get_values(-0.2, 1.2, num)
        for y in values:
            x1 = converter1.display_from_linear(y)
            x2 = converter2.display_from_linear(y)
            error2 = math.fabs(x2 - x1)
            msg2 = 'y=%.8f    x1=%.8f  x2=%.8f    error=%.8f' % (y, x1, x2, error2)
            if verbose:
                print (msg2)
            self.assertLessEqual(error2, tolerance2)

    def test_srgb_vs_hybrid(self, verbose=False):
        ''' Test the explicit sRGB converter against a hybrid with the same parameters. '''
        if verbose: print ('test_srgb_vs_hybrid():')
        # First, disallow K0, Phi adjustment, to exactly match GammaConverterSrgb().
        srgb_converter1 = gamma.GammaConverterSrgb()
        srgb_converter2 = gamma.GammaConverterHybrid(
            gamma=2.4, a=0.055, K0=0.03928, Phi=12.92, improve=False)
        num = 5
        self.check_converters_equal(
            srgb_converter1, srgb_converter2, num,
            tolerance1=0.0,
            tolerance2=0.0,
            verbose=verbose)
        # Allow K0, Phi adjustment. Now we will need some tolerance.
        srgb_converter2 = gamma.GammaConverterHybrid(
            gamma=2.4, a=0.055, K0=0.03928, Phi=12.92, improve=True)
        num = 5
        tolerance1 = 1.0e-5
        tolerance2 = 1.0e-2
        self.check_converters_equal(
            srgb_converter1, srgb_converter2, num,
            tolerance1=tolerance1,
            tolerance2=tolerance2,
            verbose=verbose)

    # Test api consistency.

    def test_color_gamma_converter(self, verbose=False):
        ''' Test that conversions via the ColorConverter and GammaConverter are the same. '''
        if verbose: print ('test_color_gamma_converter():')
        # Srgb is a convenient test case.
        color_converter = colormodels.ColorConverter(
            gamma_method=gamma.GAMMA_CORRECT_SRGB)
        gamma_converter = gamma.GammaConverterSrgb()
        values = [-0.05, 0.00005, 0.0005, 0.005, 0.05, 0.5, 5.0]
        tolerance = 1.0e-14
        for value in values:
            # Direction 1.
            x1 = color_converter.display_from_linear_component(value)
            x2 = gamma_converter.display_from_linear(value)
            error1 = math.fabs(x2 - x2)
            msg1 = 'y=%.8f    x1=%.8f  x2=%.8f    error=%.8f' % (value, x1, x2, error1)
            if verbose:
                print (msg1)
            self.assertLessEqual(error1, tolerance)
            # Direction 2.
            y1 = color_converter.linear_from_display_component(value)
            y2 = gamma_converter.linear_from_display(value)
            error2 = math.fabs(y2 - y2)
            msg2 = 'x=%.8f    y1=%.8f  y2=%.8f    error=%.8f' % (value, y1, y2, error2)
            if verbose:
                print (msg2)
            self.assertLessEqual(error2, tolerance)

    def test_free_functions(self, verbose=False):
        ''' Test the legacy api free functions for gamma conversions. '''
        if verbose: print ('test_free_functions():')
        # Use power-function gamma to test that as well.
        color_converter = colormodels.ColorConverter(
            gamma_method=gamma.GAMMA_CORRECT_POWER, gamma_value=2.2)
        values = [-0.05, 0.00005, 0.0005, 0.005, 0.05, 0.5, 5.0]
        tolerance = 1.0e-14
        for value in values:
            # Direction 1.
            x1 = color_converter.display_from_linear_component(value)
            x2 = colormodels.display_from_linear_component(value)
            error1 = math.fabs(x2 - x2)
            msg1 = 'y=%.8f    x1=%.8f  x2=%.8f    error=%.8f' % (value, x1, x2, error1)
            if verbose:
                print (msg1)
            self.assertLessEqual(error1, tolerance)
            # Direction 2.
            y1 = color_converter.linear_from_display_component(value)
            y2 = colormodels.linear_from_display_component(value)
            error2 = math.fabs(y2 - y2)
            msg2 = 'x=%.8f    y1=%.8f  y2=%.8f    error=%.8f' % (value, y1, y2, error2)
            if verbose:
                print (msg2)
            self.assertLessEqual(error2, tolerance)


if __name__ == '__main__':
    unittest.main()
