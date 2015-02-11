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
import math, random, numpy

import colormodels
import blackbody

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

# Tests

def test_Wyszecki_p29 ():
    '''Calculations re Wyszecki p29 table.'''
    T = 1336.0     # 'Gold' point
    xyz = blackbody.blackbody_color (T)
    print 'blackbody color at gold point', str (xyz)
    # this source is supposed to be 0.11 cd/cm^2 = 1100 cd/m^2
    # whereas monitors are c. 80 cd/m^2 to 300 cd/m^2

def test_stefan_boltzman (verbose=1):
    '''Test that the total intensity over many wavelengths matches the Stefan-Boltman formula.
    NOTE - This currently does not match.  I am not sure what the situation is.'''
    T = 100.0
    sb_test0 = blackbody_total_intensity_stefan_boltzman (T)
    print 'sb_test0', sb_test0
    sb_test1 = blackbody_total_intensity (T, 0, 1000)
    print 'sb_test1', sb_test1
    sb_test2 = blackbody_total_intensity (T, 0, 10000)
    print 'sb_test2', sb_test2
    sb_test3 = blackbody_total_intensity (T, 0, 100000)
    print 'sb_test3', sb_test3
    # following start to get slow...
    #sb_test4 = blackbody_total_intensity (T, 0, 1000000)
    #print 'sb_test4', sb_test4
    #sb_test5 = blackbody_total_intensity (T, 0, 10000000)
    #print 'sb_test5', sb_test5

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
        #if verbose >= 1:
        if True:
            print 'T', T
            print 'total_sb', total_sb
            print 'total1', total1
            print 'total2', total2
            print 'total3', total3
            print 'total4', total4
            print 'ratio', ratio

def test_blackbody (verbose=0):
    '''Test the blackbody functions.'''
    num_passed = 0
    num_failed = 0

    # a few calls with specific arguments
    test_zero1 = blackbody_total_intensity (100.0, 0, 100)
    test_zero2 = blackbody_total_intensity (0.0, 0, 100)
    test_zero3 = blackbody_total_intensity (100000.0, 0, 100)
    test_zero4 = blackbody_total_intensity (0.0, 0, 100000)
    test_zero5 = blackbody_total_intensity (100000.0, 0, 100000)
    num_passed += 5

    # determine the color for several temperatures - 10000.0 is a particularly good range
    temp_ranges = [100.0, 1000.0, 10000.0, 100000.0, 1000000.0 ]
    for T0 in temp_ranges:
        for i in range (0, 20):
            T_K = T0 * random.random()
            xyz = blackbody.blackbody_color (T_K)
            if verbose >= 1:
                print 'T = %g K, xyz = %s' % (T_K, str (xyz))
            num_passed += 1   # didn't exception

    msg = 'test_blackbody() : %d tests passed, %d tests failed' % (
        num_passed, num_failed)
    print msg

# Table of xy chromaticities for blackbodies
# From (I think): Judd and Wyszecki, Color in Business, Science and Industry, 1975, p. 164

book_chrom_table = numpy.array ([
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

def test_book (verbose=1):
    '''Test that the computed chromaticities match an existing table, from Judd and Wyszecki.'''
    num_passed = 0
    num_failed = 0

    (num_rows, num_cols) = book_chrom_table.shape
    for i in range (0, num_rows):
        T = book_chrom_table [i][0]
        book_x = book_chrom_table [i][1]
        book_y = book_chrom_table [i][2]
        # calculate color for T
        xyz = blackbody.blackbody_color (T)
        colormodels.xyz_normalize (xyz)
        dx = xyz [0] - book_x
        dy = xyz [1] - book_y
        # did we match the tablulated result?
        tolerance = 2.0e-4
        passed = (math.fabs (dx) <= tolerance) and (math.fabs (dy) <= tolerance)
        if passed:
            status = 'pass'
        else:
            status = 'FAILED'
        msg = 'test_book() : T = %g : calculated x,y = %g,%g : book values x,y = %g,%g : errors = %g,%g' % (
            T, xyz [0], xyz [1], book_x, book_y, dx, dy)
        if verbose >= 1:
            print msg
        if not passed:
            pass
            raise ValueError, msg
        if passed:
            num_passed += 1
        else:
            num_failed += 1

    msg = 'test_book() : %d tests passed, %d tests failed' % (
        num_passed, num_failed)
    print msg

# Tests

def test (verbose=0):
    '''Test the blackbody module.'''
    test_blackbody (verbose=verbose)
    test_book (verbose=verbose)
    #test_stefan_boltzman (verbose=verbose)

