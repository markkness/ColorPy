'''
gamma.py - Gamma correction conversions.

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
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import math

'''
Gamma correction:

Gamma correction converts between displayable nonlinear color values,
and physical linear color values.

Linear color values are proportional to physical light intensity.
They do not directly correspond to palette entries used to draw the color
on the display monitor.

Display color values are the values specified on the computer to draw
the desired color. They are not proportional to physical light intensity.
They correspond to color palette register entries, although here they are
kept in the nominal range 0.0 to 1.0.

The mapping between the two is approximately a power law, with the
exponent called gamma. The mapping that gives linear values from display
values is called gamma correction, and the mapping that gives display values
from linear values is called gamma inversion. The two functions should be
inverses, and the nominal range of the component values is 0.0 to 1.0.

                   Gamma Correct
               <--------------------
               linear_from_display()
    L                                         D
 [linear]                                 [display]
[physical]                               [nonlinear]
                   Gamma Invert
               -------------------->
               display_from_linear()

In practice, one often uses mappings that have a linear region near black,
and a pseudo-exponential region for brighter colors. One commonly used mapping,
the sRGB standard, has an effective overall gamma exponent of about 2.2.

The original reason for the nonlinear display values, is in the physics of
CRT video monitors. The display value was used to set a voltage on the
electron gun in the CRT, this voltage was proportional to the display value.
But due to the vagaries of the electron gun physics, the intensity of the
resulting beam was not proportional to this voltage, rather it was nearly
an exponential function of it. Therefore the correction was needed.

Also, the nonlinear conversion makes reasonably efficient use of
integer values to display human-discernible light levels.

With LCD and other modern displays, the physics is not the same. However,
the modern devices are designed to have the same kind of color response as
the legacy CRT displays, and so this gamma correction still applies.
'''

# Simple power law for gamma correction.

def simple_gamma_invert (x, gamma_exponent):
    ''' Simple power law for gamma inverse correction. '''
    if x <= 0.0:
        return x
    else:
        return math.pow (x, 1.0 / gamma_exponent)

def simple_gamma_correct (x, gamma_exponent):
    ''' Simple power law for gamma correction. '''
    if x <= 0.0:
        return x
    else:
        return math.pow (x, gamma_exponent)

# sRGB gamma correction - http://www.color.org/sRGB.xalter
#
# The effect of the equations is to closely fit a straightforward
# gamma=2.2 curve with an slight offset to allow for invertability in
# integer math. Therefore, we are maintaining consistency with the
# gamma=2.2 legacy images and the video industry.
#
# Although the parameters for the linear region are the 'official' ones,
# they can actually be improved, so we do not usually use this specific
# implementation, it is for reference only.

def srgb_gamma_invert (x):
    ''' sRGB standard for gamma inverse correction. '''
    if x <= 0.00304:
        rtn = 12.92 * x
    else:
        rtn = 1.055 * math.pow (x, 1.0/2.4) - 0.055
    return rtn

def srgb_gamma_correct (x):
    ''' sRGB standard for gamma correction. '''
    if x <= 0.03928:
        rtn = x / 12.92
    else:
        rtn = math.pow ((x + 0.055) / 1.055, 2.4)
    return rtn

#
# Gamma converter classes.
#

class GammaConverter(object):
    ''' Interface for gamma correction objects.

     Each derived class must implement two methods,
     display_from_linear() and linear_from_display().
     These convert a float between nonlinear display values,
     and linear physical intensity values.
     The two functions should be inverses.

    'display' - Color values, nonlinear, to use in display code.
    'linear'  - Color values proportional to physical intensity.
     Both are nominally in the range 0.0 - 1.0.
     '''

    def display_from_linear(self, linear):
        ''' Convert linear physical intensity to nonlinear display values. '''
        # This is gamma inversion.
        raise NotImplementedError

    def linear_from_display(self, display):
        ''' Convert nonlinear display values to linear physical intensity. '''
        # This is gamma correction.
        raise NotImplementedError

    def gamma_invert(self, linear):
        ''' Gamma inversion is display_from_linear. '''
        return self.display_from_linear(linear)

    def gamma_correct(self, display):
        ''' Gamma correction is linear_from_display. '''
        return self.linear_from_display(display)


class GammaConverterPower(GammaConverter):
    ''' Gamma correction with a simple power law. '''

    def __init__(self, gamma):
        ''' Constructor. '''
        self.gamma = gamma    # Gamma exponent.

    def display_from_linear(self, linear):
        ''' Convert linear physical intensity to nonlinear display values. '''
        # This is gamma inversion.
        display = simple_gamma_invert(linear, self.gamma)
        return display

    def linear_from_display(self, display):
        ''' Convert nonlinear display values to linear physical intensity. '''
        # This is gamma correction.
        linear = simple_gamma_correct(display, self.gamma)
        return linear


class GammaConverterSrgbReference(GammaConverter):
    ''' Gamma correction according to sRGB standard.

    This is a reference implementation only, and not normally used. '''

    def display_from_linear(self, linear):
        ''' Convert linear physical intensity to nonlinear display values. '''
        # This is gamma inversion.
        display = srgb_gamma_invert (linear)
        return display

    def linear_from_display(self, display):
        ''' Convert nonlinear display values to linear physical intensity. '''
        # This is gamma correction.
        linear = srgb_gamma_correct (display)
        return linear


class GammaConverterFunction(GammaConverter):
    ''' Gamma correction with arbitrary conversion functions. '''

    def __init__(self,
        display_from_linear_func,    # Gamma invert function.
        linear_from_display_func):   # Gamma correction function.
        ''' Constructor. '''
        self.display_from_linear_func = display_from_linear_func
        self.linear_from_display_func = linear_from_display_func

    def display_from_linear(self, linear):
        ''' Convert linear physical intensity to nonlinear display values. '''
        # This is gamma inversion.
        display = self.display_from_linear_func (linear)
        return display

    def linear_from_display(self, display):
        ''' Convert nonlinear display values to linear physical intensity. '''
        # This is gamma correction.
        linear = self.linear_from_display_func (display)
        return linear


class GammaConverterHybrid(GammaConverter):
    ''' Gamma correction formulas as used in several standards.

    'display' - Color values as would be used in display code.
    'linear'  - Color values with numbers proportional to physical intensity.
    Both are nominally in the range 0.0 - 1.0.

    The curves have a linear region near black,
    and approximately exponential for visibly bright colors.
    The linear region avoids numerical trouble near zero.

    Note that the effective gamma exponent that this model provides,
    is not exactly the same value as the gamma that is nominally supplied.
    For example, sRGB uses the number gamma=2.4, but its curve actually
    better approximates an exponent of 2.2.

    display = Phi * linear,                    linear <  K0 / Phi
    display = (1+a) * linear^(1/gamma) - a,    linear >= K0 / Phi

    linear = display / Phi,                    display <  K0
    linear = ((display + a) / (1+a))^gamma,    display >= K0

    The two regions (linear/exponential) ought to connect sensibly.
    '''

    def __init__(self,
        gamma,            # Gamma exponent.
        a,                # Offset.
        K0,               # Intensity cutoff for linear range.
        Phi,              # Linear scaling.
        improve=True):    # True to enforce continuity at the 'edge-of-black'.
        # gamma and a are the main parameters.
        self.gamma      = float(gamma)
        self.a          = float(a)
        self.one_plus_a = 1.0 + self.a
        self.inv_gamma  = 1.0 / self.gamma
        # K0 and Phi can be specified, or derived from gamma and a.
        self.K0          = float(K0)
        self.Phi         = float(Phi)
        self.K0_over_Phi = self.K0 / self.Phi
        if improve:
            # Enforce continuity at the 'edge of black' and derive K0 and Phi.
            self.set_continuous_slope()

    def display_from_linear(self, linear):
        ''' Convert physical intensity to display values. '''
        if linear < self.K0_over_Phi:
            # Linear region.
            display = self.Phi * linear
        else:
            # Pseudo-exponential region.
            linear_inv_gamma = math.pow(linear, self.inv_gamma)
            display = self.one_plus_a * linear_inv_gamma - self.a
        return display

    def linear_from_display(self, display):
        ''' Convert display values to physical intensity. '''
        if display < self.K0:
            # Linear region.
            linear = display / self.Phi
        else:
            # Pseudo-exponential region.
            display_term = (display + self.a) / self.one_plus_a
            linear = math.pow(display_term, self.gamma)
        return linear

    # The values of K0 and Phi really come naturally from gamma and a,
    # if the two regions connect sensibly.
    # Setting K0 and Phi to enforce value and slope continuity works well.
    # Alternate methods to enforce only continuity seem less useful...
    # See:
    #     https://en.wikipedia.org/wiki/SRGB
    #     https://en.wikipedia.org/wiki/Rec._2020

    # Continuity of value and slope requires:
    #     K0 = a / (gamma - 1)
    #     Phi = ((1+a)^gamma * (gamma-1)^(gamma-1)) /
    #           (a^(gamma-1) * gamma^gamma)
    #
    # This seems to make a lot of sense to enforce.
    # The K0 and Phi values apply to the 'edge of black' and so
    # it is unlikely they are really carefully chosen, while the
    # continuity condition seems natural. And it also makes sense to
    # enforce the 'edge of black' all at once.

    def set_continuous_slope(self, verbose=False):
        ''' Automatically set K0 and Phi to enforce slope continuity. '''
        # Enforce continuity at the 'edge of black'.
        # This discards the original K0 and Phi.
        K0_start  = self.K0
        Phi_start = self.Phi
        K0_better = (self.a / (self.gamma - 1.0))
        Phi_term_1 = math.pow(self.one_plus_a, self.gamma)
        Phi_term_2 = math.pow(self.gamma - 1.0, self.gamma - 1.0)
        Phi_term_3 = math.pow(self.a, self.gamma - 1.0)
        Phi_term_4 = math.pow(self.gamma, self.gamma)
        Phi_better = (Phi_term_1 * Phi_term_2) / (Phi_term_3 * Phi_term_4)
        self.K0  = K0_better
        self.Phi = Phi_better
        self.K0_over_Phi = self.K0 / self.Phi
        msg = 'K0_start=%g    Phi_start=%g    K0_better=%.12f    Phi_better=%.12f' % (
            K0_start, Phi_start, K0_better, Phi_better)
        if verbose:
            print (msg)

    # Continuity between the linear and pseudo-exponential regions requires:
    #     ((K0 + a) / (1+a))^gamma = K0 / Phi
    #
    # This can be used to check a K0 estimate.
    # At present it does not seem to be a useful iteration.
    # Or you could calculate Phi.
    # That works sometimes but not reliably.
    # Generally these routines (improve_K0, improve_Phi) are experimental,
    # and not really successful.

    def set_continuous_only(self):
        ''' Try and enforce continuity only, which does not work well. '''
        # This is not currently useful.
        # Try and improve K0, Phi values.
        # This does nothing after set_continuous_slope().
        # Before it does not seem to converge!
        for i in range(4):
            # improve_K0 is not useful...
            #self.improve_K0()
            # improve_Phi is inconsistent...
            self.improve_Phi()

    def improve_K0(self):
        ''' Check K0 value. This converges poorly as an improvement attempt. '''
        # This is not currently useful.
        K0_start = self.K0
        lhs_term = ((self.K0 + self.a) / (self.one_plus_a))
        lhs = math.pow(lhs_term, self.gamma)
        rhs = self.K0 / self.Phi
        # New K0 value that was hoped better, but actually seems worse!
        K0_better = self.Phi * lhs
        self.K0 = K0_better
        msg = 'K0_start=%g    lhs=%g    rhs=%g    K0_better=%g' % (
            K0_start, lhs, rhs, K0_better)
        print (msg)

    def improve_Phi(self):
        ''' Automatically set Phi to enforce continuity at the edge of black. '''
        # This is not currently useful.
        # This seems to work well for sRGB and poorly for UHDTV.
        # Perhaps there are two solutions???
        Phi_start = self.Phi
        lhs_term = ((self.K0 + self.a) / (self.one_plus_a))
        lhs = math.pow(lhs_term, self.gamma)
        rhs = self.K0 / self.Phi
        # New Phi value that is ideally better.
        # Sometimes yes, sometimes no.
        Phi_better = self.K0 / lhs
        self.Phi = Phi_better
        self.K0_over_Phi = self.K0 / self.Phi
        msg = 'Phi_start=%.12f    lhs=%g    rhs=%g    Phi_better=%.12f' % (
            Phi_start, lhs, rhs, Phi_better)
        print (msg)


# Some explicitly defined gamma conversion functions:

# sRGB gamma correction, for HDTV.
#   http://en.wikipedia.org/wiki/SRGB, accessed 1 Apr 2015
# Note that, despite the nominal gamma=2.4,
# the function overall is designed to approximate gamma=2.2.

srgb_gamma_converter = GammaConverterHybrid(
    gamma=2.4, a=0.055, K0=0.03928, Phi=12.92)

# Rec 2020 gamma correction, for UHDTV.
#   https://en.wikipedia.org/wiki/Rec._2020, accessed 1 Apr 2015.

# Rec 2020/UHDTV for 10 bits per component.
uhdtv10_gamma_converter = GammaConverterHybrid(
	gamma=(1.0/0.45), a=0.099, K0=(4.5*0.018), Phi=4.5)

# Rec 2020/UHDTV for 12 bits per component.
uhdtv12_gamma_converter = GammaConverterHybrid(
	gamma=(1.0/0.45), a=0.0993, K0=(4.5*0.0181), Phi=4.5)
