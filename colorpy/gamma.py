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

# Gamma correction
#
# Non-gamma corrected rgb values, also called non-linear rgb values,
# correspond to palette register entries [although here they are kept
# in the range 0.0 to 1.0.]  The numerical values are not proportional
# to the amount of light energy present.
#
# Gamma corrected rgb values, also called linear rgb values,
# do not correspond to palette entries.  The numerical values are
# proportional to the amount of light energy present.
#
# This effect is particularly significant with CRT displays.
# With LCD displays, it is less clear (at least to me), what the genuinely
# correct correction should be.

# Available gamma correction methods.
GAMMA_CORRECT_POWER = 0    # Simple power law, using supplied gamma exponent.
GAMMA_CORRECT_SRGB  = 1    # sRGB correction formula.

# sRGB standard effective gamma.  This exponent is not applied explicitly.
STANDARD_GAMMA = 2.2

# Although NTSC specifies a gamma of 2.2 as standard, this is designed
# to account for the dim viewing environments typical of TV, but not
# computers.  Well-adjusted CRT displays have a true gamma in the range
# 2.35 through 2.55.  We use the physical gamma value here, not 2.2,
# thus not correcting for a dim viewing environment.
# [Poynton, Gamma FAQ p.5, p.9, Hall, p. 121]
POYNTON_GAMMA = 2.45

# Simple power laws for gamma correction

def simple_gamma_invert (x, gamma_exponent):
    '''Simple power law for gamma inverse correction.'''
    if x <= 0.0:
        return x
    else:
        return math.pow (x, 1.0 / gamma_exponent)

def simple_gamma_correct (x, gamma_exponent):
    '''Simple power law for gamma correction.'''
    if x <= 0.0:
        return x
    else:
        return math.pow (x, gamma_exponent)

# sRGB gamma correction - http://www.color.org/sRGB.xalter
# The effect of the equations is to closely fit a straightforward
# gamma 2.2 curve with an slight offset to allow for invertability in
# integer math. Therefore, we are maintaining consistency with the
# gamma 2.2 legacy images and the video industry.

def srgb_gamma_invert (x):
    '''sRGB standard for gamma inverse correction.'''
    if x <= 0.00304:
        rtn = 12.92 * x
    else:
        rtn = 1.055 * math.pow (x, 1.0/2.4) - 0.055
    return rtn

def srgb_gamma_correct (x):
    '''sRGB standard for gamma correction.'''
    if x <= 0.03928:
        rtn = x / 12.92
    else:
        rtn = math.pow ((x + 0.055) / 1.055, 2.4)
    return rtn

def srgb_gamma_invert_reference (x):
    '''Reference implementation of sRGB standard for gamma inverse correction.'''
    return srgb_gamma_invert(x)

def srgb_gamma_correct_reference (x):
    '''Reference implementation of sRGB standard for gamma correction.'''
    return srgb_gamma_correct(x)

#
# New gamma correction...
# FIXME: Is this even used??? It is tested, but ColorConverter() may not use it!!!
#

class GammaConverter(object):
    ''' Interface for gamma correction objects.

     There should be two methods. Both take a float argument and return a float.
     They should be inverses.

    'display' - Color values as would be used in display code.
    'linear'  - Color values with numbers proportional to physical intensity.
     Both are nominally in the range 0.0 - 1.0.
     '''

    def display_from_linear(self, C_linear):
        ''' Convert linear physical intensity to nonlinear display values. '''
        # This is gamma inversion, not gamma correction.
        raise NotImplementedError

    def linear_from_display(self, C_display):
        ''' Convert nonlinear display values to linear physical intensity. '''
        # This is gamma correction.
        raise NotImplementedError


class GammaConverterPower(GammaConverter):
    ''' Gamma correction with a simple power law. '''

    def __init__(self, gamma):
        ''' Constructor. '''
        self.gamma = gamma    # Gamma exponent.

    def display_from_linear(self, C_linear):
        ''' Convert linear physical intensity to nonlinear display values. '''
        # This is gamma inversion, not gamma correction.
        C_display = simple_gamma_invert (C_linear, self.gamma)
        return C_display

    def linear_from_display(self, C_display):
        ''' Convert nonlinear display values to linear physical intensity. '''
        # This is gamma correction.
        C_linear = simple_gamma_correct (C_display, self.gamma)
        return C_linear


class GammaConverterSrgb(GammaConverter):
    ''' Gamma correction according to sRGB standard. '''

    def display_from_linear(self, C_linear):
        ''' Convert linear physical intensity to nonlinear display values. '''
        # This is gamma inversion, not gamma correction.
        C_display = srgb_gamma_invert (C_linear)
        return C_display

    def linear_from_display(self, C_display):
        ''' Convert nonlinear display values to linear physical intensity. '''
        # This is gamma correction.
        C_linear = srgb_gamma_correct (C_display)
        return C_linear


class GammaConverterFunction(GammaConverter):
    ''' Gamma correction with arbitrary conversion functions. '''

    def __init__(self,
        display_from_linear_function,    # Gamma invert function.
        linear_from_display_function):   # Gamma correction function.
        ''' Constructor. '''
        self.display_from_linear_function = display_from_linear_function
        self.linear_from_display_function = linear_from_display_function

    def display_from_linear(self, C_linear):
        ''' Convert linear physical intensity to nonlinear display values. '''
        # This is gamma inversion, not gamma correction.
        C_display = self.display_from_linear_function (C_linear)
        return C_display

    def linear_from_display(self, C_display):
        ''' Convert nonlinear display values to linear physical intensity. '''
        # This is gamma correction.
        C_linear = self.linear_from_display_function (C_display)
        return C_linear


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

    C_display = Phi * C_linear,                    C_linear <  K0 / Phi
    C_display = (1+a) * C_linear^(1/gamma) - a,    C_linear >= K0 / Phi

    C_linear = C_display / Phi,                    C_display <  K0
    C_linear = ((C_display + a) / (1+a))^gamma,    C_display >= K0

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

    def display_from_linear(self, C_linear):
        ''' Convert physical intensity to display values. '''
        if C_linear < self.K0_over_Phi:
            # Linear region.
            C_display = self.Phi * C_linear
        else:
            # Pseudo-exponential region.
            C_linear_inv_gamma = math.pow(C_linear, self.inv_gamma)
            C_display = self.one_plus_a * C_linear_inv_gamma - self.a
        return C_display

    def linear_from_display(self, C_display):
        ''' Convert display values to physical intensity. '''
        if C_display < self.K0:
            # Linear region.
            C_linear = C_display / self.Phi
        else:
            # Pseudo-exponential region.
            C_display_term = (C_display + self.a) / self.one_plus_a
            C_linear = math.pow(C_display_term, self.gamma)
        return C_linear

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


# sRGB gamma correction, for HDTV.
#   http://en.wikipedia.org/wiki/SRGB, accessed 1 Apr 2015
# Note that, despite the nominal gamma=2.4, the function overall is designed
# to approximate gamma=2.2.

srgb_gamma_converter = GammaConverterHybrid(
    gamma=2.4, a=0.055, K0=0.03928, Phi=12.92)

# Rec 2020 gamma correction, for UHDTV.
#   https://en.wikipedia.org/wiki/Rec._2020, accessed 1 Apr 2015.

# Rec 2020/UHDTV for 10 bits per component.
uhdtv_10_gamma_converter = GammaConverterHybrid(
	gamma=(1.0/0.45), a=0.099, K0=(4.5*0.018), Phi=4.5)

# Rec 2020/UHDTV for 12 bits per component.
uhdtv_12_gamma_converter = GammaConverterHybrid(
	gamma=(1.0/0.45), a=0.0993, K0=(4.5*0.0181), Phi=4.5)
