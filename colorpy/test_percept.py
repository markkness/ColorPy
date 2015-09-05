'''
test_percept.py - Test routines for percept.py.

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

import colormodels

# Functions to calculate the cutoff point between various algorithms.
# These do not really belong here...

# Luminance function [of Y value of an XYZ color] used in Luv and Lab.
# See [Kasson p.399] for details.
# The linear range coefficient L_LUM_C has more digits than in the paper,
# this makes the function more continuous over the boundary.

def calc_L_LUM_C ():
    '''L_LUM_C should be ideally chosen so that the two models in L_luminance() agree exactly at the cutoff point.
    This is where the extra digits in L_LUM_C, over Kasson, come from.'''
    wanted = (colormodels.L_LUM_A * math.pow (colormodels.L_LUM_CUTOFF, 1.0/3.0) - colormodels.L_LUM_B) / colormodels.L_LUM_CUTOFF
    print ('optimal L_LUM_C = %.16e' % (wanted))

# Utility function for Lab.
# See [Kasson p.399] for details.
# The linear range coefficient has more digits than in the paper,
# this makes the function more continuous over the boundary.

def calc_LAB_F_A ():
    '''LAB_F_A should be ideally chosen so that the two models in Lab_f() agree exactly at the cutoff point.
    This is where the extra digits in LAB_F_A, over Kasson, come from.'''
    wanted = (math.pow (colormodels.L_LUM_CUTOFF, 1.0/3.0) - colormodels.LAB_F_B) / colormodels.L_LUM_CUTOFF
    print ('optimal LAB_F_A = %.16e' % (wanted))


class TestPerceptualUniformSpaces(unittest.TestCase):
    ''' Test cases for (almost) perceptually color spaces Lab and Luv. '''

    # Not sure about these.
##    # Conversions between standard device independent color space (CIE XYZ)
##    # and the almost perceptually uniform space Luv.
##
##    def check_xyz_luv(self, xyz0, verbose):
##        ''' Check that luv_from_xyz() and xyz_from_luv() are inverses. '''
##        tolerance = 1.0e-10
##        luv0 = colormodels.luv_from_xyz (xyz0)
##        xyz1 = colormodels.xyz_from_luv (luv0)
##        luv1 = colormodels.luv_from_xyz (xyz1)
##        # Check errors.
##        dluv = luv1 - luv0
##        error_luv = math.sqrt (numpy.dot (dluv, dluv))
##        dxyz = xyz1 - xyz0
##        error_xyz = math.sqrt (numpy.dot (dxyz, dxyz))
##        self.assertLessEqual(error_luv, tolerance)
##        self.assertLessEqual(error_xyz, tolerance)
##        msg = 'xyz0: %s    luv0: %s    xyz1: %s    luv1: %s' % (
##            str(xyz0), str(luv0), str(xyz1), str(luv1))
##        if verbose:
##            print (msg)
##
##    def test_xyz_luv_black(self, verbose=False):
##        ''' Test Luv conversions on black. '''
##        xyz0 = colormodels.xyz_color (0.0, 0.0, 0.0)
##        self.check_xyz_luv(xyz0, verbose)
##
##    def test_xyz_luv(self, verbose=False):
##        ''' Test that luv_from_xyz() and xyz_from_luv() are inverses. '''
##        for i in range (20):
##            x0 = 10.0 * random.random()
##            y0 = 10.0 * random.random()
##            z0 = 10.0 * random.random()
##            xyz0 = colormodels.xyz_color (x0, y0, z0)
##            self.check_xyz_luv(xyz0, verbose)
##
##    # Conversions between standard device independent color space (CIE XYZ)
##    # and the almost perceptually uniform space Lab.
##
##    def check_xyz_lab(self, xyz0, verbose):
##        ''' Check that lab_from_xyz() and xyz_from_lab() are inverses. '''
##        tolerance = 1.0e-10
##        lab0 = colormodels.lab_from_xyz (xyz0)
##        xyz1 = colormodels.xyz_from_lab (lab0)
##        lab1 = colormodels.lab_from_xyz (xyz1)
##        # Check errors.
##        dlab = lab1 - lab0
##        error_lab = math.sqrt (numpy.dot (dlab, dlab))
##        dxyz = xyz1 - xyz0
##        error_xyz = math.sqrt (numpy.dot (dxyz, dxyz))
##        self.assertLessEqual(error_lab, tolerance)
##        self.assertLessEqual(error_xyz, tolerance)
##        msg = 'xyz0: %s    lab0: %s    xyz1: %s    lab1: %s' % (
##            str(xyz0), str(lab0), str(xyz1), str(lab1))
##        if verbose:
##            print (msg)
##
##    def test_xyz_lab_black(self, verbose=False):
##        ''' Test Lab conversions on black. '''
##        xyz0 = colormodels.xyz_color (0.0, 0.0, 0.0)
##        self.check_xyz_lab(xyz0, verbose)
##
##    def test_xyz_lab(self, verbose=False):
##        '''Test that lab_from_xyz() and xyz_from_lab() are inverses.'''
##        for i in range (20):
##            x0 = 10.0 * random.random()
##            y0 = 10.0 * random.random()
##            z0 = 10.0 * random.random()
##            xyz0 = colormodels.xyz_color (x0, y0, z0)
##            self.check_xyz_lab(xyz0, verbose)

    # Luminance function [of Y value of an XYZ color] used in Luv and Lab.

    def check_L_luminance_inverse_1(self, y0, verbose):
        ''' Check that L_luminance_inverse() is the inverse of L_luminance() for the given y0. '''
        L0 = colormodels.L_luminance (y0)
        y1 = colormodels.L_luminance_inverse (L0)
        # Check error.
        error = math.fabs (y1 - y0)
        tolerance = 1.0e-13
        self.assertLessEqual(error, tolerance)
        msg = 'y0: %g    L(y0): %g    y(L(y0)): %g    Error: %g' % (
            y0, L0, y1, error)
        if verbose:
            print (msg)

    def check_L_luminance_inverse_2(self, L0, verbose):
        ''' Check that L_luminance() is the inverse of L_luminance_inverse() for the given L0. '''
        y0 = colormodels.L_luminance_inverse (L0)
        L1 = colormodels.L_luminance (y0)
        # Check error.
        error = math.fabs (L1 - L0)
        tolerance = 1.0e-10
        self.assertLessEqual(error, tolerance)
        msg = 'L0: %g    y(L0): %g    L(y(L0)): %g    Error: %g' % (
            L0, y0, L1, error)
        if verbose:
            print (msg)

    def test_L_luminance_inverse_1(self, verbose=False):
        ''' Test that L_luminance_inverse(L_luminance(y)) = y. '''
        # Test with specific values on both sides of cutoff value.
        vals = [0.1, 0.5, 0.9, 1.1, 2.0, 10.0]
        for val in vals:
            y0 = val * colormodels.L_LUM_CUTOFF
            self.check_L_luminance_inverse_1(y0, verbose)
        # Test with random fairly small y values.
        for i in range (20):
            y0 = 0.1 * random.random()
            self.check_L_luminance_inverse_1(y0, verbose)
        # Test with random fairly large y values.
        for i in range (20):
            y0 = 10.0 * random.random()
            self.check_L_luminance_inverse_1(y0, verbose)

    def test_L_luminance_inverse_2(self, verbose=False):
        ''' Test that L_luminance(L_luminance_inverse(L)) = L. '''
        # Test with specific values on both sides of cutoff value.
        vals = [0.1, 0.5, 0.9, 1.1, 2.0, 10.0]
        for val in vals:
            L0 = val * colormodels.L_LUM_C * colormodels.L_LUM_CUTOFF
            self.check_L_luminance_inverse_2(L0, verbose)
        # Test with random fairly small L values.
        for i in range (20):
            L0 = 25.0 * random.random()
            self.check_L_luminance_inverse_2(L0, verbose)
        # Test with random fairly large L values.
        for i in range (20):
            L0 = 1000.0 * random.random()
            self.check_L_luminance_inverse_2(L0, verbose)

    # Utility function for Lab.

    def check_Lab_f_inverse_1(self, t0, verbose):
        ''' Check that Lab_f_inverse() is the inverse of Lab_f() for the given t0. '''
        f0 = colormodels.Lab_f (t0)
        t1 = colormodels.Lab_f_inverse (f0)
        # Check error.
        error = math.fabs (t1 - t0)
        tolerance = 1.0e-13
        self.assertLessEqual(error, tolerance)
        msg = 't0: %g    f(t0): %g    t(f(t0)): %g    Error: %g' % (
            t0, f0, t1, error)
        if verbose:
            print (msg)

    def check_Lab_f_inverse_2(self, f0, verbose):
        ''' Check that Lab_f() is the inverse of Lab_f_inverse() for the given f0. '''
        t0 = colormodels.Lab_f_inverse (f0)
        f1 = colormodels.Lab_f (t0)
        # Check error.
        error = math.fabs (f1 - f0)
        tolerance = 1.0e-10
        self.assertLessEqual(error, tolerance)
        msg = 'f0: %g    t(f0): %g    f(t(f0)): %g    Error: %g' % (
            f0, t0, f1, error)
        if verbose:
            print (msg)

    def test_Lab_f_inverse_1(self, verbose=False):
        ''' Test that Lab_f_inverse(Lab_f(t)) = t. '''
        # Test with specific values on both sides of cutoff value.
        vals = [0.1, 0.5, 0.9, 1.1, 2.0, 10.0]
        for val in vals:
            y0 = val * colormodels.L_LUM_CUTOFF
            self.check_Lab_f_inverse_1(y0, verbose)
        # Test with fairly small random values.
        for i in range (20):
            y0 = 0.02 * random.random()
            self.check_Lab_f_inverse_1(y0, verbose)
        # Test with fairly large random values.
        for i in range (20):
            y0 = 10.0 * random.random()
            self.check_Lab_f_inverse_1(y0, verbose)

    def test_Lab_f_inverse_2(self, verbose=False):
        ''' Test that Lab_f(Lab_f_inverse(L)) = L. '''
        # Test with specific values on both sides of cutoff value.
        vals = [0.1, 0.5, 0.9, 1.1, 2.0, 10.0]
        for val in vals:
            L0 = val * (colormodels.LAB_F_A * colormodels.L_LUM_CUTOFF + colormodels.LAB_F_B)
            self.check_Lab_f_inverse_2(L0, verbose)
        # Test with fairly small random values.
        for i in range (20):
            L0 = 0.25 * random.random()
            self.check_Lab_f_inverse_2(L0, verbose)
        # Test with fairly large random values.
        for i in range (20):
            L0 = 1000.0 * random.random()
            self.check_Lab_f_inverse_2(L0, verbose)

    # Utility function for Luv.

    def check_uv_primes_inverse_1(self, xyz0, verbose):
        ''' Check that uv_primes() and uv_primes_inverse() are inverses. '''
        up0, vp0 = colormodels.uv_primes (xyz0)
        xyz1 = colormodels.uv_primes_inverse (up0, vp0, xyz0[1])
        # Check error.
        dxyz = (xyz1 - xyz0)
        error = math.sqrt (numpy.dot (dxyz, dxyz))
        tolerance = 1.0e-13
        self.assertLessEqual(error, tolerance)
        msg = 'xyz0: %s    up: %g    vp: %g    xyz(up,vp): %s    Error: %g' % (
            str (xyz0), up0, vp0, str(xyz1), error)
        if verbose:
            print (msg)

    def check_uv_primes_inverse_2(self, up0, vp0, y0, verbose):
        ''' Check that uv_primes() and uv_primes_inverse() are inverses. '''
        xyz0 = colormodels.uv_primes_inverse (up0, vp0, y0)
        up1, vp1 = colormodels.uv_primes (xyz0)
        # Check error.
        error_up = up1 - up0
        error_vp = vp1 - vp0
        error = numpy.hypot (error_up, error_vp)
        tolerance = 1.0e-13
        self.assertLessEqual(error, tolerance)
        msg = 'up0, vp0, y0: %g, %g, %g    xyz(up0,vp0,y0): %s    (up,vp)(xyz): %g, %g    Error: %g' % (
            up0, vp0, y0, str (xyz0), up1, vp1, error)
        if verbose:
            print (msg)

    def test_uv_primes_inverse_1(self, verbose=False):
        ''' Test that uv_primes() and uv_primes_inverse() are inverses. '''
        # Test some random values.
        for i in range (20):
            x0 = 10.0 * random.random()
            y0 = 10.0 * random.random()
            z0 = 10.0 * random.random()
            xyz0 = colormodels.xyz_color (x0, y0, z0)
            self.check_uv_primes_inverse_1(xyz0, verbose)
        # Test black explicitly.
        xyz0 = colormodels.xyz_color (0.0, 0.0, 0.0)
        self.check_uv_primes_inverse_1(xyz0, verbose)

    def test_uv_primes_inverse_2(self, verbose=False):
        ''' Test that uv_primes() and uv_primes_inverse() are inverses. '''
        # Test some random values.
        for i in range (20):
            up0 = 4.0 * (2.0 * random.random() - 1.0)
            vp0 = 9.0 * (2.0 * random.random() - 1.0)
            y0  = 10.0 * random.random()
            self.check_uv_primes_inverse_2(up0, vp0, y0, verbose)
        # Test black explicitly.
        self.check_uv_primes_inverse_2(0.0, 0.0, 0.0, verbose)


if __name__ == '__main__':
    unittest.main()
