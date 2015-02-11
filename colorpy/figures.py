'''
figures.py - Create all the ColorPy sample figures.

Description:

Creates the sample figures.

This can also create the figures with some non-default initialization conditions.

Functions:

figures() -
    Create all the sample figures.

figures_clip_clamp_to_zero () -
    Adjust the color clipping method, and create the sample figures.

figures_gamma_245 () -
    Adjust the gamma correction to a power law gamma = 2.45 and create samples.

figures_white_A () -
    Adjust the white point (for Luv/Lab) and create sample figures.

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
import colormodels
import ciexyz
import illuminants
import plots
import blackbody
import rayleigh
import thinfilm
import misc

def figures ():
    '''Create all the ColorPy sample figures.'''
    # no figures for colormodels and ciexyz
    colormodels.init()  # default
    illuminants.figures()
    plots.figures()
    blackbody.figures()
    rayleigh.figures()
    thinfilm.figures()
    misc.figures()

def figures_clip_clamp_to_zero ():
    '''Adjust the color clipping method, and create the sample figures.'''
    colormodels.init()
    colormodels.init_clipping (colormodels.CLIP_CLAMP_TO_ZERO)
    figures()

def figures_gamma_245 ():
    '''Adjust the gamma correction to a power law gamma = 2.45 and create samples.'''
    colormodels.init()
    colormodels.init_gamma_correction (
        display_from_linear_function = colormodels.simple_gamma_invert,
        linear_from_display_function = colormodels.simple_gamma_correct,
        gamma = 2.45)
    figures()

def figures_white_A ():
    '''Adjust the white point (for Luv/Lab) and create sample figures.'''
    colormodels.init()
    colormodels.init_Luv_Lab_white_point (colormodels.WhiteA)
    figures()


if __name__ == '__main__':
    figures()
