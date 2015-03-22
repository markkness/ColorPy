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
    plotfunc = pyplot.plot,
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
    plotfunc   - optional plot function to use (default matplotlib.pyplot.plot)
    xlabel     - label for x axis
    ylabel     - label for y axis (default 'RGB Color')

This file is part of ColorPy.
'''
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import math
import numpy
import matplotlib.pyplot as pyplot

import colormodels
import ciexyz

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
    pyplot.xlim ((x_min, x_max))


def plot_save (filename):
    ''' Save the current plot to the filename. '''
    if filename is not None:
        print ('Saving plot %s' % str (filename))
        pyplot.savefig (filename)

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
        pyplot.fill (poly_x, poly_y, color)
        if name != None:
            dtext = 0.1
            pyplot.text (x0+dtext, y0+dtext, name, size=8.0)

    # make plot with each color with one patch
    pyplot.clf()
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
    pyplot.axis ('off')
    pyplot.title (title)
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
        pyplot.fill (poly_x, poly_y, color_string, edgecolor=color_string)
    # Plot intensity as curve.
    pyplot.plot (
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
    pyplot.clf ()
    # upper plot - solid patch of color that matches the spectrum color
    pyplot.subplot (2,1,1)
    pyplot.title (title)
    color_string = colormodels.irgb_string_from_rgb (
        colormodels.rgb_from_xyz (spectrum.get_xyz()))
    poly_x = [0.0, 1.0, 1.0, 0.0]
    poly_y = [0.0, 0.0, 1.0, 1.0]
    pyplot.fill (poly_x, poly_y, color_string)
    # draw a solid line around the patch to look nicer
    pyplot.plot (poly_x, poly_y, color='k', linewidth=2.0)
    pyplot.axis ('off')
    # lower plot - spectrum vs wavelength, with colors of the associated spectral lines below
    pyplot.subplot (2,1,2)
    spectrum_subplot (spectrum)
    tighten_x_axis (spectrum.wavelength)
    pyplot.xlabel (xlabel)
    pyplot.ylabel (ylabel)
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
    plotfunc = pyplot.plot,
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
    plotfunc   - optional plot function to use (default matplotlib.pyplot.plot)
    xlabel     - label for x axis
    ylabel     - label for y axis (default 'RGB Color')
    '''
    pyplot.clf ()
    # draw color bars in upper plot
    pyplot.subplot (2,1,1)
    pyplot.title (title)
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
        pyplot.fill (poly_x, poly_y, color_string, edgecolor=color_string)
    if tight:
        tighten_x_axis (param_list)
    # draw rgb curves in lower plot
    pyplot.subplot (2,1,2)
    # no title in lower plot
    plotfunc (param_list, rgb_colors [:,0], color='r', label='Red')
    plotfunc (param_list, rgb_colors [:,1], color='g', label='Green')
    plotfunc (param_list, rgb_colors [:,2], color='b', label='Blue')
    if tight:
        tighten_x_axis (param_list)
    pyplot.xlabel (xlabel)
    pyplot.ylabel (ylabel)
    # Save.
    plot_save (filename)
