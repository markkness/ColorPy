'''
colormodels.py - Conversions between color models

Description:

Defines several color models, and conversions between them.

The models are:

xyz - CIE XYZ color space, based on the 1931 matching functions for a 2 degree field of view.
    Spectra are converted to xyz color values by integrating with the matching functions in ciexyz.py.

    xyz colors are often handled as absolute values, conventionally written with uppercase letters XYZ,
    or as scaled values (so that X+Y+Z = 1.0), conventionally written with lowercase letters xyz.

    This is the fundamental color model around which all others are based.

rgb - Colors expressed as red, green and blue values, in the nominal range 0.0 - 1.0.
    These are linear color values, meaning that doubling the number implies a doubling of the light intensity.
    rgb color values may be out of range (greater than 1.0, or negative), and do not account for gamma correction.
    They should not be drawn directly.

irgb - Displayable color values expressed as red, green and blue values, in the range 0 - 255.
    These have been adjusted for gamma correction, and have been clipped into the displayable range 0 - 255.
    These color values can be drawn directly.

Luv - A nearly perceptually uniform color space.

Lab - Another nearly perceptually uniform color space.

As far as I know, the Luv and Lab spaces are of similar quality.
Neither is perfect, so perhaps try each, and see what works best for your application.

The models store color values as 3-element NumPy vectors.
The values are stored as floats, except for irgb, which are stored as integers.

Constants:

SRGB_Red
SRGB_Green
SRGB_Blue
SRGB_White -
    Chromaticity values for sRGB standard display monitors.

PhosphorRed
PhosphorGreen
PhosphorBlue
PhosphorWhite -
    Chromaticity values for display used in initialization.
    These are the sRGB values by default, but other values can be chosen.

CLIP_CLAMP_TO_ZERO = 0
CLIP_ADD_WHITE     = 1
    Available color clipping methods.  Add white is the default.

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

Conversion functions:

rgb_from_xyz (xyz) -
    Convert an xyz color to rgb.

xyz_from_rgb (rgb) -
    Convert an rgb color to xyz.

irgb_string_from_irgb (irgb) -
    Convert a displayable irgb color (0-255) into a hex string.

irgb_from_irgb_string (irgb_string) -
    Convert a color hex string (like '#AB13D2') into a displayable irgb color.

irgb_from_rgb (rgb) -
    Convert a (linear) rgb value (range 0.0 - 1.0) into a 0-255 displayable integer irgb value (range 0 - 255).

rgb_from_irgb (irgb) -
    Convert a displayable (gamma corrected) irgb value (range 0 - 255) into a linear rgb value (range 0.0 - 1.0).

irgb_string_from_rgb (rgb) -
    Clip the rgb color, convert to a displayable color, and convert to a hex string.

irgb_from_xyz (xyz) -
    Convert an xyz color directly into a displayable irgb color.

irgb_string_from_xyz (xyz) -
    Convert an xyz color directly into a displayable irgb color hex string.

luv_from_xyz (xyz) -
    Convert CIE XYZ to Luv.

xyz_from_luv (luv) -
    Convert Luv to CIE XYZ.  Inverse of luv_from_xyz().

lab_from_xyz (xyz) -
    Convert color from CIE XYZ to Lab.

xyz_from_lab (Lab) -
    Convert color from Lab to CIE XYZ.  Inverse of lab_from_xyz().

Gamma correction:

simple_gamma_invert (x) -
    Simple power law for gamma inverse correction.
    Not used by default.

simple_gamma_correct (x) -
    Simple power law for gamma correction.
    Not used by default.

srgb_gamma_invert (x) -
    sRGB standard for gamma inverse correction.
    This is used by default.

srgb_gamma_correct (x) -
    sRGB standard for gamma correction.
    This is used by default.

Color clipping:

clip_rgb_color (rgb_color) -
    Convert a linear rgb color (nominal range 0.0 - 1.0), into a displayable
    irgb color with values in the range (0 - 255), clipping as necessary.

    The return value is a tuple, the first element is the clipped irgb color,
    and the second element is a tuple indicating which (if any) clipping processes were used.

Initialization functions:

init (
    phosphor_red   = SRGB_Red,
    phosphor_green = SRGB_Green,
    phosphor_blue  = SRGB_Blue,
    white_point    = SRGB_White) -

    Setup the conversions between CIE XYZ and linear RGB spaces.
    Also do other initializations (gamma, conversions with Luv and Lab spaces, clipping model).
    The default arguments correspond to the sRGB standard RGB space.
    The conversion is defined by supplying the chromaticities of each of
    the monitor phosphors, as well as the resulting white color when all
    of the phosphors are at full strength.
    See [Foley/Van Dam, p.587, eqn 13.27, 13.29] and [Hall, p. 239].

init_Luv_Lab_white_point (white_point) -
    Specify the white point to use for Luv/Lab conversions.

init_gamma_correction (
    display_from_linear_function = srgb_gamma_invert,
    linear_from_display_function = srgb_gamma_correct,
    gamma = STANDARD_GAMMA) -

    Setup gamma correction.
    The functions used for gamma correction/inversion can be specified,
    as well as a gamma value.
    The specified display_from_linear_function should convert a
    linear (rgb) component [proportional to light intensity] into
    displayable component [proportional to palette values].
    The specified linear_from_display_function should convert a
    displayable (rgb) component [proportional to palette values]
    into a linear component [proportional to light intensity].
    The choices for the functions:
    display_from_linear_function -
        srgb_gamma_invert [default] - sRGB standard
        simple_gamma_invert - simple power function, can specify gamma.
    linear_from_display_function -
        srgb_gamma_correct [default] - sRGB standard
        simple_gamma_correct - simple power function, can specify gamma.
    The gamma parameter is only used for the simple() functions,
    as sRGB implies an effective gamma of 2.2.

init_clipping (clip_method = CLIP_ADD_WHITE) -
    Specify the color clipping method.

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

import gamma
#import percept

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

#
# Chromaticities of standard phosphors and white points.
#
# sRGB (ITU-R BT.709) standard phosphor chromaticities
#
SRGB_Red   = xyz_color (0.640,  0.330)
SRGB_Green = xyz_color (0.300,  0.600)
SRGB_Blue  = xyz_color (0.150,  0.060)
SRGB_White = xyz_color (0.3127, 0.3290)    # Illuminant D65

#
# Conversions between CIE XYZ and RGB colors.
#     Assumptions must be made about the specific device to construct the conversions.
#

def rgb_from_xyz (xyz):
    '''Convert an xyz color to rgb.'''
    return color_converter.rgb_from_xyz (xyz)

def xyz_from_rgb (rgb):
    '''Convert an rgb color to xyz.'''
    return color_converter.xyz_from_rgb (rgb)

# Conversion from xyz to rgb, while also scaling the brightness to the maximum displayable.

def brightest_rgb_from_xyz (xyz, max_component=1.0):
    '''Convert the xyz color to rgb, and scale to maximum displayable brightness, so one of the components will be 1.0 (or max_component).'''
    rgb = rgb_from_xyz (xyz)
    max_rgb = max (rgb)
    if max_rgb != 0.0:
        scale = max_component / max_rgb
        rgb *= scale
    return rgb

# Conversions between standard device independent color space (CIE XYZ)
# and the almost perceptually uniform space Luv.

def luv_from_xyz (xyz):
    '''Convert CIE XYZ to Luv.'''
    return color_converter.luv_from_xyz(xyz)

def xyz_from_luv (luv):
    '''Convert Luv to CIE XYZ.  Inverse of luv_from_xyz().'''
    return color_converter.xyz_from_luv(luv)

# Conversions between standard device independent color space (CIE XYZ)
# and the almost perceptually uniform space Lab.

def lab_from_xyz (xyz):
    '''Convert color from CIE XYZ to Lab.'''
    return color_converter.lab_from_xyz(xyz)

def xyz_from_lab (Lab):
    '''Convert color from Lab to CIE XYZ.  Inverse of lab_from_xyz().'''
    return color_converter.xyz_from_lab(Lab)

#
# Gamma correction
#
# Non-gamma corrected rgb values, also called non-linear rgb values,
# correspond to palette register entries [although here they are kept
# in the range 0.0 to 1.0.]  The numerical values are not proportional
# to the amount of light energy present.
#
# Gamma corrected rgb values, also called linear rgb values,
# do not correspond to palette entries.  The numerical values are
# proportional to the amount of light energy present.
#

# Available gamma correction methods.
GAMMA_CORRECT_SRGB     = 0    # sRGB/HDTV correction formula.
GAMMA_CORRECT_UHDTV10  = 1    # Rec 2020/UHDTV for 10 bits per component.
GAMMA_CORRECT_UHDTV12  = 2    # Rec 2020/UHDTV for 12 bits per component.
GAMMA_CORRECT_POWER    = 3    # Simple power law, using supplied gamma exponent.
GAMMA_CORRECT_FUNCTION = 4    # Explicitly supplied conversion functions.

def display_from_linear_component(x):
    ''' Gamma invert a single value. '''
    y = color_converter.gamma_converter.display_from_linear(x)
    return y

def linear_from_display_component(x):
    ''' Gamma correct a single value. '''
    y = color_converter.gamma_converter.linear_from_display(x)
    return y

#
# Color clipping - Physical color values may exceed the what the display can show,
#   either because the color is too pure (indicated by negative rgb values), or
#   because the color is too bright (indicated by rgb values > 1.0).
#   These must be clipped to something displayable.
#

# possible color clipping methods
CLIP_CLAMP_TO_ZERO = 0
CLIP_ADD_WHITE     = 1

def clip_rgb_color (rgb_color):
    '''Convert a linear rgb color (nominal range 0.0 - 1.0), into a displayable
    irgb color with values in the range (0 - 255), clipping as necessary.

    The return value is a tuple, the first element is the clipped irgb color,
    and the second element is a tuple indicating which (if any) clipping processes were used.
    '''
    return color_converter.clip_rgb_color (rgb_color)

#
# Conversions between linear rgb colors (range 0.0 - 1.0, values proportional to light intensity)
# and displayable irgb colors (range 0 - 255, values corresponding to hardware palette values).
#
# Displayable irgb colors can be represented as hex strings, like '#AB05B4'.
#

def irgb_string_from_irgb (irgb):
    '''Convert a displayable irgb color (0-255) into a hex string.'''
    # ensure that values are in the range 0-255
    for index in range (0, 3):
        irgb [index] = min (255, max (0, irgb [index]))
    # convert to hex string
    irgb_string = '#%02X%02X%02X' % (irgb [0], irgb [1], irgb [2])
    return irgb_string

def irgb_from_irgb_string (irgb_string):
    '''Convert a color hex string (like '#AB13D2') into a displayable irgb color.'''
    strlen = len (irgb_string)
    if strlen != 7:
        raise ValueError('irgb_string_from_irgb(): Expecting 7 character string like #AB13D2')
    if irgb_string [0] != '#':
        raise ValueError('irgb_string_from_irgb(): Expecting 7 character string like #AB13D2')
    irs = irgb_string [1:3]
    igs = irgb_string [3:5]
    ibs = irgb_string [5:7]
    ir = int (irs, 16)
    ig = int (igs, 16)
    ib = int (ibs, 16)
    irgb = irgb_color (ir, ig, ib)
    return irgb

def irgb_from_rgb (rgb):
    '''Convert a (linear) rgb value (range 0.0 - 1.0) into a 0-255 displayable integer irgb value (range 0 - 255).'''
    return color_converter.irgb_from_rgb (rgb)

def rgb_from_irgb (irgb):
    '''Convert a displayable (gamma corrected) irgb value (range 0 - 255) into a linear rgb value (range 0.0 - 1.0).'''
    return color_converter.rgb_from_irgb (irgb)

def irgb_string_from_rgb (rgb):
    '''Clip the rgb color, convert to a displayable color, and convert to a hex string.'''
    return irgb_string_from_irgb (irgb_from_rgb (rgb))

# Multi-level conversions, for convenience

def irgb_from_xyz (xyz):
    '''Convert an xyz color directly into a displayable irgb color.'''
    return irgb_from_rgb (rgb_from_xyz (xyz))

def irgb_string_from_xyz (xyz):
    '''Convert an xyz color directly into a displayable irgb color hex string.'''
    return irgb_string_from_rgb (rgb_from_xyz (xyz))

#
# Class to hold color conversion values.
#

# FIXME: Should not need this again. Utility function for Luv

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

# FIXME: Should be able to specify maximum value rather than bit depth.

class ColorConverter(object):
    ''' An object to keep track of how to convert between color spaces. '''

    def __init__ (self,
        phosphor_red       = SRGB_Red,
        phosphor_green     = SRGB_Green,
        phosphor_blue      = SRGB_Blue,
        white_point        = SRGB_White,
        gamma_method       = GAMMA_CORRECT_SRGB,
        gamma_value        = None,
        gamma_correct_func = None,
        gamma_invert_func  = None,
        clip_method        = CLIP_ADD_WHITE,
        bit_depth          = 8):
        ''' Initialize the color conversions. '''
        # xyz <-> rgb conversions need phosphor chromaticities and white point.
        self.init_rgb_xyz(
            phosphor_red, phosphor_green, phosphor_blue, white_point)
        # xyz <-> Luv and Lab conversions need white point.
        self.init_Luv_Lab_white_point(white_point)
        # Gamma correction method.
        self.init_gamma_correction(
            gamma_method, gamma_value, gamma_correct_func, gamma_invert_func)
        # Clipping method.
        self.init_clipping(clip_method)
        # Bit depth for integer rgb values.
        self.init_bit_depth(bit_depth)

    def init_rgb_xyz(self,
        phosphor_red,
        phosphor_green,
        phosphor_blue,
        white_point):
        '''Setup the conversions between CIE XYZ and linear RGB spaces.

        The default arguments correspond to the sRGB standard RGB space.
        The conversion is defined by supplying the chromaticities of each of
        the monitor phosphors, as well as the resulting white color when all
        of the phosphors are at full strength.

        See [Foley/Van Dam, p.587, eqn 13.27, 13.29] and [Hall, p. 239].
        '''
        # xyz colors of the monitor phosphors (and full white).
        self.PhosphorRed   = phosphor_red
        self.PhosphorGreen = phosphor_green
        self.PhosphorBlue  = phosphor_blue
        self.PhosphorWhite = white_point
        phosphor_matrix = numpy.column_stack ((phosphor_red, phosphor_green, phosphor_blue))
        # Normalize white point to Y=1.0.
        normalized_white = white_point.copy()
        xyz_normalize_Y1 (normalized_white)
        # Determine intensities of each phosphor by solving:
        #     phosphor_matrix * intensity_vector = white_point
        intensities = numpy.linalg.solve (phosphor_matrix, normalized_white)
        # Construct xyz_from_rgb matrix from the results.
        self.xyz_from_rgb_matrix = numpy.column_stack (
            (phosphor_red   * intensities [0],
             phosphor_green * intensities [1],
             phosphor_blue  * intensities [2]))
        # Invert to get rgb_from_xyz matrix.
        self.rgb_from_xyz_matrix = numpy.linalg.inv (self.xyz_from_rgb_matrix)

    def init_Luv_Lab_white_point(self, white_point):
        ''' Specify the white point to use for Luv/Lab conversions. '''
        #import percept            # Avoid circular import.
        self.reference_white = white_point.copy()
        xyz_normalize_Y1 (self.reference_white)
        self.reference_u_prime, self.reference_v_prime = uv_primes (self.reference_white)
        #self.percept_converter = percept.PerceptualConverter(self.reference_white)

    def init_gamma_correction(self,
        gamma_method,          # gamma conversion method.
        gamma_value,           # gamma exponent value, for GAMMA_CORRECT_POWER.
        gamma_correct_func,    # linear_from_display function, for GAMMA_CORRECT_FUNCTION.
        gamma_invert_func):    # display_from_linear function, for GAMMA_CORRECT_FUNCTION.
        '''Specify the gamma correction method.

        Gamma correction converts rgb components, in 0.0 - 1.0 range,
        between linear values, proportional to light intensity,
        and displayable values, proportional to palette values.

        The choices for the method:
        GAMMA_CORRECT_SRGB:
            Apply the sRGB correction formula, with improvements to K0, Phi.
            The gamma exponent, and correction and inversion functions are ignored.
            The effective gamma is about 2.2.
        GAMMA_CORRECT_UHDTV10:
            Apply the UHDTV/Rec-2020 correction formula, for 10-bit color depth.
            The gamma exponent, and correction and inversion functions are ignored.
        GAMMA_CORRECT_UHDTV12:
            Apply the UHDTV/Rec-2020 correction formula, for 12-bit color depth.
            The gamma exponent, and correction and inversion functions are ignored.
        GAMMA_CORRECT_POWER:
            Apply a simple exponent conversion.
            The gamma exponent value must be specified.
        GAMMA_CORRECT_FUNCTION:
            Apply explicitly supplied correction and inversion functions.
            The gamma exponent is ignored.
        '''
        if gamma_method == GAMMA_CORRECT_SRGB:
            self.gamma_converter = gamma.srgb_gamma_converter
        elif gamma_method == GAMMA_CORRECT_UHDTV10:
            self.gamma_converter = gamma.uhdtv10_gamma_converter
        elif gamma_method == GAMMA_CORRECT_UHDTV12:
            self.gamma_converter = gamma.uhdtv12_gamma_converter
        elif gamma_method == GAMMA_CORRECT_POWER:
            self.gamma_converter = gamma.GammaConverterPower(gamma=gamma_value)
        elif gamma_method == GAMMA_CORRECT_FUNCTION:
            self.gamma_converter = gamma.GammaConverterFunction(
                display_from_linear_func=gamma_invert_func,
                linear_from_display_func=gamma_correct_func)
        else:
            raise ValueError('Invalid gamma correction method %s' % (str(gamma_method)))

    def init_clipping(self, clip_method):
        '''Specify the color clipping method.'''
        if not clip_method in [CLIP_CLAMP_TO_ZERO, CLIP_ADD_WHITE]:
            raise ValueError('Invalid color clipping method %s' % (str(clip_method)))
        self.clip_method = clip_method

    def init_bit_depth(self, bit_depth):
        ''' Initialize the bit depth for displayable integer rgb colors. '''
        self.bit_depth = bit_depth
        self.max_value = (1 << self.bit_depth) - 1

    def dump(self):
        ''' Print some info about the color conversions. '''
        print ('xyz_from_rgb', str (self.xyz_from_rgb_matrix))
        print ('rgb_from_xyz', str (self.rgb_from_xyz_matrix))
        # Bit depth.
        print ('bit_depth = %d' % (self.bit_depth))
        print ('max_value = %d' % (self.max_value))

    # Conversions between xyz and rgb.
    # (rgb here is linear, not gamma adjusted.)

    def rgb_from_xyz(self, xyz):
        '''Convert an xyz color to rgb.'''
        return numpy.dot (self.rgb_from_xyz_matrix, xyz)

    def xyz_from_rgb(self, rgb):
        '''Convert an rgb color to xyz.'''
        return numpy.dot (self.xyz_from_rgb_matrix, rgb)

    # Conversions between standard device independent color space (CIE XYZ)
    # and the almost perceptually uniform space Luv.

    def luv_from_xyz(self, xyz):
        '''Convert CIE XYZ to Luv.'''
        import percept            # Avoid circular import.
        luv = percept.luv_from_xyz(
            xyz,
            self.reference_white,
            self.reference_u_prime,
            self.reference_v_prime)
        return luv

    def xyz_from_luv(self, luv):
        '''Convert Luv to CIE XYZ.  Inverse of luv_from_xyz().'''
        import percept            # Avoid circular import.
        xyz = percept.xyz_from_luv(
            luv,
            self.reference_white,
            self.reference_u_prime,
            self.reference_v_prime)
        return xyz

    # Conversions between standard device independent color space (CIE XYZ)
    # and the almost perceptually uniform space Lab.

    def lab_from_xyz(self, xyz):
        '''Convert color from CIE XYZ to Lab.'''
        import percept            # Avoid circular import.
        lab = percept.lab_from_xyz(xyz, self.reference_white)
        return lab

    def xyz_from_lab(self, Lab):
        '''Convert color from Lab to CIE XYZ.  Inverse of lab_from_xyz().'''
        import percept            # Avoid circular import.
        xyz = percept.xyz_from_lab(Lab, self.reference_white)
        return xyz

    # Conversion of linear rgb color (range 0.0 - 1.0) to displayable values (range 0 - 255).

    # Clipping of undisplayable colors.

    def clip_color_clamp(self, rgb):
        ''' Clip an rgb color to remove negative components.
        Any negative components are zeroed. '''
        # The input color is modified as necessary.
        clipped = False
        # Set negative rgb values to zero.
        if rgb [0] < 0.0:
            rgb [0] = 0.0
            clipped = True
        if rgb [1] < 0.0:
            rgb [1] = 0.0
            clipped = True
        if rgb [2] < 0.0:
            rgb [2] = 0.0
            clipped = True
        return clipped

    def clip_color_whiten(self, rgb):
        ''' Clip an rgb color to remove negative components.
        White is added as necessary to remove any negative components. '''
        # The input color is modified as necessary.
        clipped = False
        # Add enough white to make all rgb values nonnegative.
        rgb_min = min (0.0, min (rgb))
        # Get scaling factor to maintain max rgb after adding white.
        rgb_max = max (rgb)
        scaling = 1.0
        if rgb_max > 0.0:
            scaling = rgb_max / (rgb_max - rgb_min)
        # Add white and scale.
        if rgb_min < 0.0:
            rgb [0] = scaling * (rgb [0] - rgb_min);
            rgb [1] = scaling * (rgb [1] - rgb_min);
            rgb [2] = scaling * (rgb [2] - rgb_min);
            clipped = True
        return clipped

    def clip_color_intensity(self, rgb):
        ''' Scale an rgb color if needed to the component range 0.0 - 1.0. '''
        # The input color is modified as necessary.
        clipped = False
        rgb_max = max (rgb)
        # Does not actually overflow until 2^B * intensity > (2^B + 0.5).
        intensity_cutoff = 1.0 + (0.5 / self.max_value)
        if rgb_max > intensity_cutoff:
            scaling = intensity_cutoff / rgb_max
            rgb *= scaling
            clipped = True
        return clipped

    # Gamma correction, to convert between linear and displayable values.
    # Linear  = Component value is proportional to physical light intensity.
    # Display = Component value is appropriate to display on monitor.

    def display_from_linear_component(self, x):
        ''' Gamma invert a value (nominal range 0.0 - 1.0)
        to convert from linear to displayable values. '''
        y = self.gamma_converter.display_from_linear(x)
        return y

    def linear_from_display_component(self, x):
        ''' Gamma correct a value (nominal range 0.0 - 1.0)
        to convert from displayable to linear values. '''
        y = self.gamma_converter.linear_from_display(x)
        return y

    def display_from_linear(self, rgb):
        ''' Gamma invert an rgb color (nominal range 0.0 - 1.0)
        to convert from linear to displayable values. '''
        rgb[0] = self.gamma_converter.display_from_linear(rgb[0])
        rgb[1] = self.gamma_converter.display_from_linear(rgb[1])
        rgb[2] = self.gamma_converter.display_from_linear(rgb[2])

    def linear_from_display(self, rgb):
        ''' Gamma correct an rgb color (nominal range 0.0 - 1.0)
        to convert from displayable to linear values. '''
        rgb[0] = self.gamma_converter.linear_from_display(rgb[0])
        rgb[1] = self.gamma_converter.linear_from_display(rgb[1])
        rgb[2] = self.gamma_converter.linear_from_display(rgb[2])

    # Scaling from 0.0 - 1.0 range to integer values 0 - 2^(bitdepth) - 1.

    def scale_int_from_float(self, rgb):
        ''' Scale a color with component range 0.0 - 1.0 to integer values
        in range 0 - 2^(bitdepth) - 1. '''
        ir = round (self.max_value * rgb [0])
        ig = round (self.max_value * rgb [1])
        ib = round (self.max_value * rgb [2])
        # Ensure that values are in the valid range.
        # This is redundant if the value was properly clipped, but make sure.
        ir = min (self.max_value, max (0, ir))
        ig = min (self.max_value, max (0, ig))
        ib = min (self.max_value, max (0, ib))
        irgb = irgb_color (ir, ig, ib)
        return irgb

    def scale_float_from_int(self, irgb):
        ''' Scale a color with integer components 0 - 2^(bitdepth) - 1
        to floating point values in range 0.0 - 1.0. '''
        # Scale to 0.0 - 1.0.
        r = float (irgb [0]) / self.max_value
        g = float (irgb [1]) / self.max_value
        b = float (irgb [2]) / self.max_value
        rgb = rgb_color (r, g, b)
        return rgb

    def clip_rgb_color(self, rgb_color):
        '''Convert a linear rgb color (nominal range 0.0 - 1.0), into a displayable
        irgb color with values in the range (0 - 255), clipping as necessary.

        The return value is a tuple, the first element is the clipped irgb color,
        and the second element is a tuple indicating which (if any) clipping processes were used.
        '''
        clipped_chromaticity = False
        clipped_intensity = False

        rgb = rgb_color.copy()

        # clip chromaticity if needed (negative rgb values)
        if self.clip_method == CLIP_CLAMP_TO_ZERO:
            clipped_chromaticity = self.clip_color_clamp(rgb)
        elif self.clip_method == CLIP_ADD_WHITE:
            clipped_chromaticity = self.clip_color_whiten(rgb)
        else:
            raise ValueError('Invalid color clipping method %s' % (str(self.clip_method)))

        # clip intensity if needed (rgb values > 1.0) by scaling
        clipped_intensity = self.clip_color_intensity(rgb)

        # gamma correction
        self.display_from_linear(rgb)

        # Scale to 0 - 2^B - 1.
        irgb = self.scale_int_from_float(rgb)
        return (irgb, (clipped_chromaticity, clipped_intensity))

    # Conversions between linear rgb colors (0.0 - 1.0 range) and
    # displayable irgb values (0 - 2^B - 1 range).

    def irgb_from_rgb(self, rgb):
        '''Convert a (linear) rgb value (range 0.0 - 1.0) into a displayable integer irgb value (range 0 - 2^B - 1).'''
        result = self.clip_rgb_color (rgb)
        (irgb, (clipped_chrom,clipped_int)) = result
        return irgb

    def rgb_from_irgb(self, irgb):
        '''Convert a displayable (gamma corrected) irgb value (range 0 - 2^B - 1) into a linear rgb value (range 0.0 - 1.0).'''
        # Scale to 0.0 - 1.0, and gamma correct.
        rgb = self.scale_float_from_int(irgb)
        self.linear_from_display(rgb)
        return rgb

#
# Initialization - Initialize to sRGB at module startup.
#   If a different rgb model is needed, then the startup can be re-done to set the new conditions.
#

color_converter = None

def init (
    phosphor_red       = SRGB_Red,
    phosphor_green     = SRGB_Green,
    phosphor_blue      = SRGB_Blue,
    white_point        = SRGB_White,
    gamma_method       = GAMMA_CORRECT_SRGB,
    gamma_value        = None,
    gamma_correct_func = None,
    gamma_invert_func  = None,
    clip_method        = CLIP_ADD_WHITE,
    bit_depth          = 8,
    verbose            = False):
    ''' Initialize. '''
    global color_converter
    color_converter = ColorConverter(
        phosphor_red       = phosphor_red,
        phosphor_green     = phosphor_green,
        phosphor_blue      = phosphor_blue,
        white_point        = white_point,
        gamma_method       = gamma_method,
        gamma_value        = gamma_value,
        gamma_correct_func = gamma_correct_func,
        gamma_invert_func  = gamma_invert_func,
        clip_method        = clip_method,
        bit_depth          = bit_depth)
    if verbose:
        color_converter.dump()


init()
# Default conversions setup on module load
