'''
pure_colors.py - Some work-in-progress related to pure colors.

Pure colors mean spectral lines and the 'purples'.

This file is part of ColorPy.
'''
from __future__ import print_function

import math
import numpy

import colormodels
import ciexyz
import plots

#
# Miscellaneous stuff for spectral line colors.
# This is used by the shark fin plot as well as the examples in this file.
#

def scale_rgb_max (xyz_array, brightness):
    ''' Scale each color to have the max rgb value be the desired brightness. '''
    num_points = xyz_array.shape[0]
    for i in range (num_points):
        rgb = colormodels.brightest_rgb_from_xyz (xyz_array [i], brightness)
        xyz_array [i] = colormodels.xyz_from_rgb (rgb)


def get_spectral_colors (wl_array):
    ''' Get the pure spectral line colors. '''
    # wl_array = wavelengths in nm.
    num  = wl_array.shape[0]
    xyzs = numpy.zeros((num, 3))
    for i in range (num):
        wl  = wl_array [i]
        xyz = ciexyz.xyz_from_wavelength (wl)
        colormodels.xyz_normalize (xyz)
        xyzs [i] = xyz
    return xyzs


def get_purple_colors (t_array, violet_xyz, red_xyz):
    ''' Get the pure purple colors by interpolating between violet and red. '''
    # t_array    = interpolation fractions 0.0 to 1.0
    # violet_xyz = xyz color for pure violet
    # red_xyz    = xyz_color for pure red
    num  = t_array.shape[0]
    xyzs = numpy.zeros((num, 3))
    # FIXME: violet and red may be backwards.
    first_xyz = violet_xyz
    last_xyz  = red_xyz
    for i in range (num):
        t   = t_array [i]
        omt = 1.0 - t
        xyz = t * first_xyz + omt * last_xyz
        colormodels.xyz_normalize (xyz)
        xyzs [i] = xyz
    return xyzs


def get_normalized_spectral_line_colors (
    brightness = 1.0,
    num_purples = 0,
    dwl_angstroms = 10):
    '''Get an array of xyz colors covering the visible spectrum.
    Optionally add a number of 'purples', which are colors interpolated between the color
    of the lowest wavelength (violet) and the highest (red).

    brightness - Desired maximum rgb component of each color.  Default 1.0.  (Maxiumum displayable brightness)
    num_purples - Number of colors to interpolate in the 'purple' range.  Default 0.  (No purples)
    dwl_angstroms - Wavelength separation, in angstroms (0.1 nm).  Default 10 A. (1 nm spacing)
    '''
    # Get wavelengths. Delta is so far only 2 A and 10 A.
    ratio     = round (10.0 / float(dwl_angstroms))
    num_spect = ratio * (ciexyz.end_wl_nm - ciexyz.start_wl_nm) + 1
    wl_array  = numpy.linspace (ciexyz.start_wl_nm, ciexyz.end_wl_nm, num=num_spect)

    # Get the spectral line colors.
    xyzs_spect = get_spectral_colors (wl_array)

    # Get the purples.
    violet_xyz  = xyzs_spect [ 0, :]
    red_xyz     = xyzs_spect [-1, :]
    t_array     = numpy.linspace (0.0, 1.0, num=num_purples)
    xyzs_purple = get_purple_colors (t_array, violet_xyz, red_xyz)

    # Join spectral colors and purples.
    xyzs = numpy.vstack ([xyzs_spect, xyzs_purple])

    # Scale.
    scale_rgb_max (xyzs, brightness)
    return xyzs

def get_normalized_spectral_line_colors_annotated (
    brightness = 1.0,
    num_purples = 0,
    dwl_angstroms = 10):
    '''Get an array of xyz colors covering the visible spectrum.
    Optionally add a number of 'purples', which are colors interpolated between the color
    of the lowest wavelength (violet) and the highest (red).
    A text string describing the color is supplied for each color.

    brightness - Desired maximum rgb component of each color.  Default 1.0.  (Maxiumum displayable brightness)
    num_purples - Number of colors to interpolate in the 'purple' range.  Default 0.  (No purples)
    dwl_angstroms - Wavelength separation, in angstroms (0.1 nm).  Default 10 A. (1 nm spacing)
    '''
    # Get wavelengths. Delta is so far only 2 A and 10 A.
    ratio     = round (10.0 / float(dwl_angstroms))
    num_spect = ratio * (ciexyz.end_wl_nm - ciexyz.start_wl_nm) + 1
    wl_array  = numpy.linspace (ciexyz.start_wl_nm, ciexyz.end_wl_nm, num=num_spect)

    # Get the spectral line colors and names.
    xyzs_spect  = get_spectral_colors (wl_array)
    names_spect = []
    for j in range(wl_array.shape[0]):
        name = '%.1f nm' % wl_array[j]
        names_spect.append (name)

    # Get the purples and names.
    violet_xyz   = xyzs_spect [ 0, :]
    red_xyz      = xyzs_spect [-1, :]
    t_array      = numpy.linspace (0.0, 1.0, num=num_purples)
    xyzs_purple  = get_purple_colors (t_array, violet_xyz, red_xyz)
    names_purple = []
    for j in range (num_purples):
        name = '%03d purp' % round (1000.0 * t_array[j])
        names_purple.append (name)

    # Join spectral colors and purples.
    xyzs  = numpy.vstack ([xyzs_spect, xyzs_purple])
    names = names_spect + names_purple

    # Scale.
    scale_rgb_max (xyzs, brightness)
    return (xyzs, names)

#
# Figures.
#

def spectral_colors_patch_plot ():
    '''Colors of the pure spectral lines.'''
    xyzs = get_normalized_spectral_line_colors (brightness=1.0, num_purples=0, dwl_angstroms=10)
    plots.xyz_patch_plot (
        xyzs, None, 'Colors of pure spectral lines', 'Spectral', num_across=20)
    xyzs, names = get_normalized_spectral_line_colors_annotated (brightness=1.0, num_purples=0, dwl_angstroms=10)
    plots.xyz_patch_plot (
        xyzs, None, 'Colors of pure spectral lines-2', 'Spectral-2', num_across=20)


def spectral_colors_plus_purples_patch_plot ():
    '''Colors of the pure spectral lines plus purples.'''
    xyzs = get_normalized_spectral_line_colors (brightness=1.0, num_purples=200, dwl_angstroms=10)
    plots.xyz_patch_plot (
        xyzs, None, 'Colors of pure spectral lines plus purples', 'SpectralPlusPurples', num_across=20)
    xyzs, names = get_normalized_spectral_line_colors_annotated (brightness=1.0, num_purples=200, dwl_angstroms=10)
    plots.xyz_patch_plot (
        xyzs, None, 'Colors of pure spectral lines plus purples-2', 'SpectralPlusPurples-2', num_across=20)

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
    (xyzs, names) = get_normalized_spectral_line_colors_annotated (brightness=brightness, num_purples=200, dwl_angstroms=1)
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

#
# Main.
#

def figures ():
    ''' Draw plots of the pure colors and purples. '''
    # These are all pretty much a work-in-progress.
    if True:
        spectral_colors_patch_plot ()
    if True:
        spectral_colors_plus_purples_patch_plot ()
    if True:
        perceptually_uniform_spectral_color_plots ()


if __name__ == '__main__':
    figures()
