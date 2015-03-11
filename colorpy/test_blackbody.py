'''
test_blackbody.py - Test cases for blackbody.py

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
import unittest

import blackbody
import colormodels

# FIXME: The following calculation is not working currently.
# It is an attempt to get the scale of the intensity correct.
# It needs more investigation.

STEFAN_BOLTZMAN = 5.670e-8        # W/(m^2 K^4)

def blackbody_total_intensity (T_K, start_wl_nm, end_wl_nm):
    '''Get the sum of the specific intensity, at 1 nm increments, from start_wl_nm to end_wl_nm.'''
    total = 0.0
    for wl_nm in range (start_wl_nm, end_wl_nm+1):
        specific = blackbody.blackbody_specific_intensity (wl_nm, T_K)
        total += specific
    return total

def blackbody_total_intensity_stefan_boltzman (T_K):
    '''Get the sum of the intensities over all wavelengths, assuming the Stefan-Boltzman law.'''
    total = STEFAN_BOLTZMAN * math.pow (T_K, 4)
    # TODO - What (if any) scaling is required of this result to correspond to blackbody_specific_intensity()?
    # I am not sure, and there is a mismatch.
    # not entirely sure about the following scaling...  See Shu.
    scaling = blackbody.SPEED_OF_LIGHT     # almost
    total *= scaling
    return total

def test_stefan_boltzman():
    '''Test that the total intensity over many wavelengths matches the Stefan-Boltman formula.
    NOTE - This currently does not match.  I am not sure what the situation is.'''
    T = 100.0
    sb_test0 = blackbody_total_intensity_stefan_boltzman (T)
    print ('sb_test0', sb_test0)
    sb_test1 = blackbody_total_intensity (T, 0, 1000)
    print ('sb_test1', sb_test1)
    sb_test2 = blackbody_total_intensity (T, 0, 10000)
    print ('sb_test2', sb_test2)
    sb_test3 = blackbody_total_intensity (T, 0, 100000)
    print ('sb_test3', sb_test3)
    # following start to get slow...
    #sb_test4 = blackbody_total_intensity (T, 0, 1000000)
    #print ('sb_test4', sb_test4)
    #sb_test5 = blackbody_total_intensity (T, 0, 10000000)
    #print ('sb_test5', sb_test5)

    # compare the computed result with the stefan-boltzman formula
    # TODO - these do not match, although the T^4 behavior is observed...
    T_list = [100.0, 1000.0, 4000.0, 6500.0, 10000.0, 15000.0]
    for T in T_list:
        total_sb = blackbody_total_intensity_stefan_boltzman (T)
        # larger wavelength intervals capture more of the total power
        total1 = blackbody_total_intensity (T, 360, 830)
        total2 = blackbody_total_intensity (T, 1, 1000)
        total3 = blackbody_total_intensity (T, 1, 10000)
        total4 = blackbody_total_intensity (T, 1, 100000)
        ratio = total4 / total_sb
        print ('T', T)
        print ('total_sb', total_sb)
        print ('total1', total1)
        print ('total2', total2)
        print ('total3', total3)
        print ('total4', total4)
        print ('ratio', ratio)


# Table of xy chromaticities for blackbodies. From (I think):
#     Judd and Wyszecki, Color in Business, Science and Industry, 1975, p. 164.

Judd_Wyszeki_blackbody_chromaticity_table = numpy.array ([
    [ 1000.0, 0.6528, 0.3444],
    [ 1400.0, 0.5985, 0.3858],
    [ 1600.0, 0.5732, 0.3993],
    [ 1800.0, 0.5493, 0.4082],
    [ 2000.0, 0.5267, 0.4133],
    [ 2200.0, 0.5056, 0.4152],
    [ 2400.0, 0.4862, 0.4147],
    [ 2600.0, 0.4682, 0.4123],
    [ 2800.0, 0.4519, 0.4086],
    [ 3000.0, 0.4369, 0.4041],
    [ 3200.0, 0.4234, 0.3990],
    [ 3400.0, 0.4110, 0.3935],
    [ 3600.0, 0.3999, 0.3879],
    [ 3800.0, 0.3897, 0.3823],
    [ 4200.0, 0.3720, 0.3714],
    [ 4500.0, 0.3608, 0.3636],
    [ 4800.0, 0.3510, 0.3562],
    [ 5200.0, 0.3397, 0.3472],
    [ 5800.0, 0.3260, 0.3354],
    [ 6500.0, 0.3135, 0.3237],
    [ 7500.0, 0.3004, 0.3103],
    [ 8500.0, 0.2908, 0.3000],
    [10000.0, 0.2807, 0.2884],
    [30000.0, 0.2501, 0.2489]])


class TestBlackbody(unittest.TestCase):
    ''' Test cases for blackbody spectrum. '''

    def test_coverage_color(self, verbose=False):
        ''' Coverage test of blackbody color. '''
        # Calculate the color for a variety of temperatures.
        T_list = numpy.logspace(1.0, 6.0, 21, base=10).tolist()
        for T in T_list:
            xyz = blackbody.blackbody_color (T)
            msg = 'T: %g K    xyz: %s' % (T, str(xyz))
            if verbose:
                print (msg)

    def test_coverage_total_intensity(self):
        ''' Coverage test of blackbody total intensity. '''
        # FIXME: This function is only used in a test that is not working now.
        blackbody_total_intensity (100.0, 0, 100)
        blackbody_total_intensity (0.0, 0, 100)
        blackbody_total_intensity (100000.0, 0, 100)
        blackbody_total_intensity (0.0, 0, 100000)
        blackbody_total_intensity (100000.0, 0, 100000)

    def test_gold_point(self, verbose=False):
        ''' Test the chromaticity at the 'gold point'. '''
        # From Wyszecki & Stiles, p. 28.
        T        = 1336.0     # 'Gold' point
        x_expect = 0.607
        y_expect = 0.381
        xyz = blackbody.blackbody_color (T)
        colormodels.xyz_normalize (xyz)
        x_actual = xyz[0]
        y_actual = xyz[1]
        # Check result. The tolerance is high, there is a discrepancy
        # in the last printed digit in the table in the book.
        # A tolerance of 5.0e-4 would match the precision in the book.
        tolerance = 6.0e-4
        self.assertAlmostEqual(x_actual, x_expect, delta=tolerance)
        self.assertAlmostEqual(y_actual, y_expect, delta=tolerance)
        # This source is supposed to be 0.11 cd/cm^2 = 1100 cd/m^2,
        # whereas monitors are c. 80 cd/m^2 to 300 cd/m^2.
        msg = 'Blackbody color at gold point: %s' % (str (xyz))
        if verbose:
            print (msg)

    def test_judd_wyszecki(self, verbose=False):
        ''' Test computed chromaticities vs table in Judd and Wyszecki. '''
        if verbose:
            print ('Test vs. Judd and Wyszecki:')
        table = Judd_Wyszeki_blackbody_chromaticity_table
        num_rows = table.shape[0]
        for i in range (0, num_rows):
            # Read temperature and expected chromaticity.
            T        = table [i][0]
            x_expect = table [i][1]
            y_expect = table [i][2]
            # Calculate chromaticity for the temperature.
            xyz = blackbody.blackbody_color (T)
            colormodels.xyz_normalize (xyz)
            x_actual = xyz[0]
            y_actual = xyz[1]
            # Check against the tabulated result.
            x_error = math.fabs(x_actual - x_expect)
            y_error = math.fabs(y_actual - y_expect)
            # The tolerance used is larger than desired.
            # A tolerance of 5.0e-5 would match the precision in the book.
            tolerance = 15.0e-5
            self.assertAlmostEqual(x_actual, x_expect, delta=tolerance)
            self.assertAlmostEqual(y_actual, y_expect, delta=tolerance)
            # Print results.
            msg = 'T: %8.1f K    Calculated x,y: %.5f, %.5f    Expected x,y: %.5f, %.5f    Error: %.5e, %.5e' % (
                T, x_actual, y_actual, x_expect, y_expect, x_error, y_error)
            if verbose:
                print (msg)

    def check_old_spectrum(self, old_spect, new_spect, tolerance, verbose):
        ''' Old-style and new-style spectra should return the same values. '''
        ok = numpy.allclose(old_spect[:,0], new_spect.wavelength, atol=tolerance)
        self.assertTrue(ok)
        ok = numpy.allclose(old_spect[:,1], new_spect.intensity, atol=tolerance)
        self.assertTrue(ok)

    def test_old(self, verbose=False):
        ''' Test the old-style functions. '''
        tolerance = 0.0
        T_list = [100.0, 1000.0, 3500.0, 5000.0, 9000.0, 15000.0, 1.0e6]
        for T in T_list:
            # Spectrum should match.
            spect_old = blackbody.blackbody_spectrum_old (T)
            spect_new = blackbody.get_blackbody_spectrum (T)
            self.check_old_spectrum(spect_old, spect_new, tolerance, verbose)


if __name__ == '__main__':
    if False:
        # This calculation is not working yet...
        test_stefan_boltzman()
    unittest.main()
