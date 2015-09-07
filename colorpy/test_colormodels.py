'''
test_colormodels.py - Test routines for colormodels.py.

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
import colortypes
import purecolors


class TestColormodels(unittest.TestCase):
    ''' Test cases for colormodel conversions. '''

    def test_xyz_normalization(self, verbose=True):
        ''' Test of xyz color constructors. '''
        # Test sum normalization.
        xyz1 = colortypes.xyz_color(0.1, 0.2, 0.3)
        colormodels.xyz_normalize(xyz1)
        sum_xyz = xyz1[0] + xyz1[1] + xyz1[2]
        self.assertAlmostEqual(sum_xyz, 1.0)
        # Test Y normalization.
        xyz2 = colortypes.xyz_color_from_xyY(0.33, 0.55, 0.8)
        colormodels.xyz_normalize_Y1(xyz2)
        self.assertAlmostEqual(xyz2[1], 1.0)

    def test_rgb_xyz_matrices_inverses(self, verbose=False):
        ''' Test that the rgb<--->xyz conversion matrices are inverses of each other. '''
        test_eye0 = numpy.dot (
            colormodels.color_converter.rgb_from_xyz_matrix,
            colormodels.color_converter.xyz_from_rgb_matrix)
        test_eye1 = numpy.dot (
            colormodels.color_converter.xyz_from_rgb_matrix,
            colormodels.color_converter.rgb_from_xyz_matrix)
        msg0 = 'RGB_from_XYZ * XYZ_from_RGB =\n%s' % (str(test_eye0))
        msg1 = 'XYZ_from_RGB * RGB_from_XYZ =\n%s' % (str(test_eye1))
        if verbose:
            print (msg0)
            print (msg1)
        atol = 1.0e-8
        ok0 = numpy.allclose (test_eye0, numpy.eye (3), atol=atol)
        ok1 = numpy.allclose (test_eye1, numpy.eye (3), atol=atol)
        self.assertTrue(ok0)
        self.assertTrue(ok1)

    def check_xyz_rgb(self, xyz0, verbose):
        ''' Check that the xyz color, converted to rgb then back, remains the same. '''
        rgb0 = colormodels.rgb_from_xyz (xyz0)
        xyz1 = colormodels.xyz_from_rgb (rgb0)
        rgb1 = colormodels.rgb_from_xyz (xyz1)
        # Check errors.
        err_rgb = rgb1 - rgb0
        error_rgb = math.sqrt (numpy.dot (err_rgb, err_rgb))
        err_xyz = xyz1 - xyz0
        error_xyz = math.sqrt (numpy.dot (err_xyz, err_xyz))
        tolerance = 1.0e-10
        self.assertLess(error_xyz, tolerance)
        self.assertLess(error_rgb, tolerance)
        msg = 'xyz: %s    rgb: %s    xyz2: %s    rgb2: %s' % (
            str(xyz0), str(rgb0), str(xyz1), str(rgb1))
        if verbose:
            print (msg)

    def test_xyz_rgb(self, verbose=False):
        ''' Test some color values via check_xyz_rgb(). '''
        for i in range (20):
            x0 = 10.0 * random.random()
            y0 = 10.0 * random.random()
            z0 = 10.0 * random.random()
            xyz0 = colortypes.xyz_color (x0, y0, z0)
            self.check_xyz_rgb (xyz0, verbose)

    def check_xyz_irgb(self, xyz0, verbose):
        ''' Check the direct conversions from xyz to irgb. '''
        irgb0 = colormodels.irgb_from_rgb (
            colormodels.rgb_from_xyz (xyz0))
        irgb1 = colormodels.irgb_from_xyz (xyz0)
        self.assertEqual(irgb0[0], irgb1[0])
        self.assertEqual(irgb0[1], irgb1[1])
        self.assertEqual(irgb0[2], irgb1[2])
        # The string should also match.
        irgbs0 = colormodels.irgb_string_from_rgb (
            colormodels.rgb_from_xyz (xyz0))
        irgbs1 = colormodels.irgb_string_from_xyz (xyz0)
        msg = 'irgb0: %s    text0: %s        irgb1: %s    text1: %s' % (
            str(irgb0), irgbs0, str(irgb1), irgbs1)
        if verbose:
            print (msg)
        self.assertEqual(irgbs0, irgbs1)

    def test_xyz_irgb(self, verbose=False):
        ''' Test the direct conversions from xyz to irgb. '''
        for i in range (20):
            x0 = 10.0 * random.random()
            y0 = 10.0 * random.random()
            z0 = 10.0 * random.random()
            xyz0 = colortypes.xyz_color (x0,y0,z0)
            self.check_xyz_irgb(xyz0, verbose)

    def check_rgb_irgb(self, irgb0, verbose):
        ''' Check that conversions between rgb and irgb are invertible. '''
        rgb0  = colormodels.rgb_from_irgb (irgb0)
        irgb1 = colormodels.irgb_from_rgb (rgb0)
        rgb1  = colormodels.rgb_from_irgb (irgb1)
        # Integer conversion should match exactly.
        self.assertEqual(irgb0[0], irgb1[0])
        self.assertEqual(irgb0[1], irgb1[1])
        self.assertEqual(irgb0[2], irgb1[2])
        msg = 'irgb0: %s    irgb1: %s' % (str(irgb0), str(irgb1))
        if verbose:
            print (msg)
        # Float conversion should match closely.
        # (It actually seems to match exactly for me.)
        tolerance = 1.0e-14
        err_rgb = rgb1 - rgb0
        err_r = math.fabs (err_rgb [0])
        err_g = math.fabs (err_rgb [1])
        err_b = math.fabs (err_rgb [2])
        self.assertLessEqual(err_r, tolerance)
        self.assertLessEqual(err_g, tolerance)
        self.assertLessEqual(err_b, tolerance)
        msg = 'rgb0: %s    rgb1: %s' % (str(rgb0), str(rgb1))
        if verbose:
            print (msg)

    def test_rgb_irgb(self, verbose=False):
        ''' Test that conversions between rgb and irgb are invertible. '''
        for i in range (20):
            ir = random.randrange (0, 256)
            ig = random.randrange (0, 256)
            ib = random.randrange (0, 256)
            irgb0 = colortypes.irgb_color (ir, ig, ib)
            self.check_rgb_irgb(irgb0, verbose)

    # Clipping.

    def test_clipping(self, verbose=False):
        ''' Test the various color clipping methods. '''
        # This is just a coverage test.
        xyz_colors = purecolors.get_normalized_spectral_line_colors ()
        num_wl = xyz_colors.shape[0]
        for i in range (num_wl):
            # Get rgb values for standard add white clipping.
            colormodels.color_converter.init_clipping (colormodels.CLIP_ADD_WHITE)
            rgb_white_color = colormodels.irgb_string_from_rgb (
                colormodels.rgb_from_xyz (xyz_colors [i]))

            # Get rgb values for clamp-to-zero clipping.
            colormodels.color_converter.init_clipping (colormodels.CLIP_CLAMP_TO_ZERO)
            rgb_clamp_color = colormodels.irgb_string_from_rgb (
                colormodels.rgb_from_xyz (xyz_colors [i]))

            msg = 'Wavelength: %s    White: %s    Clamp: %s' % (
                str(i),    # FIXME: Put in Angstroms.
                rgb_white_color,
                rgb_clamp_color)
            if verbose:
                print (msg)

    # Conversions between standard device independent color space (CIE XYZ)
    # and the almost perceptually uniform space Luv.

    def check_xyz_luv(self, xyz0, verbose):
        ''' Check that luv_from_xyz() and xyz_from_luv() are inverses. '''
        tolerance = 1.0e-10
        luv0 = colormodels.luv_from_xyz (xyz0)
        xyz1 = colormodels.xyz_from_luv (luv0)
        luv1 = colormodels.luv_from_xyz (xyz1)
        # Check errors.
        dluv = luv1 - luv0
        error_luv = math.sqrt (numpy.dot (dluv, dluv))
        dxyz = xyz1 - xyz0
        error_xyz = math.sqrt (numpy.dot (dxyz, dxyz))
        self.assertLessEqual(error_luv, tolerance)
        self.assertLessEqual(error_xyz, tolerance)
        msg = 'xyz0: %s    luv0: %s    xyz1: %s    luv1: %s' % (
            str(xyz0), str(luv0), str(xyz1), str(luv1))
        if verbose:
            print (msg)

    def test_xyz_luv_black(self, verbose=False):
        ''' Test Luv conversions on black. '''
        xyz0 = colortypes.xyz_color (0.0, 0.0, 0.0)
        self.check_xyz_luv(xyz0, verbose)

    def test_xyz_luv(self, verbose=False):
        ''' Test that luv_from_xyz() and xyz_from_luv() are inverses. '''
        for i in range (20):
            x0 = 10.0 * random.random()
            y0 = 10.0 * random.random()
            z0 = 10.0 * random.random()
            xyz0 = colortypes.xyz_color (x0, y0, z0)
            self.check_xyz_luv(xyz0, verbose)

    # Conversions between standard device independent color space (CIE XYZ)
    # and the almost perceptually uniform space Lab.

    def check_xyz_lab(self, xyz0, verbose):
        ''' Check that lab_from_xyz() and xyz_from_lab() are inverses. '''
        tolerance = 1.0e-10
        lab0 = colormodels.lab_from_xyz (xyz0)
        xyz1 = colormodels.xyz_from_lab (lab0)
        lab1 = colormodels.lab_from_xyz (xyz1)
        # Check errors.
        dlab = lab1 - lab0
        error_lab = math.sqrt (numpy.dot (dlab, dlab))
        dxyz = xyz1 - xyz0
        error_xyz = math.sqrt (numpy.dot (dxyz, dxyz))
        self.assertLessEqual(error_lab, tolerance)
        self.assertLessEqual(error_xyz, tolerance)
        msg = 'xyz0: %s    lab0: %s    xyz1: %s    lab1: %s' % (
            str(xyz0), str(lab0), str(xyz1), str(lab1))
        if verbose:
            print (msg)

    def test_xyz_lab_black(self, verbose=False):
        ''' Test Lab conversions on black. '''
        xyz0 = colortypes.xyz_color (0.0, 0.0, 0.0)
        self.check_xyz_lab(xyz0, verbose)

    def test_xyz_lab(self, verbose=False):
        '''Test that lab_from_xyz() and xyz_from_lab() are inverses.'''
        for i in range (20):
            x0 = 10.0 * random.random()
            y0 = 10.0 * random.random()
            z0 = 10.0 * random.random()
            xyz0 = colortypes.xyz_color (x0, y0, z0)
            self.check_xyz_lab(xyz0, verbose)


if __name__ == '__main__':
    unittest.main()
