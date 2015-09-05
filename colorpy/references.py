'''
references.py - Various references to color model data in the literature.

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

from colortypes import xyz_color

#
# Various reference data that is (mostly) not used elsewhere.
#

#
# Definitions of some standard values for colors and conversions
#

# Chromaticities of various standard phosphors and white points.

# sRGB (ITU-R BT.709) standard phosphor chromaticities
SRGB_Red   = xyz_color (0.640, 0.330)
SRGB_Green = xyz_color (0.300, 0.600)
SRGB_Blue  = xyz_color (0.150, 0.060)
SRGB_White = xyz_color (0.3127, 0.3290)  # D65

# HDTV standard phosphors, from Poynton [Color FAQ] p. 9
#   These are claimed to be similar to typical computer monitors
HDTV_Red   = xyz_color (0.640, 0.330)
HDTV_Green = xyz_color (0.300, 0.600)
HDTV_Blue  = xyz_color (0.150, 0.060)
# use D65 as white point for HDTV

# SMPTE phosphors
#   However, Hall [p. 188] notes that TV expects values calibrated for NTSC
#   even though actual phosphors are as below.
# From Hall p. 118, and Kasson p. 400
SMPTE_Red   = xyz_color (0.630, 0.340)
SMPTE_Green = xyz_color (0.310, 0.595)
SMPTE_Blue  = xyz_color (0.155, 0.070)
# use D65 as white point for SMPTE

# NTSC phosphors [original standard for TV, but no longer used in TV sets]
# From Hall p. 119 and Foley/Van Dam p. 589
NTSC_Red   = xyz_color (0.670, 0.330)
NTSC_Green = xyz_color (0.210, 0.710)
NTSC_Blue  = xyz_color (0.140, 0.080)
# use D65 as white point for NTSC

# Typical short persistence phosphors from Foley/Van Dam p. 583
FoleyShort_Red   = xyz_color (0.61, 0.35)
FoleyShort_Green = xyz_color (0.29, 0.59)
FoleyShort_Blue  = xyz_color (0.15, 0.063)

# Typical long persistence phosphors from Foley/Van Dam p. 583
FoleyLong_Red   = xyz_color (0.62, 0.33)
FoleyLong_Green = xyz_color (0.21, 0.685)
FoleyLong_Blue  = xyz_color (0.15, 0.063)

# Typical TV phosphors from Judd/Wyszecki p. 239
Judd_Red   = xyz_color (0.68, 0.32)       # Europium Yttrium Vanadate
Judd_Green = xyz_color (0.28, 0.60)       # Zinc Cadmium Sulfide
Judd_Blue  = xyz_color (0.15, 0.07)       # Zinc Sulfide

# White points [all are for CIE 1931 for small field of view]
#   These are from Judd/Wyszecki
WhiteA   = xyz_color (0.4476, 0.4074)      # approx 2856 K
WhiteB   = xyz_color (0.3484, 0.3516)      # approx 4874 K
WhiteC   = xyz_color (0.3101, 0.3162)      # approx 6774 K
WhiteD55 = xyz_color (0.3324, 0.3475)      # approx 5500 K
WhiteD65 = xyz_color (0.3127, 0.3290)      # approx 6500 K
WhiteD75 = xyz_color (0.2990, 0.3150)      # approx 7500 K

# Blackbody white points [this empirically gave good results]
Blackbody6500K = xyz_color (0.3135, 0.3237)
Blackbody6600K = xyz_color (0.3121, 0.3223)
Blackbody6700K = xyz_color (0.3107, 0.3209)
Blackbody6800K = xyz_color (0.3092, 0.3194)
Blackbody6900K = xyz_color (0.3078, 0.3180)
Blackbody7000K = xyz_color (0.3064, 0.3166)

# MacBeth Color Checker white patch
#   Using this as white point will force MacBeth chart entry to equal machine RGB
MacBethWhite = xyz_color (0.30995, 0.31596, 0.37409)

# Also see Judd/Wyszecki p.164 for colors of Planck Blackbodies

#
# Some standard xyz/rgb conversion matricies, which assume particular phosphors.
# These are useful for testing.
#

# sRGB, from http://www.color.org/sRGB.xalter
srgb_rgb_from_xyz_matrix = numpy.array ([
    [ 3.2410, -1.5374, -0.4986],
    [-0.9692,  1.8760,  0.0416],
    [ 0.0556, -0.2040,  1.0570]
])

# SMPTE conversions, from Kasson p. 400
smpte_xyz_from_rgb_matrix = numpy.array ([
    [0.3935, 0.3653, 0.1916],
    [0.2124, 0.7011, 0.0865],
    [0.0187, 0.1119, 0.9582]
])
smpte_rgb_from_xyz_matrix = numpy.array ([
    [ 3.5064, -1.7400, -0.5441],
    [-1.0690,  1.9777,  0.0352],
    [ 0.0563, -0.1970,  1.0501]
])

'''
Setup the conversions between CIE XYZ and linear RGB spaces.
The conversion is defined by supplying the chromaticities of each of
the monitor phosphors, as well as the resulting white color when all
of the phosphors are at full strength.
See [Foley/Van Dam, p.587, eqn 13.27, 13.29] and [Hall, p. 239].

References:

Foley, van Dam, Feiner and Hughes. Computer Graphics: Principles and Practice, 2nd edition,
    Addison Wesley Systems Programming Series, 1990. ISBN 0-201-12110-7.

Roy Hall, Illumination and Color in Computer Generated Imagery. Monographs in Visual Communication,
    Springer-Verlag, New York, 1989. ISBN 0-387-96774-5.

Wyszecki and Stiles, Color Science: Concepts and Methods, Quantitative Data and Formulae, 2nd edition,
    John Wiley, 1982. Wiley Classics Library Edition 2000. ISBN 0-471-39918-3.

Judd and Wyszecki, Color in Business, Science and Industry, 1975.

Kasson and Plouffe, An Analysis of Selected Computer Interchange Color Spaces,
    ACM Transactions on Graphics, Vol. 11, No. 4, October 1992.

Charles Poynton - Frequently asked questions about Gamma and Color,
    posted to comp.graphics.algorithms, 25 Jan 1995.

sRGB - http://www.color.org/sRGB.xalter - (accessed 15 Sep 2008)
    A Standard Default Color Space for the Internet: sRGB,
    Michael Stokes (Hewlett-Packard), Matthew Anderson (Microsoft), Srinivasan Chandrasekar (Microsoft),
    Ricardo Motta (Hewlett-Packard), Version 1.10, November 5, 1996.
'''
