'''
test_plots.py - Test cases for plots.py

This file is part of ColorPy.
'''
from __future__ import print_function

import numpy
import unittest

import blackbody
import ciexyz
import colormodels
import misc
import plots

class TestPlots(unittest.TestCase):
    ''' Test cases for plots. '''

    # Patch plots.

    def test_rgb_patch_plot(self, verbose=True):
        ''' Test the rgb patch plot. '''
        # Draw some primary colors.
        # FIXME: Separated color and name is bug-prone.
        primary_colors = [
            '#000000', '#FF0000', '#00FF00', '#0000FF',
            '#FFFF00', '#FF00FF', '#00FFFF', '#FFFFFF',
        ]
        primary_names = [
            'Black',  'Red',     'Green', 'Blue',
            'Yellow', 'Magenta', 'Cyan',  'White',
        ]
        filename = 'Test-RgbPatch' if verbose else None
        misc.colorstring_patch_plot (
            primary_colors, primary_names,
            'Primary RGB Colors',
            filename, num_across=4)

    def test_xyz_patch_plot(self, verbose=True):
        ''' Test the xyz patch plot. '''
        # MacBeth ColorChecker is a fine test here.
        filename = 'Test-XyzPatch' if verbose else None
        misc.MacBeth_ColorChecker_plot (filename)

    # Spectrum plots, old and new style.

    def test_spectrum_plot(self, verbose=True):
        ''' Test the spectrum plot. '''
        # Use a blackbody spectrum to test.
        T = 5000.0
        filename = 'Test-Spectrum' if verbose else None
        spectrum = blackbody.get_blackbody_spectrum (T)
        plots.spectrum_plot (
            spectrum,
            'Blackbody Spectrum 5000 K',
            filename,
            xlabel = 'Wavelength [nm]',
            ylabel = 'Specific Intensity')

    def test_spectrum_plot_old(self, verbose=True):
        ''' Test the old-style spectrum plot. '''
        # Use a blackbody spectrum to test.
        # Keeping much the same as the other spectrum plot also helps
        # to visually check that it is correct.
        T = 5000.0
        filename = 'Test-SpectrumOld' if verbose else None
        spectrum = blackbody.get_blackbody_spectrum (T)
        array    = spectrum.to_array()
        plots.spectrum_plot_old (
            array,
            'Blackbody Spectrum 5000 K - Old/Deprecated',
            filename,
            xlabel = 'Wavelength [nm]',
            ylabel = 'Specific Intensity')

    # Color vs parameter plot.

    def test_color_vs_param_plot(self, verbose=True):
        ''' Test the color-vs-parameter plot. '''
        # Plot color vs. wavelength for the visible spectrum.
        filename = 'Test-ColorVsParam' if verbose else None
        spect = ciexyz.Spectrum()
        c = 0.135
        # Get rgb colors for each wavelength.
        rgb_colors = numpy.empty ((spect.num_wl, 3))
        for i in range (spect.num_wl):
            xyz = ciexyz.xyz_from_wavelength (spect.wavelength [i])
            rgb = colormodels.rgb_from_xyz (xyz)
            rgb_colors [i] = rgb * c
        # Plot colors vs wavelength.
        plots.color_vs_param_plot (
            spect.wavelength,
            rgb_colors,
            'Color vs Wavelength',
            filename,
            tight = True,
            xlabel = r'Wavelength [nm]',
            ylabel = r'RGB Color')


if __name__ == '__main__':
    unittest.main()
