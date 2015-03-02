'''
test_pure_colors.py - Test module for pure_colors.py.

This file is part of ColorPy.
'''
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import numpy
import unittest

import ciexyz
import colormodels
import pure_colors

# FIXME: Rename these files to 'purecolors.py' or 'pure.py'?

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
        colors  = pure_colors.get_pure_colors (brightness, wls, purples)
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
        colors = pure_colors.get_num_pure_colors (brightness, 100, 100)
        # Colors should have expected brightness.
        tolerance = 1.0e-10
        self.check_colors_brightness(colors, brightness, tolerance, verbose)
        # Colors should not be white.
        distance = 0.2
        self.check_colors_not_white(colors, distance, verbose)

    def test_normalized_spectral_line_colors(self, verbose=False):
        ''' Test of deprecated routine. '''
        colors = pure_colors.get_normalized_spectral_line_colors ()
        # Colors should not be white.
        distance = 0.2
        self.check_colors_not_white(colors, distance, verbose)

    def test_purple_chromaticity(self, verbose=True):
        ''' Test that purple(0.1) is close to red not violet,
        and that purple(0.9) is close to violet and not red. '''
        # TODO.
        # FIXME: Make sure of/define the direction.
        pass

    def test_purple_interpolate(self, verbose=False):
        ''' Test that purple chromaticities are linearly interpolated. '''
        wls     = numpy.array([ciexyz.start_wl_nm, ciexyz.end_wl_nm])
        purples = numpy.array([0.2, 0.5, 0.8])
        colors  = pure_colors.get_pure_colors (1.0, wls, purples)
        # Color 0 is violet, color 1 is red, colors 2,3,4 are purples.
        purp_20 = colors[2]
        purp_50 = colors[3]
        purp_80 = colors[4]
        # Scale them all consistently.
        purp_20 = colormodels.xyz_normalize (purp_20)
        purp_50 = colormodels.xyz_normalize (purp_50)
        purp_80 = colormodels.xyz_normalize (purp_80)
        # Purple-50 should be average of 20 and 80.
        expect_50 = 0.5 * (purp_20 + purp_80)
        tolerance = 1.0e-10
        self.check_color_match(purp_50, expect_50, tolerance, verbose)

    def test_perceptually_equal(self, verbose=False):
        ''' Test the perceptually equal colors. '''
        # Mostly a coverage test for now.
        brightness = 1.0
        colors = pure_colors.get_perceptually_equal_spaced_colors (
            brightness, 100)
        # Colors should have expected brightness.
        tolerance = 1.0e-10
        # FIXME: They are changed a little bit, probably by interpolation.
        # Thus a large tolerance is required.
        tolerance = 0.01
        self.check_colors_brightness(colors, brightness, tolerance, verbose)
        # Colors should not be white.
        distance = 0.2
        self.check_colors_not_white(colors, distance, verbose)
        # TODO: Test that distance between pairs of successive colors, should be
        # the average distance, and the same for each pair.


if __name__ == '__main__':
    unittest.main()
