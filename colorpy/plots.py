'''
plots.py - Various types of plots.

Description:

Functions to draw various types of plots for light spectra.

Functions:

log_interpolate (y0, y1, num_values) -
    Return a list of values, num_values in size, logarithmically interpolated
    between y0 and y1. The first value will be y0, the last y1.

tighten_x_axis (x_list) -
    Tighten the x axis (only) of the current plot to match the given range of x values.
    The y axis limits are not affected.

General plots:

rgb_patch_plot (
    rgb_colors,
    color_names,
    title,
    filename,
    patch_gap = 0.05,
    num_across = 6) -
    Draw a set of color patches, specified as linear rgb colors.

xyz_patch_plot (
    xyz_colors,
    color_names,
    title,
    filename,
    patch_gap = 0.05,
    num_across = 6) -
    Draw a set of color patches specified as xyz colors.

spectrum_subplot (spectrum) -
    Plot a spectrum, with x-axis the wavelength, and y-axis the intensity.
    The curve is colored at that wavelength by the (approximate) color of a
    pure spectral color at that wavelength, with intensity constant over wavelength.
    (This means that dark looking colors here mean that wavelength is poorly viewed by the eye.
    This is not a complete plotting function, e.g. no file is saved, etc.
    It is assumed that this function is being called by one that handles those things.

spectrum_plot (
    spectrum,
    title,
    filename,
    xlabel = 'Wavelength ($nm$)',
    ylabel = 'Intensity ($W/m^2$)') -

    Plot for a single spectrum -
    In a two part graph, plot:
    top: color of the spectrum, as a large patch.
    low: graph of spectrum intensity vs wavelength (x axis).
    The graph is colored by the (approximated) color of each wavelength.
    Each wavelength has equal physical intensity, so the variation in
    apparent intensity (e.g. 400, 800 nm are very dark, 550 nm is bright),
    is due to perceptual factors in the eye.  This helps show how much
    each wavelength contributes to the percieved color.

    spectrum - spectrum to plot
    title    - title for plot
    filename - filename to save plot to
    xlabel   - label for x axis
    ylabel   - label for y axis

color_vs_param_plot (
    param_list,
    rgb_colors,
    title,
    filename,
    tight    = False,
    plotfunc = pylab.plot,
    xlabel   = 'param',
    ylabel   = 'RGB Color') -

    Plot for a color that varies with a parameter -
    In a two part figure, draw:
    top: color as it varies with parameter (x axis)
    low: r,g,b values, as linear 0.0-1.0 values, of the attempted color.

    param_list - list of parameters (x axis)
    rgb_colors - numpy array, one row for each param in param_list
    title      - title for plot
    filename   - filename to save plot to
    plotfunc   - optional plot function to use (default pylab.plot)
    xlabel     - label for x axis
    ylabel     - label for y axis (default 'RGB Color')

Specialized plots:

visible_spectrum_plot () -
    Plot the visible spectrum, as a plot vs wavelength.

cie_matching_functions_plot () -
    Plot the CIE XYZ matching functions, as three spectral subplots.

shark_fin_plot () -
    Draw the 'shark fin' CIE chromaticity diagram of the pure spectral lines (plus purples) in xy space.

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
import pylab

import colormodels
import ciexyz
import pure_colors
import rayleigh

#
# Utilities for plots.
#

def log_interpolate (y0, y1, num_values):
    '''Return a list of values, num_values in size, logarithmically interpolated
    between y0 and y1. The first value will be y0, the last y1.'''
    rtn = []
    if num_values <= 0:
        raise ValueError('Invalid number of divisions %s in log_interpolate' % (str (num_values)))
    if num_values == 1:
        # can't use both endpoints, too constrained
        yi = math.sqrt (y0 * y1)
        rtn.append (yi)
    else:
        # normal case
        beta = math.log (y1 / y0) / float (num_values - 1)
        for i in range (0, num_values):
            yi = y0 * math.exp (beta * float (i))
            rtn.append (yi)
    return rtn


def tighten_x_axis (x_list):
    '''Tighten the x axis (only) of the current plot to match the given range of x values.
    The y axis limits are not affected.'''
    x_min = min (x_list)
    x_max = max (x_list)
    pylab.xlim ((x_min, x_max))


def plot_save (filename):
    ''' Save the current plot to the filename. '''
    if filename is not None:
        print ('Saving plot %s' % str (filename))
        pylab.savefig (filename)

#
# Patch plots - Plots with each color value as a solid patch, with optional labels.
#

def rgb_patch_plot (
    rgb_colors,
    color_names,
    title,
    filename,
    patch_gap = 0.05,
    num_across = 6):
    '''Draw a set of color patches, specified as linear rgb colors.'''

    def draw_patch (x0, y0, color, name, patch_gap):
        '''Draw a patch of color.'''
        # patch relative vertices
        m = patch_gap
        omm = 1.0 - m
        poly_dx = [m, m, omm, omm]
        poly_dy = [m, omm, omm, m]
        # construct vertices
        poly_x = [ x0 + dx_i for dx_i in poly_dx ]
        poly_y = [ y0 + dy_i for dy_i in poly_dy ]
        pylab.fill (poly_x, poly_y, color)
        if name != None:
            dtext = 0.1
            pylab.text (x0+dtext, y0+dtext, name, size=8.0)

    # make plot with each color with one patch
    pylab.clf()
    num_colors = len (rgb_colors)
    for i in range (0, num_colors):
        (iy, ix) = divmod (i, num_across)
        # get color as a displayable string
        colorstring = colormodels.irgb_string_from_rgb (rgb_colors [i])
        if color_names != None:
            name = color_names [i]
        else:
            name = None
        draw_patch (float (ix), float (-iy), colorstring, name, patch_gap)
    pylab.axis ('off')
    pylab.title (title)
    # Save.
    plot_save (filename)


def xyz_patch_plot (
    xyz_colors,
    color_names,
    title,
    filename,
    patch_gap = 0.05,
    num_across = 6):
    '''Draw a set of color patches specified as xyz colors.'''
    rgb_colors = []
    for xyz in xyz_colors:
        rgb = colormodels.rgb_from_xyz (xyz)
        rgb_colors.append (rgb)
    rgb_patch_plot (rgb_colors, color_names, title, filename, patch_gap=patch_gap, num_across=num_across)

#
# Spectrum plots
#

def spectrum_plot_old (
    spectrum_array,
    title,
    filename,
    xlabel = 'Wavelength ($nm$)',
    ylabel = 'Intensity ($W/m^2$)'):
    ''' Plot an old-style spectrum array. '''
    spect = ciexyz.Spectrum_from_array (spectrum_array)
    spectrum_plot (
        spect,
        title,
        filename,
        xlabel=xlabel,
        ylabel=ylabel)


def spectrum_subplot (spectrum):
    '''Plot a spectrum, with x-axis the wavelength, and y-axis the intensity.
    The curve is colored at that wavelength by the (approximate) color of a
    pure spectral color at that wavelength, with intensity constant over wavelength.
    (This means that dark looking colors here mean that wavelength is poorly viewed by the eye.

    This is not a complete plotting function, e.g. no file is saved, etc.
    It is assumed that this function is being called by one that handles those things.'''
    num_wl = spectrum.num_wl
    # Get rgb colors for each wavelength.
    rgb_colors = numpy.empty ((num_wl, 3))
    for i in range (num_wl):
        wl_nm = spectrum.wavelength [i]
        xyz = ciexyz.xyz_from_wavelength (wl_nm)
        rgb_colors [i] = colormodels.rgb_from_xyz (xyz)
    # Scale to make brightest rgb value = 1.0.
    rgb_max = numpy.max (rgb_colors)
    if rgb_max != 0.0:
        scaling = 1.0 / rgb_max
        rgb_colors *= scaling
    # Draw color patches (thin vertical lines matching the spectrum curve).
    # Skip the last for range limitations, it should be zero intensity anyways.
    for i in range (num_wl-1):
        x0 = spectrum.wavelength [i]
        x1 = spectrum.wavelength [i+1]
        y0 = spectrum.intensity [i]
        y1 = spectrum.intensity [i+1]
        poly_x = [x0,  x1,  x1, x0]
        poly_y = [0.0, 0.0, y1, y0]
        color_string = colormodels.irgb_string_from_rgb (rgb_colors [i])
        pylab.fill (poly_x, poly_y, color_string, edgecolor=color_string)
    # Plot intensity as curve.
    pylab.plot (
        spectrum.wavelength, spectrum.intensity,
        color='k', linewidth=2.0, antialiased=True)


def spectrum_plot (
    spectrum,
    title,
    filename,
    xlabel = 'Wavelength ($nm$)',
    ylabel = 'Intensity ($W/m^2$)'):
    '''Plot for a single spectrum -
    In a two part graph, plot:
    top: color of the spectrum, as a large patch.
    low: graph of spectrum intensity vs wavelength (x axis).
    The graph is colored by the (approximated) color of each wavelength.
    Each wavelength has equal physical intensity, so the variation in
    apparent intensity (e.g. 400, 800 nm are very dark, 550 nm is bright),
    is due to perceptual factors in the eye.  This helps show how much
    each wavelength contributes to the percieved color.

    spectrum - spectrum to plot
    title    - title for plot
    filename - filename to save plot to
    xlabel   - label for x axis
    ylabel   - label for y axis
    '''
    pylab.clf ()
    # upper plot - solid patch of color that matches the spectrum color
    pylab.subplot (2,1,1)
    pylab.title (title)
    color_string = colormodels.irgb_string_from_rgb (
        colormodels.rgb_from_xyz (spectrum.get_xyz()))
    poly_x = [0.0, 1.0, 1.0, 0.0]
    poly_y = [0.0, 0.0, 1.0, 1.0]
    pylab.fill (poly_x, poly_y, color_string)
    # draw a solid line around the patch to look nicer
    pylab.plot (poly_x, poly_y, color='k', linewidth=2.0)
    pylab.axis ('off')
    # lower plot - spectrum vs wavelength, with colors of the associated spectral lines below
    pylab.subplot (2,1,2)
    spectrum_subplot (spectrum)
    tighten_x_axis (spectrum.wavelength)
    pylab.xlabel (xlabel)
    pylab.ylabel (ylabel)
    # Save.
    plot_save (filename)

#
# Color vs param plot.
#

def color_vs_param_plot (
    param_list,
    rgb_colors,
    title,
    filename,
    tight    = False,
    plotfunc = pylab.plot,
    xlabel   = 'param',
    ylabel   = 'RGB Color'):
    '''Plot for a color that varies with a parameter -
    In a two part figure, draw:
    top: color as it varies with parameter (x axis)
    low: r,g,b values, as linear 0.0-1.0 values, of the attempted color.

    param_list - list of parameters (x axis)
    rgb_colors - numpy array, one row for each param in param_list
    title      - title for plot
    filename   - filename to save plot to
    plotfunc   - optional plot function to use (default pylab.plot)
    xlabel     - label for x axis
    ylabel     - label for y axis (default 'RGB Color')
    '''
    pylab.clf ()
    # draw color bars in upper plot
    pylab.subplot (2,1,1)
    pylab.title (title)
    # no xlabel, ylabel in upper plot
    num_points = len (param_list)
    for i in range (0, num_points-1):
        x0 = param_list [i]
        x1 = param_list [i+1]
        y0 = 0.0
        y1 = 1.0
        poly_x = [x0, x1, x1, x0]
        poly_y = [y0, y0, y1, y1]
        color_string = colormodels.irgb_string_from_rgb (rgb_colors [i])
        pylab.fill (poly_x, poly_y, color_string, edgecolor=color_string)
    if tight:
        tighten_x_axis (param_list)
    # draw rgb curves in lower plot
    pylab.subplot (2,1,2)
    # no title in lower plot
    plotfunc (param_list, rgb_colors [:,0], color='r', label='Red')
    plotfunc (param_list, rgb_colors [:,1], color='g', label='Green')
    plotfunc (param_list, rgb_colors [:,2], color='b', label='Blue')
    if tight:
        tighten_x_axis (param_list)
    pylab.xlabel (xlabel)
    pylab.ylabel (ylabel)
    # Save.
    plot_save (filename)

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
    color_vs_param_plot (
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
    pylab.clf ()
    # X
    pylab.subplot (3,1,1)
    pylab.title ('1931 CIE XYZ Matching Functions')
    pylab.ylabel ('CIE $X$')
    spectrum_subplot (spect_x)
    tighten_x_axis (spect_x.wavelength)
    # Y
    pylab.subplot (3,1,2)
    pylab.ylabel ('CIE $Y$')
    spectrum_subplot (spect_y)
    tighten_x_axis (spect_y.wavelength)
    # Z
    pylab.subplot (3,1,3)
    pylab.xlabel ('Wavelength (nm)')
    pylab.ylabel ('CIE $Z$')
    spectrum_subplot (spect_z)
    tighten_x_axis (spect_z.wavelength)
    # Save.
    filename = 'CIEXYZ_Matching'
    plot_save (filename)


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
    spectrum_plot (spect_x, 'CIE X', 'CIE-X')
    spectrum_plot (spect_y, 'CIE Y', 'CIE-Y')
    spectrum_plot (spect_z, 'CIE Z', 'CIE-Z')


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
    pylab.clf ()
    pylab.title ('Perceptual Brightness of Rayleigh Scattered Light')
    pylab.xlabel ('Wavelength (nm)')
    pylab.ylabel ('CIE $Y$ / $\lambda^4$')
    spectrum_subplot (spect)
    tighten_x_axis (spect.wavelength)
    # Save.
    filename = 'Laser-Scatter'
    plot_save (filename)


def shark_fin_plot ():
    '''Draw the 'shark fin' CIE chromaticity diagram of the pure spectral lines (plus purples) in xy space.'''
    # get array of (approximate) colors for the boundary of the fin
    xyz_list = pure_colors.get_num_pure_colors (
        brightness=1.0, num_spect=2351, num_purple=200)

    # get normalized colors
    xy_list = xyz_list.copy()
    (num_colors, num_cols) = xy_list.shape
    for i in range (0, num_colors):
        colormodels.xyz_normalize (xy_list [i])
    # get phosphor colors and normalize
    red   = colormodels.PhosphorRed
    green = colormodels.PhosphorGreen
    blue  = colormodels.PhosphorBlue
    white = colormodels.PhosphorWhite
    colormodels.xyz_normalize (red)
    colormodels.xyz_normalize (green)
    colormodels.xyz_normalize (blue)
    colormodels.xyz_normalize (white)

    def get_direc_to_white (xyz):
        '''Get unit vector (xy plane) in direction of the white point.'''
        direc = white - xyz
        mag = math.hypot (direc [0], direc [1])
        if mag != 0.0:
            direc /= mag
        return (direc[0], direc[1])

    # plot
    pylab.clf ()

    # draw best attempt at pure spectral colors on inner edge of shark fin
    s = 0.025     # distance in xy plane towards white point
    for i in range (0, len (xy_list)-1):
        x0 = xy_list [i][0]
        y0 = xy_list [i][1]
        x1 = xy_list [i+1][0]
        y1 = xy_list [i+1][1]
        # get unit vectors in direction of white point
        (dir_x0, dir_y0) = get_direc_to_white (xy_list [i])
        (dir_x1, dir_y1) = get_direc_to_white (xy_list [i+1])
        # polygon vertices
        poly_x = [x0, x1, x1 + s*dir_x1, x0 + s*dir_x0]
        poly_y = [y0, y1, y1 + s*dir_y1, y0 + s*dir_y0]
        # draw (using full color, not normalized value)
        color_string = colormodels.irgb_string_from_rgb (
            colormodels.rgb_from_xyz (xyz_list [i]))
        pylab.fill (poly_x, poly_y, color_string, edgecolor=color_string)

    # fill in the monitor gamut with true colors
    def get_brightest_irgb_string (xyz):
        '''Convert the xyz color to rgb, scale to maximum displayable brightness, and convert to a string.'''
        rgb = colormodels.brightest_rgb_from_xyz (xyz)
        color_string = colormodels.irgb_string_from_rgb (rgb)
        return color_string

    def fill_gamut_slice (v0, v1, v2):
        '''Fill in a slice of the monitor gamut with the correct colors.'''
        #num_s, num_t = 10, 10
        #num_s, num_t = 25, 25
        num_s, num_t = 50, 50
        dv10 = v1 - v0
        dv21 = v2 - v1
        for i_s in range (num_s):
            s_a = float (i_s)   / float (num_s)
            s_b = float (i_s+1) / float (num_s)
            for i_t in range (num_t):
                t_a = float (i_t)   / float (num_t)
                t_b = float (i_t+1) / float (num_t)
                # vertex coords
                v_aa = v0 + t_a * (dv10 + s_a * dv21)
                v_ab = v0 + t_b * (dv10 + s_a * dv21)
                v_ba = v0 + t_a * (dv10 + s_b * dv21)
                v_bb = v0 + t_b * (dv10 + s_b * dv21)
                # poly coords
                poly_x = [v_aa [0], v_ba [0], v_bb [0], v_ab [0]]
                poly_y = [v_aa [1], v_ba [1], v_bb [1], v_ab [1]]
                # average color
                avg = 0.25 * (v_aa + v_ab + v_ba + v_bb)
                # convert to rgb and scale to maximum displayable brightness
                color_string = get_brightest_irgb_string (avg)
                pylab.fill (poly_x, poly_y, color_string, edgecolor=color_string)
    fill_gamut_slice (white, blue,  green)
    fill_gamut_slice (white, green, red)
    fill_gamut_slice (white, red,   blue)

    # draw the curve of the xy values of the spectral lines and purples
    pylab.plot (xy_list [:,0], xy_list [:,1], color='#808080', linewidth=3.0)
    # draw monitor gamut and white point
    pylab.plot ([red  [0], green[0]], [red  [1], green[1]], 'o-', color='k')
    pylab.plot ([green[0], blue [0]], [green[1], blue [1]], 'o-', color='k')
    pylab.plot ([blue [0], red  [0]], [blue [1], red  [1]], 'o-', color='k')
    pylab.plot ([white[0], white[0]], [white[1], white[1]], 'o-', color='k')
    # label phosphors
    dx = 0.01
    dy = 0.01
    pylab.text (red   [0] + dx, red   [1], 'Red',   ha='left',   va='center')
    pylab.text (green [0], green [1] + dy, 'Green', ha='center', va='bottom')
    pylab.text (blue  [0] - dx, blue  [1], 'Blue',  ha='right',  va='center')
    pylab.text (white [0], white [1] + dy, 'White', ha='center', va='bottom')
    # titles etc
    pylab.axis ([0.0, 0.85, 0.0, 0.85])
    pylab.xlabel (r'CIE $x$')
    pylab.ylabel (r'CIE $y$')
    pylab.title (r'CIE Chromaticity Diagram')
    filename = 'ChromaticityDiagram'
    # Save.
    plot_save (filename)

#
# Main.
#

def figures ():
    '''Draw specific figures not used anywhere else.'''
    visible_spectrum_plot()
    cie_matching_functions_plot()
    cie_matching_functions_spectrum_plot()
    shark_fin_plot()
    scattered_visual_brightness()


if __name__ == '__main__':
    figures()
