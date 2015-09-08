'''
clipping.py - Clipping undisplayable colors, and integer/string conversions.

Constants:

CLIP_CLAMP_TO_ZERO = 0
CLIP_ADD_WHITE     = 1
    Available color clipping methods.  Add white is the default.

Functions:

Conversion functions:

hexstring_from_irgb (irgb) -
    Convert a displayable irgb color (0-255) into a hex string.

irgb_from_hexstring (hexstring) -
    Convert a color hex string (like '#AB13D2') into a displayable irgb color.

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

import colortypes

#
# Color clipping:
#
# Calculated rgb color values can be out of the range of what the display can show.
#
# There can be negative rgb components, which mean that color is too saturated,
# and the monitor primary colors cannot match it.
# There can also be rgb components that are too large, which means that the
# color is brighter than what the monitor is capable of.
#
# In both of these cases, the rgb components must be limited to the normal
# range of 0.0 to 1.0 to be physically displayable.
#
# There are two options available for the first case.
# Either negative rgb components can be simply clamped to 0.0,
# or white can be added until there are no negative components.
#
# The second usually looks better, but improved methods are possible!
#

# Available color clipping methods.
CLIP_CLAMP_TO_ZERO = 0
CLIP_ADD_WHITE     = 1


def check_clip_method(clip_method):
    ''' Check that the clip method is legal, or raise an exception. '''
    if not clip_method in [CLIP_CLAMP_TO_ZERO, CLIP_ADD_WHITE]:
        raise ValueError('Invalid color clipping method %s' % (str(clip_method)))

# Color clipping: clipping of negative rgb values.
# These should remove all negative values.
# These modify the passed in colors, and return information about the clipping done.

def clip_color_clamp(rgb):
    ''' Clip an rgb color to remove negative components.
    Any negative components are zeroed. '''
    # The input rgb color is modified.
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

def clip_color_whiten(rgb):
    ''' Clip an rgb color to remove negative components.
    White is added as necessary to remove any negative components. '''
    # The input rgb color is modified.
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

def clip_color(rgb, clip_method=CLIP_ADD_WHITE):
    ''' Clip chromaticity (negative rgb values). '''
    # The input rgb color is modified.
    if clip_method == CLIP_CLAMP_TO_ZERO:
        clipped_chromaticity = clip_color_clamp(rgb)
    elif clip_method == CLIP_ADD_WHITE:
        clipped_chromaticity = clip_color_whiten(rgb)
    else:
        raise ValueError('Invalid color clipping method %s' % (str(clip_method)))
    return clipped_chromaticity

# Intensity clipping: clipping of too large rgb values.
# These should remove all values significantly larger than 1.0.
# These modify the passed in colors, and return information about the clipping done.
# This should be done after color clipping, as that might affect the intensity.

def clip_intensity(rgb, max_value):
    ''' Clip intensity (rgb values significantly > 1.0). '''
    # The input rgb color is modified.
    clipped = False
    rgb_max = max (rgb)
    # Does not actually overflow for a little bit,
    # because until then the rounded value does not exceed max_value.
    intensity_cutoff = 1.0 + (0.5 / max_value)
    if rgb_max > intensity_cutoff:
        scaling = intensity_cutoff / rgb_max
        rgb *= scaling
        clipped = True
    return clipped

#
# Conversions between integer displayable colors and hexstrings, like '#AB05B4'.
#

def hexstring_from_irgb (irgb, num_digits=2):
    ''' Convert a displayable irgb color into a hex string.
    Use the specified number of hex digits per color component. '''
    # Determine max value for the number of digits, and clamp values.
    num_values = 1
    for i in range(num_digits):
        num_values *= 0x10
    min_value = 0
    max_value = num_values - 1
    ir = min(max_value, max(min_value, irgb [0]))
    ig = min(max_value, max(min_value, irgb [1]))
    ib = min(max_value, max(min_value, irgb [2]))
    # Convert to hexstring.
    format1 = '%0' + '%d' % (num_digits) + 'X'
    format2 = '#' + format1 + format1 + format1
    hexstring = format2 % (ir, ig, ib)
    return hexstring

def irgb_from_hexstring (hexstring):
    ''' Convert a hexstring (like '#AB13D2') into a displayable irgb color. '''
    # Check leading '#'.
    if hexstring [0] != '#':
        raise ValueError('hexstring_from_irgb(): Expect hex digit string like #AB13D2')
    # Check number of digits.
    num_all_digits = len(hexstring) - 1
    num_digits, remainder = divmod(num_all_digits, 3)
    if remainder != 0:
        raise ValueError('hexstring_from_irgb(): Expect number of hex digits is multiple of 3')
    # Extract digits.
    irs = hexstring [1               :1 +   num_digits]
    igs = hexstring [1 +   num_digits:1 + 2*num_digits]
    ibs = hexstring [1 + 2*num_digits:1 + 3*num_digits]
    # Parse as hexadecimal integers.
    ir = int (irs, 0x10)
    ig = int (igs, 0x10)
    ib = int (ibs, 0x10)
    irgb = colortypes.irgb_color (ir, ig, ib)
    return irgb

#
# Scaling between 0.0 to 1.0 range and integer 0 to max_value range.
#

def scale_int_from_float(rgb, max_value):
    ''' Scale a color with nominal range 0.0 to 1.0 to integer values in range 0 to max_value. '''
    ir = round (max_value * rgb [0])
    ig = round (max_value * rgb [1])
    ib = round (max_value * rgb [2])
    # Clamp values to range.
    ir = min (max_value, max (0, ir))
    ig = min (max_value, max (0, ig))
    ib = min (max_value, max (0, ib))
    irgb = colortypes.irgb_color (ir, ig, ib)
    return irgb

def scale_float_from_int(irgb, max_value):
    ''' Scale a color with integer values in range 0 to max_value to range 0.0 to 1.0. '''
    r = float (irgb [0]) / max_value
    g = float (irgb [1]) / max_value
    b = float (irgb [2]) / max_value
    rgb = colortypes.rgb_color (r, g, b)
    return rgb
