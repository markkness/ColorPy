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
import math, random, numpy
import colormodels
import ciexyz

def test_xyz_rgb (verbose=1):
    '''Test that xyz_to_rgb() and rgb_to_xyz() are inverses.'''

    def test_A (xyz0, tolerance=1.0e-10, verbose=1):
        rgb0 = colormodels.rgb_from_xyz (xyz0)
        xyz1 = colormodels.xyz_from_rgb (rgb0)
        rgb1 = colormodels.rgb_from_xyz (xyz1)
        # check errors
        err_rgb = rgb1 - rgb0
        error_rgb = math.sqrt (numpy.dot (err_rgb, err_rgb))
        err_xyz = xyz1 - xyz0
        error_xyz = math.sqrt (numpy.dot (err_xyz, err_xyz))
        passed = (error_rgb <= tolerance) and (error_xyz <= tolerance)
        if passed:
            status = 'pass'
        else:
            status = 'FAILED'
        msg = 'test_xyz_rgb.test_A() : xyz0 = %s, rgb(xyz0) = %s, xyz(rgb(xyz0)) = %s, rgb(xyz(rgb(xyz0))) = %s, errors = (%g, %g), %s' % (
            str (xyz0), str (rgb0), str (xyz1), str (rgb1), error_rgb, error_xyz, status)
        if verbose >= 1:
            print msg
        if not passed:
            pass
            raise ValueError, msg
        return passed

    num_passed = 0
    num_failed = 0

    for i in xrange (0, 100):
        x0 = 10.0 * random.random()
        y0 = 10.0 * random.random()
        z0 = 10.0 * random.random()
        xyz0 = colormodels.xyz_color (x0,y0,z0)
        passed = test_A (xyz0, tolerance=1.0e-10, verbose=verbose)
        if passed:
            num_passed += 1
        else:
            num_failed += 1

    # Test that the conversion matrices are inverses
    test_eye0 = numpy.dot (colormodels.rgb_from_xyz_matrix, colormodels.xyz_from_rgb_matrix)
    test_eye1 = numpy.dot (colormodels.xyz_from_rgb_matrix, colormodels.rgb_from_xyz_matrix)
    passed = numpy.allclose (test_eye0, numpy.eye (3)) and numpy.allclose (test_eye1, numpy.eye (3))
    if passed:
        num_passed += 1
    else:
        num_failed += 1

    msg = 'test_xyz_rgb() : %d tests passed, %d tests failed' % (
        num_passed, num_failed)
    print msg

def test_xyz_irgb (verbose=1):
    '''Test the direct conversions from xyz to irgb.'''
    for i in xrange (0, 100):
        x0 = 10.0 * random.random()
        y0 = 10.0 * random.random()
        z0 = 10.0 * random.random()
        xyz0 = colormodels.xyz_color (x0,y0,z0)
        irgb0 = colormodels.irgb_from_rgb (
            colormodels.rgb_from_xyz (xyz0))
        irgb1 = colormodels.irgb_from_xyz (xyz0)
        if (irgb0[0] != irgb1[0]) or (irgb0[1] != irgb1[1]) or (irgb0[2] != irgb1[2]):
            raise ValueError
        irgbs0 = colormodels.irgb_string_from_rgb (
            colormodels.rgb_from_xyz (xyz0))
        irgbs1 = colormodels.irgb_string_from_xyz (xyz0)
        if irgbs0 != irgbs1:
            raise ValueError
    print 'Passed test_xyz_irgb()'

#
# Color model conversions to (nearly) perceptually uniform spaces Luv and Lab.
#

# Luminance function [of Y value of an XYZ color] used in Luv and Lab. See [Kasson p.399] for details.
# The linear range coefficient L_LUM_C has more digits than in the paper,
# this makes the function more continuous over the boundary.

def calc_L_LUM_C ():
    '''L_LUM_C should be ideally chosen so that the two models in L_luminance() agree exactly at the cutoff point.
    This is where the extra digits in L_LUM_C, over Kasson, come from.'''
    wanted = (colormodels.L_LUM_A * math.pow (colormodels.L_LUM_CUTOFF, 1.0/3.0) - colormodels.L_LUM_B) / colormodels.L_LUM_CUTOFF
    print 'optimal L_LUM_C = %.16e' % (wanted)

def test_L_luminance (verbose=1):
    '''Test that L_luminance() and L_luminance_inverse() are really inverses.'''
    # Test A - Check that L_luminance_inverse() is the inverse of L_luminance()
    def test_A (y0, tolerance=1.0e-13, verbose=1):
        '''Check that L_luminance_inverse() is the inverse of L_luminance() for the given y0.'''
        # we should cover both ranges in the tests
        if (y0 > colormodels.L_LUM_CUTOFF):
            range_info = 'in normal range'
        else:
            range_info = 'in linear range'
        L0 = colormodels.L_luminance (y0)
        y1 = colormodels.L_luminance_inverse (L0)
        # check error
        error = math.fabs (y1 - y0)
        passed = (error <= tolerance)
        if passed:
            status = 'pass'
        else:
            status = 'FAILED'
        msg = 'test_L_luminance.test_A() : y0 = %g (%s), L(y0) = %g, y(L(y0)) = %g, error = %g, %s' % (
            y0, range_info, L0, y1, error, status)
        if verbose >= 1:
            print msg
        if not passed:
            pass
            raise ValueError, msg
        return passed

    # Test B - Check that L_luminance() is the inverse of L_luminance_inverse()
    def test_B (L0, tolerance=1.0e-10, verbose=1):
        '''Check that L_luminance() is the inverse of L_luminance_inverse() for the given y0.'''
        # we should cover both ranges in the tests
        if (L0 > colormodels.L_LUM_C * colormodels.L_LUM_CUTOFF):
            range_info = 'in normal range'
        else:
            range_info = 'in linear range'
        y0 = colormodels.L_luminance_inverse (L0)
        L1 = colormodels.L_luminance (y0)
        # check error
        error = math.fabs (L1 - L0)
        passed = (error <= tolerance)
        if passed:
            status = 'pass'
        else:
            status = 'FAILED'
        msg = 'test_L_luminance.test_B() : L0 = %g (%s), y(L0) = %g, L(y(L0)) = %g, error = %g, %s' % (
            L0, range_info, y0, L1, error, status)
        if verbose >= 1:
            print msg
        if not passed:
            pass
            raise ValueError, msg
        return passed

    num_passed = 0
    num_failed = 0

    # Test A for fairly small y values (to ensure coverage of linear range)
    for i in xrange (0, 100):
        y0 = 0.1 * random.random()
        passed = test_A (y0, tolerance=1.0e-13, verbose=verbose)
        if passed:
            num_passed += 1
        else:
            num_failed += 1
        
    # Test A for fairly large y values
    for i in xrange (0, 100):
        y0 = 10.0 * random.random()
        passed = test_A (y0, tolerance=1.0e-13, verbose=verbose)
        if passed:
            num_passed += 1
        else:
            num_failed += 1

    # Test B for fairly small L values (to ensure coverage of linear range)
    for i in xrange (0, 100):
        L0 = 50.0 * random.random()
        passed = test_B (L0, tolerance=1.0e-10, verbose=verbose)
        if passed:
            num_passed += 1
        else:
            num_failed += 1
        
    # Test B for fairly large L values
    for i in xrange (0, 100):
        L0 = 1000.0 * random.random()
        passed = test_B (L0, tolerance=1.0e-10, verbose=verbose)
        if passed:
            num_passed += 1
        else:
            num_failed += 1

    msg = 'test_L_luminance() : %d tests passed, %d tests failed' % (
        num_passed, num_failed)
    print msg

# Utility function for Luv

def test_uv_primes (verbose=1):
    '''Test that uv_primes() and uv_primes_inverse() are inverses.'''

    def test_A (xyz0, tolerance=0.0, verbose=1):
        (up0, vp0) = colormodels.uv_primes (xyz0)
        xyz1 = colormodels.uv_primes_inverse (up0, vp0, xyz0[1])
        # check error
        dxyz = (xyz1 - xyz0)
        error = math.sqrt (numpy.dot (dxyz, dxyz))
        passed = (error <= tolerance)
        if passed:
            status = 'pass'
        else:
            status = 'FAILED'
        msg = 'test_uv_primes.test_A() : xyz0 = %s, (up,vp) = (%g,%g), xyz(up,vp) = %s, error = %g, %s' % (
            str (xyz0), up0, vp0, str(xyz1), error, status)
        if verbose >= 1:
            print msg
        if not passed:
            pass
            raise ValueError, msg
        return passed

    def test_B (up0, vp0, y0, tolerance=0.0, verbose=1):
        xyz0 = colormodels.uv_primes_inverse (up0, vp0, y0)
        (up1, vp1) = colormodels.uv_primes (xyz0)
        # check error
        error_up = up1 - up0
        error_vp = vp1 - vp0
        error = numpy.hypot (error_up, error_vp)
        passed = (error <= tolerance)
        if passed:
            status = 'pass'
        else:
            status = 'FAILED'
        msg = 'test_uv_primes.test_B() : (up0,vp0,y0) = (%g,%g,%g), xyz (up0,vp0,y0) = %s, (up,vp)(xyz) = (%g,%g), error = %g, %s' % (
            up0, vp0, y0, str (xyz0), up1, vp1, error, status)
        if verbose >= 1:
            print msg
        if not passed:
            pass
            raise ValueError, msg
        return passed
        
    num_passed = 0
    num_failed = 0

    # Test A
    for i in xrange (0, 100):
        x0 = 10.0 * random.random()
        y0 = 10.0 * random.random()
        z0 = 10.0 * random.random()
        xyz0 = colormodels.xyz_color (x0,y0,z0)
        passed = test_A (xyz0, tolerance=1.0e-13, verbose=verbose)
        if passed:
            num_passed += 1
        else:
            num_failed += 1
            
    # Test black case explicitly
    xyz0 = colormodels.xyz_color (0.0, 0.0, 0.0)    
    passed = test_A (xyz0, tolerance=0.0, verbose=verbose)
    if passed:
        num_passed += 1
    else:
        num_failed += 1

    # Test B
    for i in xrange (0, 100):
        up0 = 4.0 * (2.0 * random.random() - 1.0)
        vp0 = 9.0 * (2.0 * random.random() - 1.0)
        y0 = 10.0 * random.random()
        passed = test_B (up0, vp0, y0, tolerance=1.0e-13, verbose=verbose)
        if passed:
            num_passed += 1
        else:
            num_failed += 1

    # Test black case explicitly
    passed = test_B (0.0, 0.0, 0.0, tolerance=0.0, verbose=verbose)
    if passed:
        num_passed += 1
    else:
        num_failed += 1

    msg = 'test_uv_primes() : %d tests passed, %d tests failed' % (
        num_passed, num_failed)
    print msg

# Utility function for Lab
#     See [Kasson p.399] for details.
#     The linear range coefficient has more digits than in the paper,
#     this makes the function more continuous over the boundary.

def calc_LAB_F_A ():
    '''LAB_F_A should be ideally chosen so that the two models in Lab_f() agree exactly at the cutoff point.
    This is where the extra digits in LAB_F_A, over Kasson, come from.'''
    wanted = (math.pow (colormodels.L_LUM_CUTOFF, 1.0/3.0) - colormodels.LAB_F_B) / colormodels.L_LUM_CUTOFF
    print 'optimal LAB_F_A = %.16e' % (wanted)

def test_Lab_f (verbose=1):
    '''Test that Lab_f() and Lab_f_inverse() are really inverses.'''
    # Test A - Check that Lab_f_inverse() is the inverse of Lab_f()
    def test_A (t0, tolerance=1.0e-13, verbose=1):
        '''Check that Lab_f_inverse() is the inverse of Lab_f() for the given t0.'''
        # we should cover both ranges in the tests
        if (t0 > colormodels.L_LUM_CUTOFF):
            range_info = 'in normal range'
        else:
            range_info = 'in linear range'
        f0 = colormodels.Lab_f (t0)
        t1 = colormodels.Lab_f_inverse (f0)
        # check error
        error = math.fabs (t1 - t0)
        passed = (error <= tolerance)
        if passed:
            status = 'pass'
        else:
            status = 'FAILED'
        msg = 'test_Lab_f.test_A() : t0 = %g (%s), f(t0) = %g, t(f(t0)) = %g, error = %g, %s' % (
            t0, range_info, f0, t1, error, status)
        if verbose >= 1:
            print msg
        if not passed:
            pass
            raise ValueError, msg
        return passed

    # Test B - Check that Lab_f() is the inverse of Lab_f_inverse()
    def test_B (f0, tolerance=1.0e-10, verbose=1):
        '''Check that Lab_f() is the inverse of Lab_f_inverse() for the given f0.'''
        # we should cover both ranges in the tests
        if f0 > colormodels.LAB_F_A * colormodels.L_LUM_CUTOFF + colormodels.LAB_F_B:
            range_info = 'in normal range'
        else:
            range_info = 'in linear range'
        t0 = colormodels.Lab_f_inverse (f0)
        f1 = colormodels.Lab_f (t0)
        # check error
        error = math.fabs (f1 - f0)
        passed = (error <= tolerance)
        if passed:
            status = 'pass'
        else:
            status = 'FAILED'
        msg = 'test_Lab_f.test_B() : f0 = %g (%s), t(f0) = %g, f(t(f0)) = %g, error = %g, %s' % (
            f0, range_info, t0, f1, error, status)
        if verbose >= 1:
            print msg
        if not passed:
            pass
            raise ValueError, msg
        return passed

    num_passed = 0
    num_failed = 0

    # Test A for fairly small y values (to ensure coverage of linear range)
    for i in xrange (0, 100):
        y0 = 0.025 * random.random()
        passed = test_A (y0, tolerance=1.0e-13, verbose=verbose)
        if passed:
            num_passed += 1
        else:
            num_failed += 1

    # Test A for fairly large y values
    for i in xrange (0, 100):
        y0 = 10.0 * random.random()
        passed = test_A (y0, tolerance=1.0e-13, verbose=verbose)
        if passed:
            num_passed += 1
        else:
            num_failed += 1

    # Test B for fairly small L values (to ensure coverage of linear range)
    for i in xrange (0, 100):
        L0 = 0.25 * random.random()
        passed = test_B (L0, tolerance=1.0e-10, verbose=verbose)
        if passed:
            num_passed += 1
        else:
            num_failed += 1
        
    # Test B for fairly large L values
    for i in xrange (0, 100):
        L0 = 1000.0 * random.random()
        passed = test_B (L0, tolerance=1.0e-10, verbose=verbose)
        if passed:
            num_passed += 1
        else:
            num_failed += 1

    msg = 'test_Lab_f() : %d tests passed, %d tests failed' % (
        num_passed, num_failed)
    print msg

# Conversions between standard device independent color space (CIE XYZ)
# and the almost perceptually uniform space Luv.

def test_xyz_luv (verbose=1):
    '''Test that luv_from_xyz() and xyz_from_luv() are inverses.'''

    def test_A (xyz0, tolerance=1.0e-10, verbose=1):
        '''Test that luv_from_xyz() and xyz_from_luv() are inverses.'''
        luv0 = colormodels.luv_from_xyz (xyz0)
        xyz1 = colormodels.xyz_from_luv (luv0)
        luv1 = colormodels.luv_from_xyz (xyz1)
        # check errors
        dluv = luv1 - luv0
        error_luv = math.sqrt (numpy.dot (dluv, dluv))
        dxyz = xyz1 - xyz0
        error_xyz = math.sqrt (numpy.dot (dxyz, dxyz))
        passed = (error_luv <= tolerance) and (error_xyz <= tolerance)
        if passed:
            status = 'pass'
        else:
            status = 'FAILED'
        msg = 'test_xyz_luv.test_A() : xyz0 = %s, luv(xyz0) = %s, xyz(luv(xyz0)) = %s, luv(xyz(luv(xyz0))) = %s, errors = (%g, %g), %s' % (
            str (xyz0), str (luv0), str (xyz1), str (luv1), error_luv, error_xyz, status)
        if verbose >= 1:
            print msg
        if not passed:
            pass
            raise ValueError, msg
        return passed

    num_passed = 0
    num_failed = 0

    for i in xrange (0, 100):
        x0 = 10.0 * random.random()
        y0 = 10.0 * random.random()
        z0 = 10.0 * random.random()
        xyz0 = colormodels.xyz_color (x0,y0,z0)
        passed = test_A (xyz0, tolerance=1.0e-10, verbose=verbose)
        if passed:
            num_passed += 1
        else:
            num_failed += 1

    # Test black explicitly
    xyz0 = colormodels.xyz_color (0.0, 0.0, 0.0)
    passed = test_A (xyz0, tolerance=1.0e-10, verbose=verbose)
    if passed:
        num_passed += 1
    else:
        num_failed += 1

    msg = 'test_xyz_luv() : %d tests passed, %d tests failed' % (
        num_passed, num_failed)
    print msg

# Conversions between standard device independent color space (CIE XYZ)
# and the almost perceptually uniform space Lab.

def test_xyz_lab (verbose=1):
    '''Test that lab_from_xyz() and xyz_from_lab() are inverses.'''

    def test_A (xyz0, tolerance=1.0e-10, verbose=1):
        '''Test that lab_from_xyz() and xyz_from_lab() are inverses.'''
        lab0 = colormodels.lab_from_xyz (xyz0)
        xyz1 = colormodels.xyz_from_lab (lab0)
        lab1 = colormodels.lab_from_xyz (xyz1)
        # check errors
        dlab = lab1 - lab0
        error_lab = math.sqrt (numpy.dot (dlab, dlab))
        dxyz = xyz1 - xyz0
        error_xyz = math.sqrt (numpy.dot (dxyz, dxyz))
        passed = (error_lab <= tolerance) and (error_xyz <= tolerance)
        if passed:
            status = 'pass'
        else:
            status = 'FAILED'
        msg = 'test_xyz_lab.test_A() : xyz0 = %s, lab(xyz0) = %s, xyz(lab(xyz0)) = %s, lab(xyz(lab(xyz0))) = %s, errors = (%g, %g), %s' % (
            str (xyz0), str (lab0), str (xyz1), str (lab1), error_lab, error_xyz, status)
        if verbose >= 1:
            print msg
        if not passed:
            pass
            raise ValueError, msg
        return passed

    num_passed = 0
    num_failed = 0

    for i in xrange (0, 100):
        x0 = 10.0 * random.random()
        y0 = 10.0 * random.random()
        z0 = 10.0 * random.random()
        xyz0 = colormodels.xyz_color (x0,y0,z0)
        passed = test_A (xyz0, tolerance=1.0e-10, verbose=verbose)
        if passed:
            num_passed += 1
        else:
            num_failed += 1

    # Test black explicitly
    xyz0 = colormodels.xyz_color (0.0, 0.0, 0.0)
    passed = test_A (xyz0, tolerance=1.0e-10, verbose=verbose)
    if passed:
        num_passed += 1
    else:
        num_failed += 1

    msg = 'test_xyz_lab() : %d tests passed, %d tests failed' % (
        num_passed, num_failed)
    print msg

# Gamma correction

def test_gamma (verbose=1):
    if verbose >= 1:
        print 'Testing gamma corrections...'

    def test_gamma_corrections ():
        # test individual component gamma
        for i in xrange (0, 100):
            x = 10.0 * (2.0 * random.random() - 1.0)
            a = colormodels.linear_from_display_component (x)
            b = colormodels.display_from_linear_component (a)
            c = colormodels.linear_from_display_component (b)
            # check
            err1 = math.fabs (b - x)
            rel1 = math.fabs (err1 / (b + x))
            err2 = math.fabs (c - a)
            rel2 = math.fabs (err2 / (c + a))
            #print 'x = %g, b = %g, err = %g, rel = %g' % (x, b, err1, rel1)
            #print 'a = %g, c = %g, err = %g, rel = %g' % (a, c, err2, rel2)
            tolerance = 1.0e-14
            if rel1 > tolerance:
                raise ValueError
            if rel2 > tolerance:
                raise ValueError

    # test default sRGB component (cannot supply exponent)
    if verbose >= 1:
        print 'testing sRGB gamma'
    colormodels.init_gamma_correction (
        display_from_linear_function = colormodels.srgb_gamma_invert,
        linear_from_display_function = colormodels.srgb_gamma_correct)
    test_gamma_corrections()

    # test simple power law gamma (can supply exponent)    
    gamma_set = [0.1, 0.5, 1.0, 1.1, 1.5, 2.0, 2.2, 2.5, 10.0]
    for gamma in gamma_set:
        if verbose >= 1:
            print 'testing gamma', gamma
        colormodels.init_gamma_correction (
            display_from_linear_function = colormodels.simple_gamma_invert,
            linear_from_display_function = colormodels.simple_gamma_correct,
            gamma = gamma)
        test_gamma_corrections()

    print 'Passed test_gamma()'

# Linear (0.0-1.0) rgb to/from displayable (0-255) irgb

def test_irgb_string (verbose=1):
    '''Convert back and forth from irgb and irgb_string.'''
    for i in xrange (0, 100):
        ir = random.randrange (0, 256)
        ig = random.randrange (0, 256)
        ib = random.randrange (0, 256)
        irgb = colormodels.irgb_color (ir, ig, ib)
        irgb_string = colormodels.irgb_string_from_irgb (irgb)
        irgb2 = colormodels.irgb_from_irgb_string (irgb_string)
        irgb_string2 = colormodels.irgb_string_from_irgb (irgb2)
        if (irgb[0] != irgb2[0]) or (irgb[1] != irgb2[1]) or (irgb[2] != irgb2[2]):
            msg = 'irgb %s and irgb2 %s do not match' % (str (irgb), str (irgb2))
            raise ValueError, msg
        if (irgb_string != irgb_string2):
            msg = 'irgb_string %s and irgb_string2 %s do not match' % (irgb_string, irgb_string2)
            raise ValueError, msg
    if verbose >= 1:
        print 'Passed test_irgb_string()'

def test_rgb_irgb (verbose=1):
    '''Test that conversions between rgb and irgb are invertible.'''
    for i in xrange (0, 100):
        ir = random.randrange (0, 256)
        ig = random.randrange (0, 256)
        ib = random.randrange (0, 256)
        irgb0 = colormodels.irgb_color (ir, ig, ib)
        rgb0 = colormodels.rgb_from_irgb (irgb0)
        irgb1 = colormodels.irgb_from_rgb (rgb0)
        rgb1 = colormodels.rgb_from_irgb (irgb1)
        if (irgb0[0] != irgb1[0]) or (irgb0[1] != irgb1[1]) or (irgb0[2] != irgb1[2]):
            msg = 'irgb0 %s and irgb1 %s do not match' % (str (irgb0), str (irgb1))
            raise ValueError, msg
        tolerance = 1.0e-14
        err_rgb = rgb1 - rgb0
        err_r = math.fabs (err_rgb [0])
        err_g = math.fabs (err_rgb [1])
        err_b = math.fabs (err_rgb [2])
        if (err_r > tolerance) or (err_g > tolerance) or (err_b > tolerance):
            msg = 'rgb0 %s and rgb1 %s differ by %g' % (str (rgb0), str (rgb1), max (err_r,err_g,err_b))
            raise ValueError, msg
    if verbose >= 1:
        print 'Passed test_rgb_irgb()'

# Clipping

def test_clipping (verbose=1):
    '''Test the various color clipping methods.'''
    xyz_colors = ciexyz.get_normalized_spectral_line_colors ()
    #print 'xyz_colors', xyz_colors
    (num_wl, num_cols) = xyz_colors.shape
    # get rgb values for standard clipping
    colormodels.init_clipping (colormodels.CLIP_ADD_WHITE)
    rgb_add_white = []
    for i in xrange (0, num_wl):
        color = colormodels.irgb_string_from_rgb (
            colormodels.rgb_from_xyz (xyz_colors [i]))
        rgb_add_white.append (color)
    # get rgb values for clamp clipping
    colormodels.init_clipping (colormodels.CLIP_CLAMP_TO_ZERO)
    rgb_clamp = []
    for i in xrange (0, num_wl):
        color = colormodels.irgb_string_from_rgb (
            colormodels.rgb_from_xyz (xyz_colors [i]))
        rgb_clamp.append (color)
    # compare
    if verbose >= 1:
        print 'colors from add white, colors from clamp'
        for i in xrange (0, num_wl):
            print rgb_add_white [i], rgb_clamp [i]
    print 'Passed test_clipping()'
            
#
# Main test routine for the conversions
#

def test (verbose=0):
    '''Test suite for color model conversions.'''
    test_xyz_rgb (verbose=verbose)
    test_xyz_irgb (verbose=verbose)
    test_L_luminance (verbose=verbose)
    test_Lab_f (verbose=verbose)
    test_uv_primes (verbose=verbose)
    test_xyz_luv (verbose=verbose)
    test_xyz_lab (verbose=verbose)
    test_gamma (verbose=0)
    test_irgb_string (verbose=1)
    test_rgb_irgb (verbose=1)
    test_clipping (verbose=0)
