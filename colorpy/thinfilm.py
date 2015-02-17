'''
thinfilm.py - Thin film interference colors.

Description:

Reflection from a thin film, as a function of wavelength, thickness, and index of refraction of materials.

Note that film thicknesses are given in nm instead of m, as this is a more convenient unit in this case.

We consider incident light from a medium of index of refraction n1,
striking a thin film of index n2, with a third medium of index n3 behind the film.

The total reflection from the film, back towards the incident light, is calculated.

Some sample values of the index of refraction:
    air :          n = 1.003
    water:         n = 1.33
    glass/plastic: n = 1.5
    oil:           n = 1.44 (matches Minnaert's color observations)

Functions:

class thin_film (n1, n2, n3, thickness_nm) -
    Represents a thin film, with the indices of refraction n1,n2,n3 representing:
	n1 - index of refraction of infinite region the light comes from
	n2 - index of refraction of finite region of the film
	n3 - index of refraction of infinite region beyond the film
    and thickness_nm being the thickness of the film [nm].

On these class objects, the following functions are available:

get_interference_reflection_coefficient (wl_nm) -
    Get the reflection coefficient for the intensity for light
    of the given wavelength impinging on the film.

reflection_spectrum () -
    Get the reflection spectrum (independent of illuminant) for the thin film.

illuminated_spectrum (illuminant) -
    Get the spectrum when illuminated by the specified illuminant.

illuminated_color (illuminant) -
    Get the xyz color when illuminated by the specified illuminant.

Plots:

thinfilm_patch_plot (n1, n2, n3, thickness_nm_list, illuminant, title, filename) -
    Make a patch plot of the color of the film for each thickness [nm].

thinfilm_color_vs_thickness_plot (n1, n2, n3, thickness_nm_list, illuminant, title, filename) -
    Plot the color of the thin film for the specfied thicknesses [nm].

thinfilm_spectrum_plot (n1, n2, n3, thickness_nm, illuminant, title, filename) -
    Plot the spectrum of the reflection from a thin film for the given thickness [nm].

References:

Frank S. Crawford, Jr., Waves: Berkeley Physics Course - Volume 3,
McGraw-Hill Book Company, 1968. Library of Congress 64-66016.

M. Minnaert, The nature of light and color in the open air,
translation H.M. Kremer-Priest, Dover Publications, New York, 1954. ISBN 486-20196-1.  p. 208-209.

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
import cmath
import math
import numpy
import time

import colormodels
import ciexyz
import illuminants
import plots

class thin_film:
    '''A thin film of dielectric material.'''
    def __init__ (self, n1, n2, n3, thickness_nm):
        self.n1 = n1
        self.n2 = n2
        self.n3 = n3
        self.thickness_nm = thickness_nm
        self.too_thick = False

        # pre-calculate
        def field_reflection_coefficient (n1, n2):
            ''' Calculate the reflection coefficient for a light wave traveling from
            a region with index of refraction n1 to one having an index of n2.
            This is the coefficient for the electric field, not the intensity.'''
            return ( (n1 - n2) / (n1 + n2) )

        # R12 = field reflection coefficient for light traveling from region 1 to 2
        # R23 = field reflection coefficient for light traveling from region 2 to 3
        self.R12 = field_reflection_coefficient (n1, n2)
        self.R23 = field_reflection_coefficient (n2, n3)
        self.R12sqd_plus_R23sqd = self.R12*self.R12 + self.R23*self.R23
        self.R12_times_R23_times_2 = 2.0 * self.R12 * self.R23
        self.phase_factor = -2.0 * self.thickness_nm * 2.0 * math.pi * n2

        # aliasing will occur if the layer is too thick - see if this is true
        sample_interval_nm = 1.0      # assuming 1 nm
        wavelength_0_nm    = 380.0    # shortest wl results in minimum max_thickness
        max_thickness_nm = 0.25 * math.pow (wavelength_0_nm, 2) / (n2 * sample_interval_nm)
        if self.thickness_nm > max_thickness_nm:
            self.too_thick = True

    def get_interference_reflection_coefficient (self, wl_nm):
        '''Get the reflection coefficient for the intensity for light
        of the given wavelength impinging on the film.'''
        if self.too_thick:
            # would alias -
            # if the layer is too thick, the cos() factor is averaged over multiple periods
            # to zero, this is the best we can do
            return self.R12sqd_plus_R23sqd

        ## small-reflection approximation
        #R = self.R12sqd_plus_R23sqd + self.R12_times_R23_times_2 * math.cos (self.phase_factor / wl_nm)
        #return R

        # exact - accounts for multiple reflections, and does not assume a small
        # reflection coefficient.  Should be correct for complex n1,n2,n3 as well.
        phase = cmath.exp (complex (0, 1.0) * (self.phase_factor / wl_nm))
        num   = self.R12 + self.R23 * phase
        den   = 1.0 + self.R12 * self.R23 * phase
        Re    = num / den
        R     = Re.real*Re.real + Re.imag*Re.imag
        return R

    def get_reflection_spectrum (self):
        '''Get the reflection spectrum (independent of illuminant) for the thin film.'''
        spectrum = ciexyz.Spectrum()
        for i in range (spectrum.num_wl):
            wl_nm = spectrum.wavelength [i]
            spectrum.intensity [i] = self.get_interference_reflection_coefficient (wl_nm)
        return spectrum

    def get_illuminated_spectrum (self, illuminant):
        '''Get the spectrum when illuminated by the specified illuminant.'''
        spectrum = self.get_reflection_spectrum()
        spectrum.intensity *= illuminant.intensity
        return spectrum

    def get_illuminated_color (self, illuminant):
        '''Get the xyz color when illuminated by the specified illuminant.'''
        spectrum = self.get_illuminated_spectrum (illuminant)
        xyz = spectrum.get_xyz()
        return xyz

    # Deprecated - Versions working with arrays not Spectrum classes.

    def reflection_spectrum_old (self):
        '''Get the reflection spectrum (independent of illuminant) for the thin film.'''
        spect = self.get_reflection_spectrum()
        array = spect.to_array()
        return array

    def illuminated_spectrum_old (self, illuminant):
        '''Get the spectrum when illuminated by the specified illuminant.'''
        # FIXME: Spectrum_from_array()???
        illum = ciexyz.Spectrum()
        illum.from_array(illuminant)
        spect = self.get_illuminated_spectrum (illum)
        array = spect.to_array()
        return array

    def illuminated_color_old (self, illuminant):
        '''Get the xyz color when illuminated by the specified illuminant.'''
        # FIXME: Spectrum_from_array()???
        illum = ciexyz.Spectrum()
        illum.from_array(illuminant)
        xyz = self.get_illuminated_color (illum)
        return xyz


def create_thin_films (n1, n2, n3, thickness_list):
    ''' Create a list of thin films from a list of thicknesses. '''
    films = []
    for thickness in thickness_list:
        film = thin_film (n1, n2, n3, thickness)
        films.append(film)
    return films

#
# Figures
#

def thinfilm_patch_plot_old (n1, n2, n3, thickness_nm_list, illuminant, title, filename):
    '''Make a patch plot of the color of the film for each thickness [nm].'''
    films = create_thin_films(n1, n2, n3, thickness_nm_list)
    xyz_colors = []
    labels = []
    for film in films:
        xyz = film.illuminated_color_old (illuminant)
        xyz_colors.append (xyz)
        label = '%.1f nm' % (film.thickness_nm)
        labels.append(label)
    plots.xyz_patch_plot (xyz_colors, labels, title, filename)

def thinfilm_patch_plot_new (n1, n2, n3, thickness_nm_list, illuminant, title, filename):
    '''Make a patch plot of the color of the film for each thickness [nm].'''
    films = create_thin_films(n1, n2, n3, thickness_nm_list)
    xyz_colors = []
    labels = []
    for film in films:
        xyz = film.get_illuminated_color (illuminant)
        xyz_colors.append (xyz)
        label = '%.1f nm' % (film.thickness_nm)
        labels.append(label)
    plots.xyz_patch_plot (xyz_colors, labels, title, filename)

def thinfilm_color_vs_thickness_plot_old (n1, n2, n3, thickness_nm_list, illuminant, title, filename):
    '''Plot the color of the thin film for the specfied thicknesses [nm].'''
    films = create_thin_films(n1, n2, n3, thickness_nm_list)
    num_films = len (films)
    rgb_list = numpy.empty ((num_films, 3))
    for i in range (0, num_films):
        film = films[i]
        xyz = film.illuminated_color_old (illuminant)
        rgb_list [i] = colormodels.rgb_from_xyz (xyz)
    plots.color_vs_param_plot (
        thickness_nm_list,
        rgb_list,
        title,
        filename,
        xlabel = r'Thickness (nm)',
        ylabel = r'RGB Color')

def thinfilm_color_vs_thickness_plot_new (n1, n2, n3, thickness_nm_list, illuminant, title, filename):
    '''Plot the color of the thin film for the specfied thicknesses [nm].'''
    films = create_thin_films(n1, n2, n3, thickness_nm_list)
    num_films = len (films)
    rgb_list = numpy.empty ((num_films, 3))
    for i in range (0, num_films):
        film = films[i]
        xyz = film.get_illuminated_color (illuminant)
        rgb_list [i] = colormodels.rgb_from_xyz (xyz)
    plots.color_vs_param_plot (
        thickness_nm_list,
        rgb_list,
        title,
        filename,
        xlabel = r'Thickness (nm)',
        ylabel = r'RGB Color')

def thinfilm_spectrum_plot_old (n1, n2, n3, thickness_nm, illuminant, title, filename):
    '''Plot the spectrum of the reflection from a thin film for the given thickness [nm].'''
    film = thin_film (n1, n2, n3, thickness_nm)
    illuminated_spectrum = film.illuminated_spectrum_old (illuminant)
    plots.spectrum_plot_old (
        illuminated_spectrum,
        title,
        filename,
        xlabel   = 'Wavelength (nm)',
        ylabel   = 'Refection Intensity')

def thinfilm_spectrum_plot_new (n1, n2, n3, thickness_nm, illuminant, title, filename):
    '''Plot the spectrum of the reflection from a thin film for the given thickness [nm].'''
    film = thin_film (n1, n2, n3, thickness_nm)
    illuminated_spectrum = film.get_illuminated_spectrum (illuminant)
    plots.spectrum_plot_new (
        illuminated_spectrum,
        title,
        filename,
        xlabel   = 'Wavelength (nm)',
        ylabel   = 'Refection Intensity')

def figures ():
    '''Draw some thin film plots.'''
    # Scale the illuminant to get a better range of color.

    # Simple patch plot. This is not all that interesting.
    thickness_nm_list = numpy.linspace(0.0, 750.0, 36)
    illuminant = illuminants.get_illuminant_D65()
    illuminant.scale (9.50)
    thinfilm_patch_plot_new (1.500, 1.003, 1.500, thickness_nm_list,
        illuminant, 'ThinFilm Patch Plot', 'ThinFilm-Patch')

    # Plot the colors of films vs thickness.
    thickness_nm_list = numpy.linspace(0.0, 1000.0, 800)

    # Gap in glass/plastic.
    illuminant = illuminants.get_illuminant_D65()
    illuminant.scale (4.50)
    thinfilm_color_vs_thickness_plot_new (
        1.500, 1.003, 1.500, thickness_nm_list, illuminant,
        'Thin Film - Gap In Glass/Plastic (n = 1.50)\nIlluminant D65',
        'ThinFilm-GlassGap')

    # Soap bubble.
    illuminant = illuminants.get_illuminant_D65()
    illuminant.scale (9.50)
    thinfilm_color_vs_thickness_plot_new (
        1.003, 1.33, 1.003, thickness_nm_list, illuminant,
        'Thin Film - Soap Bubble (n = 1.33)\nIlluminant D65',
        'ThinFilm-SoapBubble')

    # Oil slick on water.
    illuminant = illuminants.get_illuminant_D65()
    illuminant.scale (15.00)
    thinfilm_color_vs_thickness_plot_new (
        1.003, 1.44, 1.33, thickness_nm_list, illuminant,
        'Thin Film - Oil Slick (n = 1.44) on Water (n = 1.33)\nIlluminant D65',
        'ThinFilm-OilSlick')

    # Large index of refraction bubble.
    # This has the brightest colors, but is a bit of an artificial example.
    illuminant = illuminants.get_illuminant_D65()
    illuminant.scale (3.33)
    thinfilm_color_vs_thickness_plot_new (
        1.003, 1.60, 1.003, thickness_nm_list, illuminant,
        'Thin Film - Large Index (n = 1.60) Bubble\nIlluminant D65',
        'ThinFilm-LargeBubble')

    # A very thick film to test the aliasing limits.
    # You have to go to very large thicknesses to get much aliasing.
    thickness_nm_list = numpy.linspace(0.0, 200000.0, 800)
    illuminant = illuminants.get_illuminant_D65()
    illuminant.scale (9.50)
    thinfilm_color_vs_thickness_plot_new (
        1.003, 1.33, 1.003, thickness_nm_list, illuminant,
        'Not-so-thin Film - Soap Bubble (n = 1.33)\nIlluminant D65',
        'ThinFilm-Thick')

    # Plot the spectrum of the refection for a couple of thicknesses.
    # Use a constant illuminant for a cleaner plot.
    # Should this really be using an illuminant??
    illuminant = illuminants.get_constant_illuminant()
    illuminant.scale (9.50)
    thinfilm_spectrum_plot_new (1.003, 1.33, 1.003, 400.0, illuminant,
        'Thin Film Interference Spectrum - 400 nm thick\nConstant Illuminant',
        'ThinFilm-Spectrum-400nm')
    thinfilm_spectrum_plot_new (1.003, 1.33, 1.003, 500.0, illuminant,
        'Thin Film Interference Spectrum - 500 nm thick\nConstant Illuminant',
        'ThinFilm-Spectrum-500nm')

    # Old-style.
    if True:
    #if False:
        thickness_nm_list = numpy.linspace(0.0, 750.0, 36)
        illuminant = illuminants.get_illuminant_D65_old()
        illuminants.scale_illuminant_old (illuminant, 9.50)
        thinfilm_patch_plot_old (1.500, 1.003, 1.500, thickness_nm_list,
            illuminant, 'ThinFilm Patch Plot', 'ThinFilm-Patch-Old')

        # Interesting to comment out the fine thickness list.
        thickness_nm_list = numpy.linspace(0.0, 1000.0, 800)
        illuminant = illuminants.get_illuminant_D65_old()
        illuminants.scale_illuminant_old (illuminant, 4.50)
        thinfilm_color_vs_thickness_plot_old (
            1.500, 1.003, 1.500, thickness_nm_list, illuminant,
            'Thin Film - Gap In Glass/Plastic (n = 1.50)\nIlluminant D65',
            'ThinFilm-GlassGap-Old')

        illuminant = illuminants.get_constant_illuminant_old()
        illuminants.scale_illuminant_old (illuminant, 9.50)
        thinfilm_spectrum_plot_old (1.003, 1.33, 1.003, 400.0, illuminant,
            'Thin Film Interference Spectrum - 400 nm thick\nConstant Illuminant',
            'ThinFilm-Spectrum-400nm-Old')


if __name__ == '__main__':
    t0 = time.clock()
    figures()
    t1 = time.clock()
    dt = t1 - t0
    print ('Elapsed time: %.3f sec' % (dt))
