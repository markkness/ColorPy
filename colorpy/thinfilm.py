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
import math, cmath, numpy
import pylab

import colormodels
import ciexyz
import illuminants
import plots

class thin_film:
    '''A thin film of dielectric material.'''
    def __init__ (self, n1, n2, n3, thickness_nm):
        pass
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

    def reflection_spectrum (self):
        '''Get the reflection spectrum (independent of illuminant) for the thin film.'''
        spectrum = ciexyz.empty_spectrum()
        (num_rows, num_cols) = spectrum.shape
        for i in xrange (0, num_rows):
            wl_nm = spectrum [i][0]
            spectrum [i][1] = self.get_interference_reflection_coefficient (wl_nm)
        return spectrum

    def illuminated_spectrum (self, illuminant):
        '''Get the spectrum when illuminated by the specified illuminant.'''
        spectrum = self.reflection_spectrum()
        (num_wl, num_col) = spectrum.shape
        for i in xrange (0, num_wl):
            spectrum [i][1] *= illuminant [i][1]
        return spectrum

    def illuminated_color (self, illuminant):
        '''Get the xyz color when illuminated by the specified illuminant.'''
        spectrum = self.illuminated_spectrum (illuminant)
        xyz = ciexyz.xyz_from_spectrum (spectrum)
        return xyz

#
# Figures
#

def thinfilm_patch_plot (n1, n2, n3, thickness_nm_list, illuminant, title, filename):
    '''Make a patch plot of the color of the film for each thickness [nm].'''
    xyz_colors = []
    for thickness_nm in thickness_nm_list:
        film = thin_film (n1, n2, n3, thickness_nm)
        xyz = film.illuminated_color (illuminant)
        xyz_colors.append (xyz)
    plots.xyz_patch_plot (xyz_colors, None, title, filename)

def thinfilm_color_vs_thickness_plot (n1, n2, n3, thickness_nm_list, illuminant, title, filename):
    '''Plot the color of the thin film for the specfied thicknesses [nm].'''
    num_thick = len (thickness_nm_list)
    rgb_list = numpy.empty ((num_thick, 3))
    for i in xrange (0, num_thick):
        film = thin_film (n1, n2, n3, thickness_nm_list [i])
        xyz = film.illuminated_color (illuminant)
        rgb_list [i] = colormodels.rgb_from_xyz (xyz)
    plots.color_vs_param_plot (
        thickness_nm_list,
        rgb_list,
        title,
        filename,
        xlabel = r'Thickness (nm)',
        ylabel = r'RGB Color')

def thinfilm_spectrum_plot (n1, n2, n3, thickness_nm, illuminant, title, filename):
    '''Plot the spectrum of the reflection from a thin film for the given thickness [nm].'''
    film = thin_film (n1, n2, n3, thickness_nm)
    illuminated_spectrum = film.illuminated_spectrum (illuminant)
    plots.spectrum_plot (
        illuminated_spectrum,
        title,
        filename,
        xlabel   = 'Wavelength (nm)',
        ylabel   = 'Refection Intensity')

def figures ():
    '''Draw some thin film plots.'''
    # simple patch plot
    thickness_nm_list = xrange (0, 1000, 10)
    illuminant = illuminants.get_illuminant_D65()
    illuminants.scale_illuminant (illuminant, 9.50)
    thinfilm_patch_plot (1.500, 1.003, 1.500, thickness_nm_list, illuminant, 'ThinFilm Patch Plot', 'ThinFilm-Patch')
    
    # plot the colors of films vs thickness.
    # we scale the illuminant to get a better range of color.
    #thickness_nm_list = xrange (0, 1000, 2)   # faster
    thickness_nm_list = xrange (0, 1000, 1)    # nicer
    # gap in glass/plastic
    illuminant = illuminants.get_illuminant_D65()
    illuminants.scale_illuminant (illuminant, 4.50)
    thinfilm_color_vs_thickness_plot (1.500, 1.003, 1.500, thickness_nm_list, illuminant,
        'Thin Film - Gap In Glass/Plastic (n = 1.50)\nIlluminant D65', 'ThinFilm-GlassGap')
    # soap bubble
    illuminant = illuminants.get_illuminant_D65()
    illuminants.scale_illuminant (illuminant, 9.50)
    thinfilm_color_vs_thickness_plot (1.003, 1.33, 1.003, thickness_nm_list, illuminant,
        'Thin Film - Soap Bubble (n = 1.33)\nIlluminant D65', 'ThinFilm-SoapBubble')
    # oil slick on water
    illuminant = illuminants.get_illuminant_D65()
    illuminants.scale_illuminant (illuminant, 15.00)
    thinfilm_color_vs_thickness_plot (1.003, 1.44, 1.33, thickness_nm_list, illuminant,
        'Thin Film - Oil Slick (n = 1.44) on Water (n = 1.33)\nIlluminant D65', 'ThinFilm-OilSlick')
    # large index of refraction bubble
    illuminant = illuminants.get_illuminant_D65()
    illuminants.scale_illuminant (illuminant, 3.33)
    thinfilm_color_vs_thickness_plot (1.003, 1.60, 1.003, thickness_nm_list, illuminant,
        'Thin Film - Large Index (n = 1.60) Bubble\nIlluminant D65', 'ThinFilm-LargeBubble')

    # plot the spectrum of the refection for a couple of thicknesses - using constant illuminant for cleaner plot
    illuminant = illuminants.get_constant_illuminant()
    illuminants.scale_illuminant (illuminant, 9.50)
    thinfilm_spectrum_plot (1.003, 1.33, 1.003, 400.0, illuminant,
        'Thin Film Interference Spectrum - 400 nm thick\nConstant Illuminant',
        'ThinFilm-Spectrum-400nm')
    thinfilm_spectrum_plot (1.003, 1.33, 1.003, 500.0, illuminant,
        'Thin Film Interference Spectrum - 500 nm thick\nConstant Illuminant',
        'ThinFilm-Spectrum-500nm')
