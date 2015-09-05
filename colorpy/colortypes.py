'''
colortypes.py - Basic types for colors.

Description:

The models store color values as 3-element NumPy vectors.
The values are stored as floats, except for irgb, which are stored as integers.

Functions:

'Constructor-like' functions:

xyz_color (x, y, z = None) -
    Construct an xyz color.  If z is omitted, set it so that x+y+z = 1.0.

xyz_normalize (xyz) -
    Scale so that all values add to 1.0.
    This both modifies the passed argument and returns the normalized result.

xyz_normalize_Y1 (xyz) -
    Scale so that the y component is 1.0.
    This both modifies the passed argument and returns the normalized result.

xyz_color_from_xyY (x, y, Y) -
    Given the 'little' x,y chromaticity, and the intensity Y,
    construct an xyz color.  See Foley/Van Dam p. 581, eq. 13.21.

rgb_color (r, g, b) -
    Construct a linear rgb color from components.

irgb_color (ir, ig, ib) -
    Construct a displayable integer irgb color from components.

luv_color (L, u, v) -
    Construct a Luv color from components.

lab_color (L, a, b) -
    Construct a Lab color from components.

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

import numpy

#
# Constructor functions for colors in the various color models.
# This is a separate module to allow a lightweight import of the types only.
#

# The xyz constructors have some special versions to handle some common situations.

def xyz_color (x, y, z = None):
    '''Construct an xyz color.  If z is omitted, set it so that x+y+z = 1.0.'''
    if z == None:
        # choose z so that x+y+z = 1.0
        z = 1.0 - (x + y)
    rtn = numpy.array ([x, y, z])
    return rtn

def xyz_normalize (xyz):
    '''Scale so that all values add to 1.0.
    This both modifies the passed argument and returns the normalized result.'''
    sum_xyz = xyz[0] + xyz[1] + xyz[2]
    if sum_xyz != 0.0:
        scale = 1.0 / sum_xyz
        xyz [0] *= scale
        xyz [1] *= scale
        xyz [2] *= scale
    return xyz

def xyz_normalize_Y1 (xyz):
    '''Scale so that the y component is 1.0.
    This both modifies the passed argument and returns the normalized result.'''
    if xyz [1] != 0.0:
        scale = 1.0 / xyz [1]
        xyz [0] *= scale
        xyz [1] *= scale
        xyz [2] *= scale
    return xyz

def xyz_color_from_xyY (x, y, Y):
    '''Given the 'little' x,y chromaticity, and the intensity Y,
    construct an xyz color.  See Foley/Van Dam p. 581, eq. 13.21.'''
    return xyz_color (
        (x/y)* Y,
        Y,
        (1.0-x-y)/(y) * Y)

# Simple constructors for the remaining models.

def rgb_color (r, g, b):
    '''Construct a linear rgb color from components.'''
    rtn = numpy.array ([r, g, b])
    return rtn

def irgb_color (ir, ig, ib):
    '''Construct a displayable integer irgb color from components.'''
    rtn = numpy.array ([ir, ig, ib], int)
    return rtn

def luv_color (L, u, v):
    '''Construct a Luv color from components.'''
    rtn = numpy.array ([L, u, v])
    return rtn

def lab_color (L, a, b):
    '''Construct a Lab color from components.'''
    rtn = numpy.array ([L, a, b])
    return rtn
