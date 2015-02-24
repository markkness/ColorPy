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
    # get range of wavelengths, in angstroms, so that we can have finer resolution than 1 nm
    wl_angstrom_range = range (10*ciexyz.start_wl_nm, 10*(ciexyz.end_wl_nm + 1), dwl_angstroms)
    # get total point count
    num_spectral = len (wl_angstrom_range)
    num_points   = num_spectral + num_purples
    xyzs = numpy.empty ((num_points, 3))
    # build list of normalized color x,y values proceeding along each wavelength
    i = 0
    for wl_A in wl_angstrom_range:
        wl_nm = wl_A * 0.1
        xyz = ciexyz.xyz_from_wavelength (wl_nm)
        colormodels.xyz_normalize (xyz)
        xyzs [i] = xyz
        i += 1
    # interpolate from end point to start point (filling in the purples)
    first_xyz = xyzs [0]
    last_xyz  = xyzs [num_spectral - 1]
    for ipurple in range (0, num_purples):
        t = float (ipurple) / float (num_purples - 1)
        omt = 1.0 - t
        xyz = t * first_xyz + omt * last_xyz
        colormodels.xyz_normalize (xyz)
        xyzs [i] = xyz
        i += 1
    # scale each color to have the max rgb component equal to the desired brightness
    for i in range (0, num_points):
        rgb = colormodels.brightest_rgb_from_xyz (xyzs [i], brightness)
        xyzs [i] = colormodels.xyz_from_rgb (rgb)
    # done
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
    # get range of wavelengths, in angstroms, so that we can have finer resolution than 1 nm
    wl_angstrom_range = range (10*ciexyz.start_wl_nm, 10*(ciexyz.end_wl_nm + 1), dwl_angstroms)
    # get total point count
    num_spectral = len (wl_angstrom_range)
    num_points   = num_spectral + num_purples
    xyzs = numpy.empty ((num_points, 3))
    names = []
    # build list of normalized color x,y values proceeding along each wavelength
    i = 0
    for wl_A in wl_angstrom_range:
        wl_nm = wl_A * 0.1
        xyz = ciexyz.xyz_from_wavelength (wl_nm)
        colormodels.xyz_normalize (xyz)
        xyzs [i] = xyz
        name = '%.1f nm' % wl_nm
        names.append (name)
        i += 1
    # interpolate from end point to start point (filling in the purples)
    first_xyz = xyzs [0]
    last_xyz  = xyzs [num_spectral - 1]
    for ipurple in range (0, num_purples):
        t = float (ipurple) / float (num_purples - 1)
        omt = 1.0 - t
        xyz = t * first_xyz + omt * last_xyz
        colormodels.xyz_normalize (xyz)
        xyzs [i] = xyz
        name = '%03d purple' % math.floor (1000.0 * t + 0.5)
        names.append (name)
        i += 1
    # scale each color to have the max rgb component equal to the desired brightness
    for i in range (0, num_points):
        rgb = colormodels.brightest_rgb_from_xyz (xyzs [i], brightness)
        xyzs [i] = colormodels.xyz_from_rgb (rgb)
    # done
    return (xyzs, names)

#
# Figures.
#

def spectral_colors_patch_plot ():
    '''Colors of the pure spectral lines.'''
    xyzs = get_normalized_spectral_line_colors (brightness=1.0, num_purples=0, dwl_angstroms=10)
    plots.xyz_patch_plot (
        xyzs, None, 'Colors of pure spectral lines', 'Spectral', num_across=20)


def spectral_colors_plus_purples_patch_plot ():
    '''Colors of the pure spectral lines plus purples.'''
    xyzs = get_normalized_spectral_line_colors (brightness=1.0, num_purples=200, dwl_angstroms=10)
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
    spectral_colors_patch_plot ()
    spectral_colors_plus_purples_patch_plot ()
    perceptually_uniform_spectral_color_plots ()


if __name__ == '__main__':
    figures()
