'''
misc.py - Miscellaneous color plots.

Description:

Some miscellaneous patch plot utilities, and some samples.

visible_spectrum_plot () -
    Plot the visible spectrum, as a plot vs wavelength.

cie_matching_functions_plot () -
    Plot the CIE XYZ matching functions, as three spectral subplots.

MacBeth_ColorChecker_plot () -
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
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import numpy
import matplotlib.pyplot as pyplot

import ciexyz
import colormodels
import plots
import rayleigh

# FIXME: Rename to examples?

#
# Some specialized figures.
#

def visible_spectrum_plot (filename='VisibleSpectrum'):
    ''' Plot the visible spectrum, as a plot vs wavelength. '''
    spect = ciexyz.Spectrum()
    # Get rgb colors for each wavelength.
    rgb_colors = numpy.empty ((spect.num_wl, 3))
    for i in range (spect.num_wl):
        xyz = ciexyz.xyz_from_wavelength (spect.wavelength [i])
        rgb = colormodels.rgb_from_xyz (xyz)
        rgb_colors [i] = rgb
    # Scale to make brightest rgb value = 1.0.
    rgb_max = numpy.max (rgb_colors)
    if rgb_max != 0.0:
        scaling = 1.0 / rgb_max
        rgb_colors *= scaling
    # plot colors and rgb values vs wavelength
    plots.color_vs_param_plot (
        spect.wavelength,
        rgb_colors,
        'The Visible Spectrum',
        filename,
        tight = True,
        xlabel = r'Wavelength (nm)',
        ylabel = r'RGB Color')


def cie_matching_functions_plot ():
    ''' Plot the CIE XYZ matching functions, as three spectral subplots. '''
    # Get 'spectra' for x,y,z matching functions.
    spect_x = ciexyz.Spectrum()
    spect_y = ciexyz.Spectrum()
    spect_z = ciexyz.Spectrum()
    for i in range (spect_x.num_wl):
        wl_nm = spect_x.wavelength [i]
        xyz = ciexyz.xyz_from_wavelength (wl_nm)
        spect_x.intensity [i] = xyz [0]
        spect_y.intensity [i] = xyz [1]
        spect_z.intensity [i] = xyz [2]
    # Plot three separate subplots, with CIE X in the first,
    # CIE Y in the second, and CIE Z in the third.
    # Label appropriately for the whole plot.
    pyplot.clf ()
    # X
    pyplot.subplot (3,1,1)
    pyplot.title ('1931 CIE XYZ Matching Functions')
    pyplot.ylabel ('CIE $X$')
    plots.spectrum_subplot (spect_x)
    plots.tighten_x_axis (spect_x.wavelength)
    # Y
    pyplot.subplot (3,1,2)
    pyplot.ylabel ('CIE $Y$')
    plots.spectrum_subplot (spect_y)
    plots.tighten_x_axis (spect_y.wavelength)
    # Z
    pyplot.subplot (3,1,3)
    pyplot.xlabel ('Wavelength (nm)')
    pyplot.ylabel ('CIE $Z$')
    plots.spectrum_subplot (spect_z)
    plots.tighten_x_axis (spect_z.wavelength)
    # Save.
    filename = 'CIEXYZ_Matching'
    plots.plot_save (filename)


def cie_matching_functions_spectrum_plot ():
    ''' Plot each of the CIE XYZ matching functions, as spectrum plots. '''
    # Get 'spectra' for x,y,z matching functions.
    spect_x = ciexyz.Spectrum()
    spect_y = ciexyz.Spectrum()
    spect_z = ciexyz.Spectrum()
    for i in range (spect_x.num_wl):
        wl_nm = spect_x.wavelength [i]
        xyz = ciexyz.xyz_from_wavelength (wl_nm)
        spect_x.intensity [i] = xyz [0]
        spect_y.intensity [i] = xyz [1]
        spect_z.intensity [i] = xyz [2]
    # Create three spectrum plots.
    plots.spectrum_plot (spect_x, 'CIE X', 'CIE-X')
    plots.spectrum_plot (spect_y, 'CIE Y', 'CIE-Y')
    plots.spectrum_plot (spect_z, 'CIE Z', 'CIE-Z')


def scattered_visual_brightness ():
    ''' Plot the perceptual brightness of Rayleigh scattered light. '''
    # This combines the extent of scattering with how bright it appears.
    # It shows why a green laser shows a distinct trail in the air,
    # while a red laser does not.
    # Get 'spectra' as CIE Y matching function and multiply by scattering.
    # Rayleigh scattering is proportional to 1 / wl^4.
    spect = ciexyz.Spectrum()
    for i in range (spect.num_wl):
        wl_nm = spect.wavelength [i]
        xyz = ciexyz.xyz_from_wavelength (wl_nm)
        scatter = rayleigh.rayleigh_scattering (wl_nm)
        spect.intensity [i] = xyz[1] * scatter
    # Scale is arbitrary so make max intensity nearly 1.0.
    # It looks a little better if the max is just under 1.
    max_intensity = max (spect.intensity)
    want_max = 0.99
    if max_intensity != 0.0:
        scaling = want_max / max_intensity
        spect.intensity *= scaling
    # Plot.
    pyplot.clf ()
    pyplot.title ('Perceptual Brightness of Rayleigh Scattered Light')
    pyplot.xlabel ('Wavelength (nm)')
    pyplot.ylabel ('CIE $Y$ / $\lambda^4$')
    plots.spectrum_subplot (spect)
    plots.tighten_x_axis (spect.wavelength)
    # Save.
    filename = 'Laser-Scatter'
    plots.plot_save (filename)

#
# Utility functions to make various patch plots, with a name per color.
# The input to these plot functions is a list of tuples, with each tuple
# holding the color values and name.
#

def named_xyz_patch_plot (named_xyz_colors, title, filename, num_across=6):
    ''' Make an patch plot with the specified xyz colors and names. '''
    # Colors specified as x, y, z, name.
    xyzs  = []
    names = []
    for named_xyz_color in named_xyz_colors:
        # Unpack x, y, z, name.
        x, y, z, name = named_xyz_color
        xyz = colormodels.xyz_color(x, y, z)
        xyzs.append (xyz)
        names.append (name)
    plots.xyz_patch_plot (xyzs, names, title, filename, num_across=num_across)


def named_xy1_patch_plot (named_colors, title, filename, num_across=6):
    ''' Make an patch plot with the specified xy (Y=1) colors and names. '''
    # Colors specified as x, y, name, assuming Y=1.
    xyzs  = []
    names = []
    for named_color in named_colors:
        # Unpack x, y, name.
        x, y, name = named_color
        xyz = colormodels.xyz_color_from_xyY (x, y, 1.0)
        xyzs.append (xyz)
        names.append (name)
    plots.xyz_patch_plot (xyzs, names, title, filename, num_across=num_across)


def named_colorstring_patch_plot (named_colors, title, filename, num_across=6):
    ''' Make an patch plot with the specified hexstring colors and names. '''
    # Colors specified as hexstring, name.
    rgbs  = []
    names = []
    for named_color in named_colors:
        # Unpack hexstring, name.
        hexstring, name = named_color
        irgb = colormodels.irgb_from_irgb_string (hexstring)
        rgb  = colormodels.rgb_from_irgb (irgb)
        rgbs.append(rgb)
        names.append(name)
    plots.rgb_patch_plot (rgbs, names, title, filename, num_across=num_across)

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
    named_xyz_patch_plot (patches, 'MacBeth ColorChecker Chart', filename)


def chemical_solutions_patch_plot (filename='ChemSolutions'):
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
    named_xyz_patch_plot (patches,
        'Colors of some chemical solutions\nJ. Chem. Ed., Vol 84, No 11, Nov 2007, p 1873-1877.',
        filename)


def universe_patch_plot (filename='TheUniverse'):
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
    named_xy1_patch_plot (xy_patches,
        'Average Color of the Universe x=0.345, y=0.345\nhttp://www.pha.jhu.edu/~kgb/cosspec/',
        filename)

#
# Some colormaps as hexstrings.
#

def primary_colors_patch_plot (filename='PrimaryColors'):
    ''' Create a sample patch plot of the primary RGB colors. '''
    named_colors = [
        ('#000000', 'Black'),
        ('#FF0000', 'Red'),
        ('#00FF00', 'Green'),
        ('#0000FF', 'Blue'),
        ('#FFFF00', 'Yellow'),
        ('#FF00FF', 'Magenta'),
        ('#00FFFF', 'Cyan'),
        ('#FFFFFF', 'White'),
    ]
    named_colorstring_patch_plot (named_colors,
        'Primary RGB Colors', filename, num_across=4)


def matplotlib_colormaps_patch_plots ():
    ''' Create some sample patch plots of some MatPlotLib colormaps. '''
    # Default colors in Matplotlib.
    matplotlib_colors = [
        ('#0000FF', 'b'),
        ('#008000', 'g'),
        ('#FF0000', 'r'),
        ('#00BFBF', 'c'),
        ('#BF00BF', 'm'),
        ('#BFBF00', 'y'),
        ('#000000', 'k'),
    ]
    named_colorstring_patch_plot (matplotlib_colors,
        'MatPlotLib default colormap', 'Colormap-Matplotlib', num_across=7)
    # Following determined by sampling MATLAB gifs of the colormaps.
    # This is imperfect for several reasons.
    # It should be possible to get the correct values from Matplotlib.
    #
    # Approximate HSV colormap.
    hsv_colors = [
        ('#FF0000', ''),   # red
        ('#FF6300', ''),   # orange
        ('#FFBD00', ''),   # yellow-orange
        ('#DEFF00', ''),   # yellow
        ('#84FF00', ''),   # yellow-green
        ('#21FF00', ''),   # green
        ('#00FF42', ''),   # green
        ('#00FF9C', ''),   # green
        ('#00FFFF', ''),   # cyan
        ('#009CFF', ''),   # light blue
        ('#0042FF', ''),   # blue
        ('#2100FF', ''),   # blue
        ('#8400FF', ''),   # violet
        ('#DE00FF', ''),   # magenta
        ('#FF00BD', ''),   # hot pink
        ('#FF0063', ''),   # red
    ]
    named_colorstring_patch_plot (hsv_colors,
        'MatPlotLib HSV colormap', 'Colormap-Hsv', num_across=8)
    # The jet colormap is associated with an astrophysical fluid jet simulation
    # from the National Center for Supercomputer Applications.
    jet_colors = [
        ('#0000BD', ''),
        ('#0000FF', ''),
        ('#0042FF', ''),
        ('#0084FF', ''),
        ('#00DBFF', ''),
        ('#00FFFF', ''),
        ('#08FFEF', ''),
        ('#42FFBD', ''),
        ('#84FF84', ''),
        ('#BDFF42', ''),
        ('#FFFF00', ''),
        ('#FFBD00', ''),
        ('#FF8400', ''),
        ('#FF4200', ''),
        ('#FF0000', ''),
        ('#BD0000', ''),
        ('#840000', ''),
    ]
    named_colorstring_patch_plot (jet_colors,
        'MatPlotLib Jet colormap', 'Colormap-Jet', num_across=9)

#
# Main.
#

def figures ():
    '''Draw the various example plots.'''
    # Spectrum plots.
    visible_spectrum_plot()
    cie_matching_functions_plot()
    cie_matching_functions_spectrum_plot()
    scattered_visual_brightness()
    # Patch plots.
    MacBeth_ColorChecker_plot()
    chemical_solutions_patch_plot()
    universe_patch_plot()
    primary_colors_patch_plot()
    matplotlib_colormaps_patch_plots()


if __name__ == '__main__':
    figures()
