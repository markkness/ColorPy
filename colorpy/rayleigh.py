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
import numpy
import pylab
import time

import colormodels
import ciexyz
import illuminants
import blackbody
import plots

def rayleigh_scattering (wl_nm):
    '''Get the Rayleigh scattering factor for the wavelength.
    Scattering is proportional to 1/wavelength^4.
    The scattering is scaled so that the factor for wl_nm = 555.0 is 1.0.'''
    wl_0_nm = 555.0
    wl_rel  = wl_nm / wl_0_nm
    rayleigh_factor = math.pow (wl_rel, -4)
    return rayleigh_factor

def rayleigh_scattering_spectrum_old ():
    '''Get the Rayleigh scattering spectrum (independent of illuminant), as a numpy array.'''
    spectrum = ciexyz.empty_spectrum()
    num_wl = spectrum.shape[0]
    for i in range (0, num_wl):
        spectrum [i][1] = rayleigh_scattering (spectrum [i][0])
    return spectrum

def get_rayleigh_scattering_spectrum ():
    ''' Get the Rayleigh scattering Spectrum. '''
    spectrum = ciexyz.Spectrum()
    for i in range (spectrum.num_wl):
        spectrum.intensity[i] = rayleigh_scattering (spectrum.wavelength[i])
    return spectrum

def rayleigh_illuminated_spectrum_old (illuminant):
    '''Get the spectrum when illuminated by the specified illuminant.'''
    spectrum = rayleigh_scattering_spectrum_old()
    num_wl = spectrum.shape[0]
    for i in range (0, num_wl):
        spectrum [i][1] *= illuminant [i][1]
    return spectrum

def get_rayleigh_illuminated_spectrum (illuminant):
    '''Get the spectrum when illuminated by the specified illuminant.'''
    # FIXME: This one should not assume standard wls???
    rayleigh = get_rayleigh_scattering_spectrum()
    spectrum = ciexyz.Spectrum()
    spectrum.intensity[:] = illuminant.intensity
    spectrum.intensity[:] *= rayleigh.intensity
    return spectrum

def rayleigh_illuminated_color_old (illuminant):
    '''Get the xyz color when illuminated by the specified illuminant.'''
    spectrum = rayleigh_illuminated_spectrum_old (illuminant)
    xyz = ciexyz.xyz_from_spectrum (spectrum)
    return xyz

def get_rayleigh_illuminated_color (illuminant):
    '''Get the xyz color when illuminated by the specified illuminant.'''
    spectrum = get_rayleigh_illuminated_spectrum (illuminant)
    xyz = spectrum.get_xyz()
    return xyz

#
# Figures
#

def rayleigh_patch_plot_old (named_illuminant_list, title, filename):
    '''Make a patch plot of the Rayleigh scattering color for each illuminant.'''
    xyz_colors = []
    color_names = []
    for (illuminant, name) in named_illuminant_list:
        xyz = rayleigh_illuminated_color_old (illuminant)
        xyz_colors.append (xyz)
        color_names.append (name)
    plots.xyz_patch_plot (xyz_colors, color_names, title, filename)

def rayleigh_patch_plot_new (named_illuminant_list, title, filename):
    ''' Make a patch plot of the Rayleigh scattering color for each illuminant. '''
    xyz_colors = []
    color_names = []
    for (illuminant, name) in named_illuminant_list:
        xyz = get_rayleigh_illuminated_color (illuminant)
        xyz_colors.append (xyz)
        color_names.append (name)
    plots.xyz_patch_plot (xyz_colors, color_names, title, filename)

def rayleigh_color_vs_illuminant_temperature_plot (T_list, title, filename):
    '''Make a plot of the Rayleigh scattered color vs. temperature of blackbody illuminant.'''
    num_T = len (T_list)
    rgb_list = numpy.empty ((num_T, 3))
    for i in range (0, num_T):
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
        plotfunc = pylab.plot,
        xlabel = r'Illuminant Temperature (K)',
        ylabel = r'RGB Color')

def rayleigh_spectrum_plot_old (illuminant, title, filename):
    '''Plot the spectrum of Rayleigh scattering of the specified illuminant.'''
    spectrum = rayleigh_illuminated_spectrum_old (illuminant)
    plots.spectrum_plot_old (
        spectrum,
        title,
        filename,
        xlabel = 'Wavelength (nm)',
        ylabel = 'Intensity ($W/m^2$)')

def rayleigh_spectrum_plot_new (illuminant, title, filename):
    '''Plot the spectrum of Rayleigh scattering of the specified illuminant.'''
    spectrum = get_rayleigh_illuminated_spectrum (illuminant)
    plots.spectrum_plot_new (
        spectrum,
        title,
        filename,
        xlabel = 'Wavelength (nm)',
        ylabel = 'Intensity ($W/m^2$)')

def figures ():
    '''Draw some plots of Rayleigh scattering.'''
    # Patch plots for some illuminants.
    rayleigh_patch_plot_new (
        [(illuminants.get_blackbody_illuminant (blackbody.SUN_TEMPERATURE), 'Sun')],
        'Rayleigh Scattering by the Sun', 'Rayleigh-PatchSun')
    rayleigh_patch_plot_new (
        [(illuminants.get_illuminant_D65 (), 'D65'),
        (illuminants.get_blackbody_illuminant (2000.0), '2000 K'),
        (illuminants.get_blackbody_illuminant (3500.0), '3500 K'),
        (illuminants.get_blackbody_illuminant (blackbody.SUN_TEMPERATURE), 'Sun'),
        (illuminants.get_blackbody_illuminant (6500.0), '6500 K'),
        (illuminants.get_blackbody_illuminant (15000.0), '15000 K')],
        'Rayleigh Scattering by Various Illuminants', 'Rayleigh-PatchVarious')
    # Old-style.
    rayleigh_patch_plot_old (
        [(illuminants.get_blackbody_illuminant_old (blackbody.SUN_TEMPERATURE), 'Sun')],
        'Rayleigh Scattering by the Sun', 'Rayleigh-PatchSun-Old')

    # Scattered color vs blackbody illuminant temperature.
    T_list = numpy.linspace(1200.0, 16000.0, 300)
    rayleigh_color_vs_illuminant_temperature_plot (
        T_list, 'Rayleigh Scattering Sky Colors', 'Rayleigh-SkyColors')

    # Spectra for several illuminants.
    T_list = [2000.0, 3000.0, blackbody.SUN_TEMPERATURE, 6500.0, 11000.0, 15000.0]
    for T in T_list:
        T_label = '%dK' % (round(T))
        rayleigh_spectrum_plot_new (
            illuminants.get_blackbody_illuminant (T),
            'Rayleigh Scattering\nIlluminant %g K' % (T),
            'Rayleigh-Spectrum-%s' % (T_label))
    # Old-style.
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
