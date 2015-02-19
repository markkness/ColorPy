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

spectral_colors_patch_plot () -
    Colors of the pure spectral lines.

spectral_colors_plus_purples_patch_plot () -
    Colors of the pure spectral lines plus purples.

perceptually_uniform_spectral_colors () -
    Patch plot of (nearly) perceptually equally spaced colors, covering the pure spectral lines plus purples.

spectral_line_555nm_plot () -
    Plot a spectrum that has mostly only a line at 555 nm.
    It is widened a bit only so the plot looks nicer, otherwise the black curve covers up the color.

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
from __future__ import print_function

import math
import numpy

import colormodels
import ciexyz
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

# Patch plots from xyz color values

def MacBeth_ColorChecker_patch_plot ():
    ''' MacBeth ColorChecker Chart. '''
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
        'MacBeth')

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
    # This caused some controversy when the (correct) xyz color was
    # incorrectly reported as light green.
    # The authors also consider several other white points,
    # we just use the default (normally D65).

    # Use the published chromaticity but Y=1.0.
    xyz_colors  = [colormodels.xyz_color_from_xyY (0.345, 0.345, 1.0)]
    color_names = ['The Universe']
    plots.xyz_patch_plot (
        xyz_colors,
        color_names,
        'Average Color of the Universe\nhttp://www.pha.jhu.edu/~kgb/cosspec/',
        'Universe')

# Pure spectral colors

def spectral_colors_patch_plot ():
    '''Colors of the pure spectral lines.'''
    xyzs = ciexyz.get_normalized_spectral_line_colors (brightness=1.0, num_purples=0, dwl_angstroms=10)
    plots.xyz_patch_plot (
        xyzs, None, 'Colors of pure spectral lines', 'Spectral', num_across=20)


def spectral_colors_plus_purples_patch_plot ():
    '''Colors of the pure spectral lines plus purples.'''
    xyzs = ciexyz.get_normalized_spectral_line_colors (brightness=1.0, num_purples=200, dwl_angstroms=10)
    plots.xyz_patch_plot (
        xyzs, None, 'Colors of pure spectral lines plus purples', 'SpectralPlusPurples', num_across=20)

# An attempt to get a perceptually equally spaced (almost) subset of the pure spectral colors

def perceptually_uniform_spectral_colors (
    brightness = 1.0,
    plot_name  = 'PerceptuallyEqualColors',
    plot_title = 'Perceptually (almost) Equally Spaced Pure Colors',
    table_name = 'percep_equal_names.txt'):
    '''Patch plot of (nearly) perceptually equally spaced colors, covering the pure spectral lines plus purples.'''
    # TODO - This may or may not be quite right...
    # get pure colors
#    xyzs = ciexyz.get_normalized_spectral_line_colors (brightness=1.0, num_purples=200, dwl_angstroms=1)
    (xyzs, names) = ciexyz.get_normalized_spectral_line_colors_annotated (brightness=brightness, num_purples=200, dwl_angstroms=1)
    (num_colors, num_columns) = xyzs.shape

    # pick these two functions for either Luv or Lab
    uniform_from_xyz = colormodels.luv_from_xyz
    xyz_from_uniform = colormodels.xyz_from_luv
    #uniform_from_xyz = colormodels.lab_from_xyz
    #xyz_from_uniform = colormodels.xyz_from_lab

    # convert colors to a nearly perceptually uniform space
    uniforms = numpy.empty ((num_colors, 3))
    for i in range (0, num_colors):
        uniforms [i] = uniform_from_xyz (xyzs [i])
    # determine spacing
    sum_ds = 0.0
    dss = numpy.empty ((num_colors, 1))
    for i in range (0, num_colors-1):
        dri = uniforms [i+1] - uniforms [i]
        dsi = math.sqrt (numpy.dot (dri, dri))
        dss [i] = dsi
        sum_ds += dsi
    # last point closes the curve
    dri = uniforms [0] - uniforms [num_colors - 1]
    dsi = math.sqrt (numpy.dot (dri, dri))
    dss [num_colors - 1] = dsi
    sum_ds += dsi
    # pick out subsamples as evenly spaced as possible
    num_samples = 160
    ds_avg = sum_ds / float (num_samples - 1)
    E_indices = []
    index = 0
    count = 0
    need = 0.0
    while True:
        while need > 1.0e-10:
            need -= dss [index]
            index += 1
        E_indices.append (index)
        need += ds_avg
        count += 1
        if count >= num_samples:
            break
    # patch plot and save names
    xyz_list = []
    fil = open (table_name, 'wt')
    fil.write ('%s\n' % plot_title)
    fil.write ('Name iRGB\n')
    fil.write ('\n')
    for index in E_indices:
        uniform_color = uniforms [index]
        uniform_xyz   = xyz_from_uniform (uniform_color)
        uniform_irgb  = colormodels.irgb_from_xyz (uniform_xyz)
        uniform_name  = names [index]
        xyz_list.append (uniform_xyz)
        fil.write ('%s %s\n' % (uniform_name, str (uniform_irgb)))
    fil.close ()
    plots.xyz_patch_plot (
        xyz_list, None, plot_title, plot_name, num_across=20)

def perceptually_uniform_spectral_color_plots ():
    brightness_list = [1.0, 0.9, 0.8, 0.75, 0.6, 0.5, 0.4, 0.3, 0.25]
    for brightness in brightness_list:
        ibright = math.floor (100.0 * brightness + 0.5)
        plot_name  = 'PerceptuallyEqualColors_%d' % ibright
        plot_title = 'Perceptually (almost) Equally Spaced Pure Colors %d%%' % ibright
        table_name = 'percep_equal_names_%d.txt' % ibright
        perceptually_uniform_spectral_colors (brightness, plot_name, plot_title, table_name)

# A sample spectrum that doesn't have equally spaced wavelengths

def spectral_line_555nm_plot ():
    '''Plot a spectrum that has mostly only a line at 555 nm.
    It is widened a bit only so the plot looks nicer, otherwise the black curve covers up the color.'''
    spectrum_list = [
        [360.0, 0.0],
        [549.0, 0.0],
        [552.0, 100.0],
        [553.0, 100.0],
        [554.0, 100.0],
        [555.0, 100.0],
        [556.0, 100.0],
        [557.0, 100.0],
        [558.0, 100.0],
        [557.0, 0.0],
        [830.0, 0.0]]
    spectrum = numpy.array (spectrum_list)
    plots.spectrum_plot_old (spectrum, '555 nm Spectral Line', 'line555nm')

#

def figures ():
    '''Draw the various miscellaneous figures.'''
    # Non-equally spaced wavelengths is a good test. Do it first.
    spectral_line_555nm_plot ()
    # patch plots of lists of color hex strings
    colorstring_patch_plot (matplotlib_colors, matplotlib_names, 'Default MatPlotLib Colormap', 'matplotlib', num_across=7)
    colorstring_patch_plot (hsv_colors, None, 'HSV Colormap', 'hsv')
    colorstring_patch_plot (jet_colors, None, 'Jet Colormap', 'jet')
    colorstring_patch_plot (primary_colors, primary_names, 'Primary Colors', 'primary', num_across=4)
    # patch charts of xyz color tables
    MacBeth_ColorChecker_patch_plot ()
    chemical_solutions_patch_plot ()
    universe_patch_plot ()
    # pure colors
    spectral_colors_patch_plot ()
    spectral_colors_plus_purples_patch_plot ()
    perceptually_uniform_spectral_color_plots ()


if __name__ == '__main__':
    figures()
