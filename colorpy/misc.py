'''
misc.py - Miscellaneous color plots.

Description:

Some miscellaneous plots.

colorstring_patch_plot (colorstrings, color_names, title, filename, num_across=6) -
    Color patch plot for colors specified as hex strings.

MacBeth_ColorChecker_patch_plot () -
    MacBeth ColorChecker Chart.
    The xyz values are from Hall p. 119.  I do not know for what lighting conditions this applies.

chemical_solutions_patch_plot () -
    Colors of some chemical solutions.
    Darren L. Williams et. al., 'Beyond lambda-max: Transforming Visible Spectra into 24-bit Color Values'.
        Journal of Chemical Education, Vol 84, No 11, Nov 2007, p1873-1877.
    A student laboratory experiment to measure the transmission spectra of some common chemical solutions,
    and determine the rgb values.

universe_patch_plot () -
    The average color of the universe.
    Karl Glazebrook and Ivan Baldry
        http://www.pha.jhu.edu/~kgb/cosspec/  (accessed 17 Sep 2008)
    The color of the sum of all light in the universe.
    This originally caused some controversy when the (correct) xyz color was incorrectly reported as light green.
    The authors also consider several other white points, here we just use the default (normally D65).

This file is part of ColorPy.
'''
from __future__ import print_function

import colormodels
import plots

# Some sample lists of displayable RGB colors as hex strings

# default colors in Matplotlib
matplotlib_colors = [
    '#0000FF',    # b
    '#008000',    # g
    '#FF0000',    # r
    '#00BFBF',    # c
    '#BF00BF',    # m
    '#BFBF00',    # y
    '#000000'     # k
]

matplotlib_names = [ 'b', 'g', 'r', 'c', 'm', 'y', 'k' ]

# Following determined by sampling rgb values of a MATLAB gif of their colormaps - this is imperfect for several reasons...
hsv_colors = [
    '#FF0000',    # red
    '#FF6300',    # orange
    '#FFBD00',    # yellow-orange
    '#DEFF00',    # yellow
    '#84FF00',    # yellow-green
    '#21FF00',    # green
    '#00FF42',    # green
    '#00FF9C',    # green
    '#00FFFF',    # cyan
    '#009CFF',    # light blue
    '#0042FF',    # blue
    '#2100FF',    # blue
    '#8400FF',    # violet
    '#DE00FF',    # magenta
    '#FF00BD',    # hot pink
    '#FF0063'     # red
]

# Following determined by sampling rgb values of a MATLAB gif of their colormaps - this is imperfect for several reasons...
# The jet colormap is associated with an astrophysical fluid jet simulation from the National Center for Supercomputer Applications.
jet_colors = [
    '#0000BD',  '#0000FF',  '#0042FF',  '#0084FF',
    '#00DBFF',  '#00FFFF',  '#08FFEF',  '#42FFBD',
    '#84FF84',  '#BDFF42',  '#FFFF00',  '#FFBD00',
    '#FF8400',  '#FF4200',  '#FF0000',  '#BD0000',
    '#840000'
]

# some primary colors, convenient for printer ribbon tests and calibration
primary_colors = [
    '#000000',
    '#FF0000',
    '#00FF00',
    '#0000FF',
    '#FFFF00',
    '#FF00FF',
    '#00FFFF',
    '#FFFFFF'
]

# FIXME: Separated color and name is bug-prone.
primary_names = [ 'Black', 'Red', 'Green', 'Blue', 'Yellow', 'Magenta', 'Cyan', 'White' ]

def colorstring_patch_plot (colorstrings, color_names, title, filename, num_across=6):
    '''Color patch plot for colors specified as hex strings.'''
    rgb_colors = []
    for color in colorstrings:
        irgb = colormodels.irgb_from_irgb_string (color)
        rgb = colormodels.rgb_from_irgb (irgb)
        rgb_colors.append (rgb)
    plots.rgb_patch_plot (
        rgb_colors,
        color_names,
        title,
        filename,
        num_across=num_across)

#
# Some example patch plots for xyz color values.
#

def MacBeth_ColorChecker_plot (filename='MacBeth'):
    ''' MacBeth ColorChecker Chart. '''
    # This is a standard test card for photographic use.
    # The xyz values are from Hall p. 119.
    # I do not know for what lighting conditions this applies.
    patches = [
        (0.092, 0.081, 0.058, 'dark skin'),
        (0.411, 0.376, 0.303, 'light skin'),
        (0.183, 0.186, 0.373, 'blue sky'),
        (0.094, 0.117, 0.067, 'foliage'),
        (0.269, 0.244, 0.503, 'blue flower'),
        (0.350, 0.460, 0.531, 'bluish green'),
        (0.386, 0.311, 0.066, 'orange'),
        (0.123, 0.102, 0.359, 'purplish blue'),
        (0.284, 0.192, 0.151, 'moderate red'),
        (0.059, 0.040, 0.102, 'purple'),
        (0.368, 0.474, 0.127, 'yellow green'),
        (0.497, 0.460, 0.094, 'orange yellow'),
        (0.050, 0.035, 0.183, 'blue'),
        (0.149, 0.234, 0.106, 'green'),
        (0.176, 0.102, 0.048, 'red'),
        (0.614, 0.644, 0.112, 'yellow'),
        (0.300, 0.192, 0.332, 'magenta'),
        (0.149, 0.192, 0.421, 'cyan'),
        (0.981, 1.000, 1.184, 'white'),
        (0.632, 0.644, 0.763, 'neutral 8'),
        (0.374, 0.381, 0.451, 'neutral 6.5'),
        (0.189, 0.192, 0.227, 'neutral 5'),
        (0.067, 0.068, 0.080, 'neutral 3.5'),
        (0.000, 0.000, 0.000, 'black'),
    ]
    xyz_colors  = [colormodels.xyz_color (x,y,z) for x,y,z,name in patches]
    color_names = [name for x,y,z,name in patches]

    plots.xyz_patch_plot (
        xyz_colors,
        color_names,
        'MacBeth ColorChecker Chart',
        filename)

def chemical_solutions_patch_plot ():
    ''' Colors of some chemical solutions. '''
    # Darren L. Williams et. al.,
    #   'Beyond lambda-max: Transforming Visible Spectra into 24-bit Color Values'.
    #    Journal of Chemical Education, Vol 84, No 11, Nov 2007, p1873-1877.
    # A student laboratory experiment to measure the transmission spectra of
    # some common chemical solutions, and determine the rgb values.
    patches = [
        (0.360, 0.218, 0.105, '1 M CoCl2'),
        (0.458, 0.691, 0.587, '1 M NiCl2'),
        (0.445, 0.621, 1.052, '1 M CuSO4'),
        (0.742, 0.579, 0.905, '0.005 M KMnO4'),
        (0.949, 1.000, 1.087, 'H2O'),
    ]
    xyz_colors  = [colormodels.xyz_color (x,y,z) for x,y,z,name in patches]
    color_names = [name for x,y,z,name in patches]

    plots.xyz_patch_plot (
        xyz_colors,
        color_names,
        'Colors of some chemical solutions\nJ. Chem. Ed., Vol 84, No 11, Nov 2007, p 1873-1877.',
        'ChemSolutions')

def universe_patch_plot ():
    ''' The average color of the universe. '''
    # Karl Glazebrook and Ivan Baldry
    #     http://www.pha.jhu.edu/~kgb/cosspec/  (accessed 17 Sep 2008)
    # The color of the sum of all light in the universe.
    # The xy chromaticity (with Y=1) is 0.345, 0.345.
    # There was some initial controversy when this xy color was incorrectly
    # reported as light green. The authors also consider other white points.
    # This just uses the default D65.
    xy_patches = [
        (0.345, 0.345, 'The Universe'),
    ]
    xyz_colors  = [colormodels.xyz_color_from_xyY (x, y, 1.0) for x,y,name in xy_patches]
    color_names = [name for x,y,name in xy_patches]

    plots.xyz_patch_plot (
        xyz_colors,
        color_names,
        'Average Color of the Universe x=0.345, y=0.345\nhttp://www.pha.jhu.edu/~kgb/cosspec/',
        'TheUniverse')

#
# Main.
#

def figures ():
    '''Draw the various miscellaneous figures.'''
    # patch plots of lists of color hex strings
    colorstring_patch_plot (matplotlib_colors, matplotlib_names, 'Default MatPlotLib Colormap', 'matplotlib', num_across=7)
    colorstring_patch_plot (hsv_colors, None, 'HSV Colormap', 'hsv', num_across=8)
    colorstring_patch_plot (jet_colors, None, 'Jet Colormap', 'jet', num_across=9)
    colorstring_patch_plot (primary_colors, primary_names, 'Primary Colors', 'primary', num_across=4)
    # Example patch plots of xyz colors.
    MacBeth_ColorChecker_plot()
    chemical_solutions_patch_plot ()
    universe_patch_plot ()


if __name__ == '__main__':
    figures()
