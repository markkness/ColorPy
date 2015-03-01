'''
rayleigh.py - Rayleigh scattering

Description:

Calculation of the scattering by very small particles (compared to the wavelength).
Also known as Rayleigh scattering.
The scattering intensity is proportional to 1/wavelength^4.
It is scaled so that the scattering factor for 555.0 nm is 1.0.
This is the basic physical reason that the sky is blue.

Functions:

rayleigh_scattering (wl_nm) -
    Get the Rayleigh scattering factor for the wavelength.
    Scattering is proportional to 1/wavelength^4.
    The scattering is scaled so that the factor for wl_nm = 555.0 is 1.0.

rayleigh_scattering_spectrum () -
    Get the Rayleigh scattering spectrum (independent of illuminant), as a numpy array.

rayleigh_illuminated_spectrum (illuminant) -
    Get the spectrum when illuminated by the specified illuminant.

rayleigh_illuminated_color (illuminant) -
    Get the xyz color when illuminated by the specified illuminant.

Plots:

rayleigh_patch_plot (named_illuminant_list, title, filename) -
    Make a patch plot of the Rayleigh scattering color for each illuminant.

rayleigh_color_vs_illuminant_temperature_plot (T_list, title, filename) -
    Make a plot of the Rayleigh scattered color vs. temperature of blackbody illuminant.

rayleigh_spectrum_plot (illuminant, title, filename) -
    Plot the spectrum of Rayleigh scattering of the specified illuminant.

References:

H.C. van de Hulst, Light Scattering by Small Particles,
Dover Publications, New York, 1981. ISBN 0-486-64228-3.

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
import matplotlib.pyplot as pyplot
import numpy
import time

import colormodels
import ciexyz
import illuminants
import blackbody
import plots

#
# Rayleigh scattering, proportional to 1 / wavelength^4.
#

def rayleigh_scattering (wl_nm):
    '''Get the Rayleigh scattering factor for the wavelength.
    Scattering is proportional to 1/wavelength^4.
    The scattering is arbitrarily scaled so for wl_nm = 555.0 it is 1.0.'''
    wl_0_nm = 555.0
    wl_rel  = wl_nm / wl_0_nm
    rayleigh_factor = math.pow (wl_rel, -4)
    return rayleigh_factor


def get_rayleigh_scattering_spectrum (model_spectrum=None):
    ''' Get the Rayleigh scattering Spectrum. '''
    spectrum = ciexyz.Spectrum (model_spectrum)
    for i in range (spectrum.num_wl):
        spectrum.intensity[i] = rayleigh_scattering (spectrum.wavelength[i])
    return spectrum


def get_rayleigh_illuminated_spectrum (illuminant):
    '''Get the spectrum when illuminated by the specified illuminant.'''
    spectrum = get_rayleigh_scattering_spectrum (model_spectrum=illuminant)
    spectrum.intensity *= illuminant.intensity
    return spectrum


def get_rayleigh_illuminated_color (illuminant):
    '''Get the xyz color when illuminated by the specified illuminant.'''
    spectrum = get_rayleigh_illuminated_spectrum (illuminant)
    xyz = spectrum.get_xyz()
    return xyz

#
# Figures
#

def rayleigh_patch_plot (named_illuminants, title, filename):
    ''' Make a patch plot of the Rayleigh scattering color for each illuminant. '''
    xyz_colors = []
    color_names = []
    for illum, name in named_illuminants:
        xyz = get_rayleigh_illuminated_color (illum)
        xyz_colors.append (xyz)
        color_names.append (name)
    plots.xyz_patch_plot (xyz_colors, color_names, title, filename)


def rayleigh_color_vs_illuminant_temperature_plot (T_list, title, filename):
    '''Make a plot of the Rayleigh scattered color vs. temperature of blackbody illuminant.'''
    num_T = len (T_list)
    rgb_list = numpy.empty ((num_T, 3))
    for i in range (num_T):
        T = T_list [i]
        illuminant = illuminants.get_blackbody_illuminant (T)
        xyz = get_rayleigh_illuminated_color (illuminant)
        rgb_list [i] = colormodels.rgb_from_xyz (xyz)
    plots.color_vs_param_plot (
        T_list,
        rgb_list,
        title,
        filename,
        tight = True,
        plotfunc = pyplot.plot,
        xlabel = r'Illuminant Temperature (K)',
        ylabel = r'RGB Color')


def rayleigh_spectrum_plot (illuminant, title, filename):
    '''Plot the spectrum of Rayleigh scattering of the specified illuminant.'''
    spectrum = get_rayleigh_illuminated_spectrum (illuminant)
    plots.spectrum_plot (
        spectrum,
        title,
        filename,
        xlabel = 'Wavelength (nm)',
        ylabel = 'Intensity ($W/m^2$)')

#
# Deprecated usage, using simple arrays instead of Spectrum class.
#

def rayleigh_scattering_spectrum_old ():
    '''Get the Rayleigh scattering spectrum (independent of illuminant), as a numpy array.'''
    spect = get_rayleigh_scattering_spectrum()
    array = spect.to_array()
    return array


def rayleigh_illuminated_spectrum_old (illuminant_array):
    '''Get the spectrum when illuminated by the specified illuminant.'''
    illum = ciexyz.Spectrum_from_array (illuminant_array)
    spect = get_rayleigh_illuminated_spectrum (illum)
    array = spect.to_array()
    return array


def rayleigh_illuminated_color_old (illuminant_array):
    '''Get the xyz color when illuminated by the specified illuminant.'''
    illum = ciexyz.Spectrum_from_array (illuminant_array)
    xyz = get_rayleigh_illuminated_color (illum)
    return xyz


def rayleigh_patch_plot_old (named_illuminant_list, title, filename):
    '''Make a patch plot of the Rayleigh scattering color for each illuminant.'''
    # Adjust illuminant list then plot.
    illum_list = []
    for illuminant_array, name in named_illuminant_list:
        illum = ciexyz.Spectrum_from_array (illuminant_array)
        illum_list.append ((illum, name))
    rayleigh_patch_plot (illum_list, title, filename)


def rayleigh_spectrum_plot_old (illuminant, title, filename):
    '''Plot the spectrum of Rayleigh scattering of the specified illuminant.'''
    illum = ciexyz.Spectrum_from_array (illuminant)
    rayleigh_spectrum_plot (illum, title, filename)

#
# Main.
#

def figures ():
    '''Draw some plots of Rayleigh scattering.'''
    # Patch plots for some illuminants.
    # Sol.
    rayleigh_patch_plot (
        [(illuminants.get_blackbody_illuminant (blackbody.SUN_TEMPERATURE), 'Sun')],
        'Rayleigh Scattering by the Sun', 'Rayleigh-PatchSun')
    # Neon line spectra.
    rayleigh_patch_plot (
        [(illuminants.get_neon_illuminant (), 'Neon Lamp')],
        'Rayleigh Scattering by Neon', 'Rayleigh-Neon')
    # A set of illuminants.
    rayleigh_patch_plot (
        [(illuminants.get_illuminant_D65 (), 'D65'),
        (illuminants.get_neon_illuminant (), 'Neon Lamp'),
        (illuminants.get_blackbody_illuminant (2000.0), '2000 K'),
        (illuminants.get_blackbody_illuminant (3500.0), '3500 K'),
        (illuminants.get_blackbody_illuminant (blackbody.SUN_TEMPERATURE), 'Sun'),
        (illuminants.get_blackbody_illuminant (12000.0), '12000 K')],
        'Rayleigh Scattering by Various Illuminants', 'Rayleigh-PatchVarious')

    # Scattered color vs blackbody illuminant temperature.
    T_list = numpy.linspace(1200.0, 16000.0, 300)
    rayleigh_color_vs_illuminant_temperature_plot (
        T_list, 'Rayleigh Scattering Sky Colors', 'Rayleigh-SkyColors')

    # Spectra for several illuminants.
    T_list = [2000.0, 3000.0, blackbody.SUN_TEMPERATURE, 6500.0, 11000.0, 15000.0]
    for T in T_list:
        T_label = '%dK' % (round(T))
        rayleigh_spectrum_plot (
            illuminants.get_blackbody_illuminant (T),
            'Rayleigh Scattering\nIlluminant %g K' % (T),
            'Rayleigh-Spectrum-%s' % (T_label))
    rayleigh_spectrum_plot (
        illuminants.get_neon_illuminant(),
        'Rayleigh Scattering Neon',
        'Rayleigh-Spectrum-10-Ne')

    # Old-style.
    rayleigh_patch_plot_old (
        [(illuminants.get_blackbody_illuminant_old (blackbody.SUN_TEMPERATURE), 'Sun')],
        'Rayleigh Scattering by the Sun', 'Rayleigh-PatchSun-Old')
    T = 6500.0
    T_label = '%dK' % (round(T))
    rayleigh_spectrum_plot_old (
        illuminants.get_blackbody_illuminant_old (T),
        'Rayleigh Scattering\nIlluminant %g K' % (T),
        'Rayleigh-Spectrum-%s-Old' % (T_label))


if __name__ == '__main__':
    t0 = time.clock()
    figures()
    t1 = time.clock()
    dt = t1 - t0
    print ('Elapsed time: %.3f sec' % (dt))
