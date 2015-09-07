'''
clipping.py - Clipping undisplayable colors, and integer/string conversions.

Constants:

CLIP_CLAMP_TO_ZERO = 0
CLIP_ADD_WHITE     = 1
    Available color clipping methods.  Add white is the default.

Functions:

Conversion functions:

irgb_string_from_irgb (irgb) -
    Convert a displayable irgb color (0-255) into a hex string.

irgb_from_irgb_string (irgb_string) -
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
# Color clipping - Physical color values may exceed the what the display can show,
#   either because the color is too pure (indicated by negative rgb values), or
#   because the color is too bright (indicated by rgb values > 1.0).
#   These must be clipped to something displayable.
#

# possible color clipping methods
CLIP_CLAMP_TO_ZERO = 0
CLIP_ADD_WHITE     = 1


def check_clip_method(clip_method):
    ''' Check that the clip method is legal, or raise an exception. '''
    if not clip_method in [CLIP_CLAMP_TO_ZERO, CLIP_ADD_WHITE]:
        raise ValueError('Invalid color clipping method %s' % (str(clip_method)))

#
# Clipping of undisplayable colors.
#

# Color clipping: clipping of negative rgb values.
# These should remove all negative values.

def clip_color_clamp(rgb):
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

def clip_color_whiten(rgb):
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

def clip_color(rgb, clip_method):
    ''' Select the method and color clip. '''
    # clip chromaticity if needed (negative rgb values)
    if clip_method == CLIP_CLAMP_TO_ZERO:
        clipped_chromaticity = clip_color_clamp(rgb)
    elif clip_method == CLIP_ADD_WHITE:
        clipped_chromaticity = clip_color_whiten(rgb)
    else:
        raise ValueError('Invalid color clipping method %s' % (str(clip_method)))
    return clipped_chromaticity

# Intensity clipping: clipping of too large rgb values.
# These should remove all values significantly larger than 1.0.

def clip_intensity(rgb, max_value):
    ''' Scale an rgb color if needed to the component range 0.0 - 1.0. '''
    # The input color is modified as necessary.
    clipped = False
    rgb_max = max (rgb)
    # Does not actually overflow until 2^B * intensity > (2^B + 0.5).
    intensity_cutoff = 1.0 + (0.5 / max_value)
    if rgb_max > intensity_cutoff:
        scaling = intensity_cutoff / rgb_max
        rgb *= scaling
        clipped = True
    return clipped

#
# Conversions between linear rgb colors (range 0.0 - 1.0, values proportional to light intensity)
# and displayable irgb colors (range 0 - 255, values corresponding to hardware palette values).
#
# Displayable irgb colors can be represented as hex strings, like '#AB05B4'.
#

def irgb_string_from_irgb (irgb):
    '''Convert a displayable irgb color (0-255) into a hex string.'''
    # ensure that values are in the range 0-255
    # FIXME: This is overwriting the input value.
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
    irgb = colortypes.irgb_color (ir, ig, ib)
    return irgb

#
# Scaling from 0.0 - 1.0 range to integer values 0 - 2^(bitdepth) - 1.
#

def scale_int_from_float(rgb, max_value):
    ''' Scale a color with component range 0.0 - 1.0 to integer values
    in range 0 - 2^(bitdepth) - 1. '''
    ir = round (max_value * rgb [0])
    ig = round (max_value * rgb [1])
    ib = round (max_value * rgb [2])
    # Ensure that values are in the valid range.
    # This is redundant if the value was properly clipped, but make sure.
    ir = min (max_value, max (0, ir))
    ig = min (max_value, max (0, ig))
    ib = min (max_value, max (0, ib))
    irgb = colortypes.irgb_color (ir, ig, ib)
    return irgb

def scale_float_from_int(irgb, max_value):
    ''' Scale a color with integer components 0 - 2^(bitdepth) - 1
    to floating point values in range 0.0 - 1.0. '''
    # Scale to 0.0 - 1.0.
    r = float (irgb [0]) / max_value
    g = float (irgb [1]) / max_value
    b = float (irgb [2]) / max_value
    rgb = colortypes.rgb_color (r, g, b)
    return rgb
