'''
percept.py - (Almost) perceptually uniform color spaces Lab and Luv.

Description:

Luv - A nearly perceptually uniform color space.

Lab - Another nearly perceptually uniform color space.

As far as I know, the Luv and Lab spaces are of similar quality.
Neither is perfect, so perhaps try each, and see what works best for your application.

Functions:

Initialization functions:

init_Luv_Lab_white_point (white_point) -
    Specify the white point to use for Luv/Lab conversions.

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

import colormodels

#
# Color model conversions to (nearly) perceptually uniform spaces Luv and Lab.
#

# Luminance function [of Y value of an XYZ color] used in Luv and Lab. See [Kasson p.399] for details.
# The linear range coefficient L_LUM_C has more digits than in the paper,
# this makes the function more continuous over the boundary.

L_LUM_A      = 116.0
L_LUM_B      = 16.0
L_LUM_C      = 903.29629551307664
L_LUM_CUTOFF = 0.008856

def L_luminance (y):
    '''L coefficient for Luv and Lab models.'''
    if y > L_LUM_CUTOFF:
        return L_LUM_A * math.pow (y, 1.0/3.0) - L_LUM_B
    else:
        # linear range
        return L_LUM_C * y

def L_luminance_inverse (L):
    '''Inverse of L_luminance().'''
    if L <= (L_LUM_C * L_LUM_CUTOFF):
        # linear range
        y = L / L_LUM_C
    else:
        t = (L + L_LUM_B) / L_LUM_A
        y = math.pow (t, 3)
    return y

# Utility function for Luv

def uv_primes (xyz):
    '''Luv utility.'''
    x = xyz [0]
    y = xyz [1]
    z = xyz [2]
    w_denom = x + 15.0 * y + 3.0 * z
    if w_denom != 0.0:
        u_prime = 4.0 * x / w_denom
        v_prime = 9.0 * y / w_denom
    else:
        # this should only happen when x=y=z=0 [i.e. black] since xyz values are positive
        u_prime = 0.0
        v_prime = 0.0
    return (u_prime, v_prime)

def uv_primes_inverse (u_prime, v_prime, y):
    '''Inverse of uv_primes(). We will always have y known when this is called.'''
    if v_prime != 0.0:
        # normal
        w_denom = (9.0 * y) / v_prime
        x = 0.25 * u_prime * w_denom
        y = y
        z = (w_denom - x - 15.0 * y) / 3.0
    else:
        # should only happen when color is totally black
        x = 0.0
        y = 0.0
        z = 0.0
    xyz = colormodels.xyz_color (x, y, z)
    return xyz

# Utility function for Lab
#     See [Kasson p.399] for details.
#     The linear range coefficient has more digits than in the paper,
#     this makes the function more continuous over the boundary.

LAB_F_A = 7.7870370302851422
LAB_F_B = (16.0/116.0)
# same cutoff as L_luminance()

def Lab_f (t):
    '''Lab utility function.'''
    if t > L_LUM_CUTOFF:
        return math.pow (t, 1.0/3.0)
    else:
        # linear range
        return LAB_F_A * t + LAB_F_B

def Lab_f_inverse (F):
    '''Inverse of Lab_f().'''
    if F <= (LAB_F_A * L_LUM_CUTOFF + LAB_F_B):
        # linear range
        t = (F - LAB_F_B) / LAB_F_A
    else:
        t = math.pow (F, 3)
    return t

#
# Color model conversions to (nearly) perceptually uniform spaces Luv and Lab.
#

# Conversions between standard device independent color space (CIE XYZ)
# and the almost perceptually uniform space Luv.

def luv_from_xyz(xyz, reference_white, reference_u_prime, reference_v_prime):
    ''' Convert CIE XYZ to Luv. '''
    y = xyz [1]
    y_p = y / reference_white [1]       # reference_white [1] is normally 1.0.
    u_prime, v_prime = uv_primes (xyz)
    L = L_luminance (y_p)
    u = 13.0 * L * (u_prime - reference_u_prime)
    v = 13.0 * L * (v_prime - reference_v_prime)
    luv = colormodels.luv_color (L, u, v)
    return luv

def xyz_from_luv(luv, XXreference_white, reference_u_prime, reference_v_prime):
    '''Convert Luv to CIE XYZ.  Inverse of luv_from_xyz().'''
    L = luv [0]
    u = luv [1]
    v = luv [2]
    # Invert L_luminance() to get y.
    y = L_luminance_inverse (L)
    if L != 0.0:
        # Color is not totally black.
        # Get u_prime, v_prime.
        L13 = 13.0 * L
        u_prime = reference_u_prime + (u / L13)
        v_prime = reference_v_prime + (v / L13)
        # Get xyz color.
        xyz = uv_primes_inverse (u_prime, v_prime, y)
    else:
        # Color is black.
        xyz = colormodels.xyz_color (0.0, 0.0, 0.0)
    return xyz

# Conversions between standard device independent color space (CIE XYZ)
# and the almost perceptually uniform space Lab.

def lab_from_xyz(xyz, reference_white):
    '''Convert color from CIE XYZ to Lab.'''
    x = xyz [0]
    y = xyz [1]
    z = xyz [2]

    x_p = x / reference_white [0]
    y_p = y / reference_white [1]
    z_p = z / reference_white [2]

    f_x = Lab_f (x_p)
    f_y = Lab_f (y_p)
    f_z = Lab_f (z_p)

    L = L_luminance (y_p)
    a = 500.0 * (f_x - f_y)
    b = 200.0 * (f_y - f_z)
    Lab = colormodels.lab_color (L, a, b)
    return Lab

def xyz_from_lab(Lab, reference_white):
    '''Convert color from Lab to CIE XYZ.  Inverse of lab_from_xyz().'''
    L = Lab [0]
    a = Lab [1]
    b = Lab [2]
    # invert L_luminance() to get y_p
    y_p = L_luminance_inverse (L)
    # calculate f_y
    f_y = Lab_f (y_p)
    # solve for f_x and f_z
    f_x = f_y + (a / 500.0)
    f_z = f_y - (b / 200.0)
    # invert Lab_f() to get x_p and z_p
    x_p = Lab_f_inverse (f_x)
    z_p = Lab_f_inverse (f_z)
    # multiply by reference white to get xyz
    x = x_p * reference_white [0]
    y = y_p * reference_white [1]
    z = z_p * reference_white [2]
    xyz = colormodels.xyz_color (x, y, z)
    return xyz

#
# Class to hold color conversion values.
#

class PerceptualConverter(object):
    ''' An object to convert between (almost) perceptually uniform color spaces. '''

    def __init__ (self,
        #white_point = colormodels.SRGB_White):
        white_point):
        ''' Initialize the color conversions. '''
        # xyz <-> Luv and Lab conversions need white point.
        self.init_Luv_Lab_white_point(white_point)

    def init_Luv_Lab_white_point(self, white_point):
        ''' Specify the white point to use for Luv/Lab conversions. '''
        self.reference_white = white_point.copy()
        colormodels.xyz_normalize_Y1 (self.reference_white)
        self.reference_u_prime, self.reference_v_prime = uv_primes (self.reference_white)

    # Conversions between standard device independent color space (CIE XYZ)
    # and the almost perceptually uniform space Luv.

    def luv_from_xyz(self, xyz):
        '''Convert CIE XYZ to Luv.'''
        luv = luv_from_xyz(
            xyz,
            self.reference_white,
            self.reference_u_prime,
            self.reference_v_prime)
        return luv

    def xyz_from_luv(self, luv):
        '''Convert Luv to CIE XYZ.  Inverse of luv_from_xyz().'''
        xyz = xyz_from_luv(
            luv,
            self.reference_white,
            self.reference_u_prime,
            self.reference_v_prime)
        return xyz

    # Conversions between standard device independent color space (CIE XYZ)
    # and the almost perceptually uniform space Lab.

    def lab_from_xyz(self, xyz):
        '''Convert color from CIE XYZ to Lab.'''
        lab = lab_from_xyz(xyz, self.reference_white)
        return lab

    def xyz_from_lab(self, Lab):
        '''Convert color from Lab to CIE XYZ.  Inverse of lab_from_xyz().'''
        xyz = xyz_from_lab(Lab, self.reference_white)
        return xyz
