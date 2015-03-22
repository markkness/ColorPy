'''
test_purecolors.py - Test module for purecolors.py.

This file is part of ColorPy.
'''
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import math
import numpy
import unittest

import ciexyz
import colormodels
import purecolors


class TestPureColors(unittest.TestCase):
    ''' Test cases for pure colors. '''

    def check_color_match(self, xyz1, xyz2, tolerance, verbose):
        ''' Check that the colors match. '''
        msg = 'xyz1: %s    xyz2: %s' % (str(xyz1), str(xyz2))
        if verbose:
            print (msg)
        ok = numpy.allclose(xyz1, xyz2, atol=tolerance)
        self.assertTrue(ok)

    def check_colors_brightness(self, xyzs, brightness, tolerance, verbose):
        ''' Check that the colors have the expected brightness. '''
        # Brightness is defined here as max(rgb).
        for xyz in xyzs:
            rgb = colormodels.rgb_from_xyz (xyz)
            bright = max(rgb)
            msg = 'Color: %s    Brightness: %.12f' % (str(xyz), bright)
            if verbose:
                print (msg)
            self.assertAlmostEqual(bright, brightness, delta=tolerance)

    def check_colors_not_white(self, xyzs, distance, verbose):
        ''' Check that the colors are (in xy space) at least the distance from white. '''
        # In practice distance should always be about 0.23 or more.
        white_rgb = colormodels.rgb_color (1.0, 1.0, 1.0)
        white_xyz = colormodels.xyz_from_rgb (white_rgb)
        white_xyz = colormodels.xyz_normalize (white_xyz)
        for xyz in xyzs:
            xyz = colormodels.xyz_normalize (xyz)
            dxy = numpy.hypot(xyz[0] - white_xyz[0], xyz[1] - white_xyz[1])
            msg = 'Color: %s    xy distance from white: %g' % (str(xyz), dxy)
            if verbose:
                print (msg)
            self.assertGreaterEqual(dxy, distance,
                'Color is not far enough from white.')

    def test_pure_colors(self, verbose=False):
        ''' Test get_pure_colors. '''
        brightness = 1.0
        wls     = numpy.linspace (360.0, 830.0, 100)
        purples = numpy.linspace (0.0, 1.0, 100)
        colors  = purecolors.get_pure_colors (wls, purples, brightness)
        # Colors should have expected brightness.
        tolerance = 1.0e-10
        self.check_colors_brightness(colors, brightness, tolerance, verbose)
        # Colors should not be white.
        distance = 0.2
        self.check_colors_not_white(colors, distance, verbose)

    def test_num_pure_colors(self, verbose=False):
        ''' Test get_num_pure_colors. '''
        # Use a different brightness than 1.0 for more testing.
        brightness = 0.5
        colors = purecolors.get_num_pure_colors (100, 100, brightness)
        # Colors should have expected brightness.
        tolerance = 1.0e-10
        self.check_colors_brightness(colors, brightness, tolerance, verbose)
        # Colors should not be white.
        distance = 0.2
        self.check_colors_not_white(colors, distance, verbose)

    def test_normalized_spectral_line_colors(self, verbose=False):
        ''' Test of deprecated routine. '''
        colors = purecolors.get_normalized_spectral_line_colors ()
        # Colors should not be white.
        distance = 0.2
        self.check_colors_not_white(colors, distance, verbose)

    def test_pure_scaling(self, verbose=False):
        ''' Test order of pure color scaling vs. purple interpolation. '''
        # This test confirms that scaling to max(rgb)=1 must happen both
        # for the original violet/red and after the purple interpolation.

        def scale_pure_color(xyz, bright):
            ''' Scale the color to max(rgb) = bright. '''
            rgb = colormodels.brightest_rgb_from_xyz (xyz, bright)
            xyz = colormodels.xyz_from_rgb (rgb)
            return xyz

        # Get pure violet and red color.
        violet_xyz = ciexyz.xyz_from_wavelength (purecolors.PURE_VIOLET_NM)
        red_xyz    = ciexyz.xyz_from_wavelength (purecolors.PURE_RED_NM)
        bright = 1.0
        # Scale violet and red and then interpolate, then scale purple.
        violet_scaled   = scale_pure_color (violet_xyz, bright)
        red_scaled      = scale_pure_color (red_xyz, bright)
        purple_interp_1 = 0.3 * violet_scaled + 0.7 * red_scaled
        purple_scaled_1 = scale_pure_color (purple_interp_1, bright)
        # Interpolate first, then scale purple.
        purple_interp_2 = 0.3 * violet_xyz + 0.7 * red_xyz
        purple_scaled_2 = scale_pure_color (purple_interp_2, bright)
        # The two purples do NOT match.
        # This confirms that two scaling steps are indeed required.
        tolerance = 0.4
        match = numpy.allclose(purple_scaled_1, purple_scaled_2, atol=tolerance)
        self.assertFalse(match)

    def test_purple_chromaticity(self, verbose=False):
        ''' Test that purple(0.1) is close to red not violet,
        and that purple(0.9) is close to violet and not red. '''

        def dist(color1, color2):
            ''' Cartesian distance between xyz colors. '''
            d0 = color1[0] - color2[0]
            d1 = color1[1] - color2[1]
            d2 = color1[2] - color2[2]
            d = math.sqrt(d0*d0 + d1*d1 + d2*d2)
            return d

        violet, red  = purecolors.PURE_VIOLET_NM, purecolors.PURE_RED_NM
        wl_array     = numpy.array([violet, red])
        purple_array = numpy.array([0.1, 0.9])
        colors = purecolors.get_pure_colors (wl_array, purple_array, 0.8)
        pure_violet   = colors[0]
        pure_red      = colors[1]
        pure_purple_1 = colors[2]
        pure_purple_9 = colors[3]
        # Purple(0.9) should be closer to violet than Purple(0.1).
        dv1 = dist(pure_violet, pure_purple_1)
        dv9 = dist(pure_violet, pure_purple_9)
        self.assertLess(dv9, dv1)
        # Purple(0.1) should be closer to red than Purple(0.9).
        dr1 = dist(pure_red, pure_purple_1)
        dr9 = dist(pure_red, pure_purple_9)
        self.assertLess(dr1, dr9)

    def test_perceptually_equal(self, verbose=False):
        ''' Test the perceptually equal colors. '''
        brightness = 1.0
        colors = purecolors.get_perceptually_equal_spaced_colors (
            brightness, 100, verbose)
        # Colors should have expected brightness.
        tolerance = 1.0e-10
        self.check_colors_brightness(colors, brightness, tolerance, verbose)
        # Colors should not be white.
        distance = 0.2
        self.check_colors_not_white(colors, distance, verbose)
        # TODO: Test that distance between pairs of successive colors, should be
        # the average distance, and the same for each pair.


if __name__ == '__main__':
    unittest.main()
