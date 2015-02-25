'''
pure_colors.py - Some work-in-progress related to pure colors.

Pure colors mean spectral lines and the 'purples'.

This file is part of ColorPy.
'''
from __future__ import print_function

import math
import numpy

import colormodels
import ciexyz
import plots

#
# Miscellaneous stuff for spectral line colors.
# This is used by the shark fin plot as well as the examples in this file.
#

def scale_rgb_max (xyz_array, brightness):
    ''' Scale each color to have the max rgb value be the desired brightness. '''
    num_points = xyz_array.shape[0]
    for i in range (num_points):
        rgb = colormodels.brightest_rgb_from_xyz (xyz_array [i], brightness)
        xyz_array [i] = colormodels.xyz_from_rgb (rgb)


def get_spectral_colors (wl_array):
    ''' Get the pure spectral line colors. '''
    # wl_array = wavelengths in nm.
    num  = wl_array.shape[0]
    xyzs = numpy.zeros((num, 3))
    for i in range (num):
        wl  = wl_array [i]
        xyz = ciexyz.xyz_from_wavelength (wl)
        colormodels.xyz_normalize (xyz)
        xyzs [i] = xyz
    return xyzs


def get_purple_colors (t_array, violet_xyz, red_xyz):
    ''' Get the pure purple colors by interpolating between violet and red. '''
    # t_array    = interpolation fractions 0.0 to 1.0
    # violet_xyz = xyz color for pure violet
    # red_xyz    = xyz_color for pure red
    num  = t_array.shape[0]
    xyzs = numpy.zeros((num, 3))
    # FIXME: violet and red may be backwards.
    first_xyz = violet_xyz
    last_xyz  = red_xyz
    for i in range (num):
        t   = t_array [i]
        omt = 1.0 - t
        xyz = t * first_xyz + omt * last_xyz
        colormodels.xyz_normalize (xyz)
        xyzs [i] = xyz
    return xyzs


def get_pure_colors (brightness, wl_array, purple_array):
    ''' Get an array of xyz colors, for pure spectral lines and purples.

    The 'purples' are colors interpolated between the lowest wavelength (violet)
    and the highest wavelength (red).

    brightness  : The maximum rgb component of each returned color.
    wl_array    : Array of wavelengths [nm] representing the visible wavelengths.
    purple_array: Array of interpolation fractions [0.0-1.0].
    '''
    # Get the spectral line colors.
    xyzs_spect = get_spectral_colors (wl_array)
    # Get the purples.
    violet_xyz  = xyzs_spect [ 0, :]
    red_xyz     = xyzs_spect [-1, :]
    xyzs_purple = get_purple_colors (purple_array, violet_xyz, red_xyz)
    # Join spectral colors and purples and scale.
    xyzs = numpy.vstack ([xyzs_spect, xyzs_purple])
    scale_rgb_max (xyzs, brightness)
    return xyzs


def get_num_pure_colors (brightness, num_spect, num_purple):
    ''' Get an array of xyz colors, for pure spectral lines and purples.

    The count of pure spectral colors and purples is as specified.
    '''
    # FIXME: The lowest and highest wavelength are probably not the best
    # ones to use for the violet and red values. As one approaches the end
    # of the visible spectrum, the colors approach zero, and then the scaled
    # value is not well defined. But we do this for now.
    wl_array     = numpy.linspace (ciexyz.start_wl_nm, ciexyz.end_wl_nm, num=num_spect)
    purple_array = numpy.linspace (0.0, 1.0, num=num_purple)
    xyzs         = get_pure_colors (brightness, wl_array, purple_array)
    return xyzs


def get_normalized_spectral_line_colors (
    brightness=1.0, num_purples=0, dwl_angstroms=10.0):
    ''' Get an array of xyz colors, for pure spectral lines and purples.

    brightness   : Desired maximum rgb component of each color.
    num_purples  : Number of colors to interpolate in the 'purple' range.
    dwl_angstroms: Wavelength separation, in angstroms (0.1 nm).
    '''
    dwl_nm    = dwl_angstroms / 10.0
    num_spect = int(round((ciexyz.end_wl_nm - ciexyz.start_wl_nm) / dwl_nm)) + 1
    xyzs      = get_num_pure_colors (brightness, num_spect, num_purples)
    return xyzs


def get_perceptually_equal_spaced_colors (brightness, num_samples, verbose=False):
    ''' Get an array of xyz colors, which are perceptually equally spaced.

    The colors are first pure spectral lines from violet to red, and then
    the purples. They are scaled so that max(rgb) = brightness.
    num_samples is the total number of colors to return.
    '''
    # Get a fine set of pure colors and lots of purples.
    # Anything finer than 1 nm is probably sufficient.
    num_spect  = 1000
    num_purple = 100
    xyzs = get_num_pure_colors (brightness, num_spect, num_purple)
    num_colors = xyzs.shape[0]
    # Choose either Luv or Lab (nearly) perceptually uniform color space.
    if True:
        uniform_from_xyz = colormodels.luv_from_xyz
    else:
        uniform_from_xyz = colormodels.lab_from_xyz
    # Convert colors to perceptually uniform space.
    uniforms = numpy.empty ((num_colors, 3))
    for i in range (num_colors):
        uniforms[i] = uniform_from_xyz (xyzs[i])
    # Get distance along closed curve in uniform space.
    # For N vertices, there are also N segments.
    # segment 0 is from vertex 0 to vertex 1, and so on so
    # segment i is from vertex i to vertex i + 1, except that i + 1 -> 0
    # for the last segment, which goes back to the first point.
    # The accumulated distances S[j] are the distances to the end of the
    # segments j. Thus S[0] is the distance to the end of the first segment,
    # and is greater than zero. It makes sense to consider S[-1] = 0.0.
    # Distance between points.
    ds = numpy.zeros((num_colors))
    for i in range (num_colors):
        im = i
        ip = i + 1
        # Handle end of closed curve.
        if i == (num_colors - 1):
            ip = 0
        dri = uniforms[ip] - uniforms[im]
        dsi = math.sqrt (numpy.dot (dri, dri))
        ds [i] = dsi
    # Total distance.
    S = numpy.zeros((num_colors))
    total = 0.0
    for i in range (num_colors):
        total += ds[i]
        S[i] = total
    S_total = S[-1]
    # Get desired total distance for each sample point.
    xyz_samples = numpy.zeros ((num_samples, 3))
    for i in range (num_samples):
        # Choose fraction from 0.0 to near (but not equal) 1.0.
        fi = float(i) / float(num_samples)
        si = fi * S_total
        # Find curve segment that encloses this distance.
        # This should always be: 0 <= j < N.
        j = numpy.searchsorted(S, si)
        # Get total distance to start and end of this segment.
        if j > 0:
            s0 = S[j -1]
        else:
            # Start of first segment has S[-1] = 0.0.
            s0 = 0.0
        s1 = S[j]
        # Get what fraction we are along this segment.
        # Should always be: 0 <= t <= 1.
        t = (si - s0) / (s1 - s0)
        # Get vertex indices at start and end of the segment.
        v0 = j
        v1 = j + 1
        if v1 >= num_colors:
            # Last segment ends at first point.
            v1 = 0
        if verbose:
            print ('i: %d    f: %.4f    s: %.4f    j: %d    t: %g    v0: %d    v1: %d' % (
                i, fi, si, j, t, v0, v1))
        # Now interpolate between the xyz colors at vertices.
        xyz0 = xyzs[v0, :]
        xyz1 = xyzs[v1, :]
        xyz = (1.0 - t) * xyz0 + t * xyz1
        xyz_samples[i, :] = xyz
    return xyz_samples

#
# Write pure color values as an HTML document.
#

def write_visible_spectrum_html (filename='visible_spectrum.html'):
    ''' Write an HTML file with the pure spectral colors. '''
    spectrum = ciexyz.Spectrum()
    num_wl = spectrum.num_wl
    # Get rgb colors for each wavelength.
    # Scale the first so that max(rgb) = 1.0.
    # Scale the second via brightest_rgb_from_xyz(). (?)
    rgb_1 = numpy.empty ((num_wl, 3))
    rgb_2 = numpy.empty ((num_wl, 3))
    for i in range (num_wl):
        xyz      = ciexyz.xyz_from_wavelength (spectrum.wavelength[i])
        rgb_1[i] = colormodels.rgb_from_xyz (xyz)
        rgb_2[i] = colormodels.brightest_rgb_from_xyz (xyz)
    # Scale rgb_1 to make brightest rgb value = 1.0.
    rgb_max = numpy.max (rgb_1)
    scaling = 1.0 / rgb_max
    rgb_1 *= scaling

    # Write the data as an HTML document.
    with open (filename, 'w') as f:
        # Html headers.
        f.write ('<html>\n')
        f.write ('<head>\n')
        f.write ('<title>Colors of Pure Spectral Lines</title>\n')
        f.write ('</head>\n')
        f.write ('<body>\n')
        f.write ('<p><h1>Colors of Pure Spectral Lines</h1></p>\n')
        f.write ('<p>%s</p>\n' % 'White added to undisplayable pure colors to fit into rgb space.')
        f.write ('<hr/>\n')
        # Table headers.
        f.write ('<table border cellpadding="5">\n')
        f.write ('<tr>\n')
        f.write ('<th>Wavelength</th>\n')
        f.write ('<th>R</th>\n')
        f.write ('<th>G</th>\n')
        f.write ('<th>B</th>\n')
        f.write ('<th>Hex Code</th>\n')
        f.write ('<th width=200>Full Brightness</th>\n')
        f.write ('<th width=200>Perceptual Brightness</th>\n')
        f.write ('</tr>\n')
        # Each row of table.
        for i in range (num_wl):
            irgb_1 = colormodels.irgb_from_rgb (rgb_1 [i])
            irgb_2 = colormodels.irgb_from_rgb (rgb_2 [i])
            red   = irgb_2 [0]
            green = irgb_2 [1]
            blue  = irgb_2 [2]
            hexstr_1 = colormodels.irgb_string_from_irgb (irgb_1)
            hexstr_2 = colormodels.irgb_string_from_irgb (irgb_2)

            iwl = spectrum.wavelength[i]
            code = '%.1f nm' % iwl

            f.write ('<tr>\n')
            f.write ('<td>%s</td>\n' % (code))
            f.write ('<td>%d</td>\n' % (red))
            f.write ('<td>%d</td>\n' % (green))
            f.write ('<td>%d</td>\n' % (blue))
            f.write ('<td>%s</td>\n' % (hexstr_2))
            swatch = "&nbsp;"
            f.write ('<td bgcolor="%s">%s</td>\n' % (hexstr_2, swatch))
            f.write ('<td bgcolor="%s">%s</td>\n' % (hexstr_1, swatch))
            f.write ('</tr>\n')
        f.write ('</table>\n')
        # End of html document.
        f.write ('</body>\n')
        f.write ('</html>\n')


def write_pantone_reference_html (filename='pantone_references.html'):
    ''' Write an HTML document with some references to Pantone colors.

    These have nothing to do with pure spectral colors.
    '''
    def write_link (f, url, text):
        '''Write an html link.'''
        link = '<a href="%s">%s</a><br/>\n' % (url, text)
        f.write (link)

    with open (filename, 'w') as f:
        f.write ('<html>\n')
        f.write ('<head>\n')
        f.write ('<title>Pantone Color References</title>\n')
        f.write ('</head>\n')
        f.write ('<body>\n')
        f.write ('<p><h1>Pantone Color References</h1></p>\n')
        f.write ('<hr/>\n')
        # Reference links for Pantone colors.
        # Links commented out failed 25 Feb 2015.
        # One source for data.
        write_link (f,
            'http://goffgrafix.com/pantone-rgb-100.php',
            'Goffgrafix.com')
        ### Another source with basically the same data.
        ##write_link (f,
        ##    'http://www.sandaleo.com/pantone.asp',
        ##    'Sandaleo.com')
        ### One with more colors including metallic (also some errors), not quite consistent with the first two.
        ##write_link (f,
        ##    'http://www.loral.org/Z/Colors/100.html',
        ##    'Loral.org - Conversions based on CorelDRAW v12 Pantone Solid Coated or Pastel Coated tables and sRGB color space.')
        # Some example Pantone colors.
        ### Some colors for various sports teams.
        ##write_link (f,
        ##    'http://www.pennjersey.info/forums/questions-answers/7895-pantone-colors-colleges-university-mlb-nfl-teams.html',
        ##    'Pantone colors for some sports teams.')
        # Some colors for various national flags.
        write_link (f,
            'http://desktoppub.about.com/od/colorpalettes/l/aa_flagcolors.htm',
            'What color is your flag? Pantone colors for some flags.')
        write_link (f,
            'http://desktoppub.about.com/library/weekly/blcpflagsrwb.htm',
            'Red, White, &amp Blue - Pantone colors for some flags.')
        write_link (f,
            'http://desktoppub.about.com/library/weekly/blcpflagsyellow.htm',
            'Yellow or Gold - Pantone colors for some flags.')
        write_link (f,
            'http://desktoppub.about.com/library/weekly/blcpflagsgreen.htm',
            'Green - Pantone colors for some flags.')
        write_link (f,
            'http://desktoppub.about.com/library/weekly/blcpatrioticswatches.htm',
            'Color swatches - Pantone colors for some flags.')
        ### Official Pantone webpages.
        ##write_link (f,
        ##    'http://pantone.com/pages/pantone/Pantone.aspx?pg=19970&ca=25',
        ##    'An official PANTONE page')
        ##write_link (f,
        ##    'http://pantone.com/pages/products/product.aspx?ca=1&pid=293&',
        ##    'Another official PANTONE page')
        # End of html document.
        f.write ('</body>\n')
        f.write ('</html>\n')

#
# Figures.
#

def pure_colors_patch_plots ():
    ''' Create patch plots of the pure spectral line colors, and also with purples. '''
    brightness = 1.0
    # Pure spectral colors, and no purples.
    num_spect = 400
    xyzs      = get_num_pure_colors (brightness, num_spect, 0)
    plots.xyz_patch_plot (xyzs, None,
        'Colors of pure spectral lines',
        'PureColors-Spectral', num_across=20)
    # With 100 purples.
    xyzs      = get_num_pure_colors (brightness, num_spect, 100)
    plots.xyz_patch_plot (xyzs, None,
        'Colors of pure spectral lines plus purples',
        'PureColors-SpectralPurples', num_across=20)


def perceptually_equal_spaced_color_plot (
    brightness,
    title,
    filename,
    num_samples,
    num_across=20):
    ''' Patch plot of perceptually equally spaced pure colors.

    Pure colors means pure spectral lines plus purples.
    Each color has max(rgb) = brightness.
    '''
    xyzs = get_perceptually_equal_spaced_colors (brightness, num_samples)
    plots.xyz_patch_plot (
        xyzs, None, title, filename, num_across=num_across)


def perceptually_equal_spaced_color_plots ():
    ''' Do the calculations for several brightness values. '''
    # These are colors which are perceptually equally spaced.
    # Various max(rgb) brightness values are used.
    brightness_list = [1.0, 0.9, 0.8, 0.75, 0.6, 0.5, 0.4, 0.3, 0.25]
    for brightness in brightness_list:
        ibright     = int(round(100.0 * brightness))
        title       = 'Perceptually Equally Spaced Pure Colors %d%%' % ibright
        filename    = 'PerceptSpacedColors_%d' % ibright
        num_samples = 160
        perceptually_equal_spaced_color_plot (
            brightness, title, filename, num_samples)

#
# Main.
#

def figures ():
    ''' Draw plots of the pure colors and purples. '''
    # Html documents.
    write_pantone_reference_html()
    write_visible_spectrum_html()
    # Plots.
    pure_colors_patch_plots()
    perceptually_equal_spaced_color_plots()


if __name__ == '__main__':
    figures()
