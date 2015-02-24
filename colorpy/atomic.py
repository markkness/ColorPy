'''
atomic.py - Atomic line spectra for the elements H, He, and Ne.

This file is part of ColorPy.
'''
from __future__ import print_function

import numpy

import ciexyz
import plots

#
# A sample emission spectrum that doesn't have equally spaced wavelengths.
#

# Only a line at 555 nm, with some width to look nicer.
emission_spectrum_555 = numpy.array([
    [360.0,   0.0],
    [549.0,   0.0],
    [552.0, 100.0],
    [553.0, 100.0],
    [554.0, 100.0],
    [555.0, 100.0],
    [556.0, 100.0],
    [557.0, 100.0],
    [558.0, 100.0],
    [557.0,   0.0],
    [830.0,   0.0],
])

#
# Elemental emission spectra. Intensity is 'arbitrary'. Data from ADC.
#

# Hydrogen.
emission_spectrum_H = numpy.array([
    [383.538,   5.0],
    [388.905,   6.0],
    [397.007,   8.0],
    [410.174,  15.0],
    [434.047,  30.0],
    [486.133,  80.0],
    [656.272, 120.0],
    [656.285, 180.0],
])

# Helium.
emission_spectrum_He = numpy.array([
    [381.961,         10],
    [381.976,          1],
    [388.865,        500],
    [396.473,         20],
    [400.927,          1],
    [402.619,         50],
    [402.636,          5],
    [412.082,         12],
    [412.099,          2],
    [414.376,          3],
    [438.793,         10],
    [443.755,          3],
    [447.148,        200],
    [447.168,         25],
    [471.315,         30],
    [471.338,          4],
    [492.193,         20],
    [501.568,        100],
    [504.774,         10],
    [587.562,        500],
    [587.597,        100],
    [667.815,        100],
    [686.748,          3],
    [706.519,        200],
    [706.571,         30],
    [728.135,         50],
])

# Neon.
emission_spectrum_Ne = numpy.array([
    [453.775,         10 ],
    [454.038,         10 ],
    [470.440,         15 ],
    [470.886,         12 ],
    [471.007,         10 ],
    [471.207,         10 ],
    [471.535,         15 ],
    [475.273,         10 ],
    [478.893,         12 ],
    [479.022,         10 ],
    [482.734,         10 ],
    [488.492,         10 ],
    [500.516,          4 ],
    [503.775,         10 ],
    [514.494,         10 ],
    [533.078,         25 ],
    [534.109,         20 ],
    [534.328,          8 ],
    [540.056,         60 ],
    [556.277,          5 ],
    [565.666,         10 ],
    [571.923,          5 ],
    [574.830,         12 ],
    [576.442,         80 ],
    [580.445,         12 ],
    [582.016,         40 ],
    [585.249,        500 ],
    [587.283,        100 ],
    [588.190,        100 ],
    [590.246,         60 ],
    [590.643,         60 ],
    [594.483,        100 ],
    [596.547,        100 ],
    [597.463,        100 ],
    [597.553,        120 ],
    [598.791,         80 ],
    [603.000,        100 ],
    [607.434,        100 ],
    [609.616,         80 ],
    [612.845,         60 ],
    [614.306,        100 ],
    [616.359,        120 ],
    [618.215,        250 ],
    [621.728,        150 ],
    [626.650,        150 ],
    [630.479,         60 ],
    [633.443,        100 ],
    [638.299,        120 ],
    [640.225,        200 ],
    [650.653,        150 ],
    [653.288,         60 ],
    [659.895,        150 ],
    [665.209,         70 ],
    [667.828,         90 ],
    [671.704,         20 ],
    [692.947,        100 ],
    [702.405,         90 ],
    [703.241,        100 ],
    [705.129,         50 ],
    [705.911,         80 ],
    [717.394,        100 ],
    [724.517,        100 ],
    [747.244,         40 ],
    [748.887,         90 ],
    [753.577,         80 ],
    [754.404,         60 ],
    [772.463,        100 ],
])

#
# Figures.
#

def emission_555_plot ():
    ''' Plot the sample spectrum with only a line at 555 nm. '''
    spect = ciexyz.Spectrum_from_array (emission_spectrum_555)
    plots.spectrum_plot (spect, '555 nm Spectral Line', 'Line-555')

def emission_plots ():
    ''' Plot some atomic emission spectra. '''
    # Hydrogen.
    spect = ciexyz.Spectrum_from_array (emission_spectrum_H)
    plots.spectrum_plot (spect, 'H Emission Spectrum', 'Emission-1-H')
    # Helium.
    spect = ciexyz.Spectrum_from_array (emission_spectrum_He)
    plots.spectrum_plot (spect, 'He Emission Spectrum', 'Emission-2-He')
    # Neon.
    spect = ciexyz.Spectrum_from_array (emission_spectrum_Ne)
    plots.spectrum_plot (spect, 'Ne Emission Spectrum', 'Emission-10-Ne')

#
# Main.
#

def figures ():
    emission_555_plot ()
    emission_plots ()


if __name__ == '__main__':
    figures()
