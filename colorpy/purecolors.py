'''
purecolors.py - Calculation of 'pure colors'.

Pure colors mean spectral lines and the 'purples'.

Specialized plots:

shark_fin_plot () -
    Draw the 'shark fin' CIE chromaticity diagram of the pure spectral lines (plus purples) in xy space.

This file is part of ColorPy.
'''
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import io
import math
import numpy
import matplotlib.pyplot as pyplot

import colormodels
import ciexyz
import plots

# Calculation of 'pure' colors. This means both, the colors of single spectral
# lines, which are as saturated as possible, as well as the 'purples', which
# are linear combinations of pure violet and pure red. These 'purples' are
# not pure spectral lines, but they are as far from white as possible, so
# they are still considered 'pure' colors here.

# The full start and end of the visible wavelength range is 360 to 830 nm.
# However, near these endpoints, the light is poorly percieved, and so the
# color approaches zero. This means that the chromaticity is poorly defined.
# However, the chromaticity is not changing much near these endpoints.
# So, to use a start and end wavelength for the 'pure colors', it makes more
# sense to use a slightly smaller range of wavelengths.
# Wyszecki and Stiles, Color Science, p. 158 suggests that many practical
# colorimetric applications use the range 380 to 780 nm, so use that instead.

PURE_VIOLET_NM = 380.0    # Wavelength [nm] for practical 'pure' violet color.
PURE_RED_NM    = 780.0    # Wavelength [nm] for practical 'pure' red color.

def scale_rgb_max (xyz_array, brightness):
    ''' Scale each xyz color to have max(rgb) value be the desired brightness.

    xyz_array : Array of colors as xyz values.
    brightness: Desired max(rgb).
    '''
    # Comments on selecting this scaling algorithm:
    # Scaling to Y=1 puts all the colors at equal perceptual brightness,
    # which seems like possibly a good starting point.
    # But it does not work. It makes the extreme wls very bright,
    # as it compensates for their originally small Y. So skip this idea.
    # Instead, to get the 'pure essence' color, we want as bright as possible
    # with the same chromaticity. So scale so max(rgb) = 1.0.
    num_points = xyz_array.shape[0]
    for i in range (num_points):
        rgb = colormodels.brightest_rgb_from_xyz (xyz_array [i], brightness)
        xyz_array [i] = colormodels.xyz_from_rgb (rgb)


def get_spectral_colors (wl_array, brightness):
    ''' Get the pure spectral line xyz colors.

    wl_array  : array of wavelengths in nm.
    brightness: colors are scaled so max(rgb) = brightness.
    '''
    num  = wl_array.shape[0]
    xyzs = numpy.zeros((num, 3))
    for i in range (num):
        wl  = wl_array [i]
        xyz = ciexyz.xyz_from_wavelength (wl)
        xyzs [i] = xyz
    scale_rgb_max (xyzs, brightness)
    return xyzs


def get_purple_colors (t_array, violet_xyz, red_xyz, brightness):
    ''' Get the pure purple xyz colors by interpolating between violet and red.

    The purple for t=0.0 is exactly red, and the purple for t=1.0 is violet.

    t_array   : 1D array of interpolation fractions 0.0 to 1.0.
    violet_xyz: xyz color for pure violet.
    red_xyz   : xyz_color for pure red.
    brightness: colors are scaled so max(rgb) = brightness.
    '''
    num  = t_array.shape[0]
    xyzs = numpy.zeros((num, 3))
    first_xyz = violet_xyz
    last_xyz  = red_xyz
    for i in range (num):
        t   = t_array [i]
        omt = 1.0 - t
        xyz = t * first_xyz + omt * last_xyz
        xyzs [i] = xyz
    scale_rgb_max (xyzs, brightness)
    return xyzs


def get_pure_colors (wl_array, purple_array, brightness):
    ''' Get an array of xyz colors, for pure spectral lines and purples.

    The 'purples' are colors interpolated between the lowest wavelength (violet)
    and the highest wavelength (red).

    wl_array    : Array of wavelengths [nm] representing the visible wavelengths.
    purple_array: Array of interpolation fractions [0.0-1.0].
    brightness  : The maximum rgb component of each returned xyz color.
    '''
    # Get the spectral line colors.
    xyzs_spect = get_spectral_colors (wl_array, brightness)
    # Get the purples.
    violet_xyz  = xyzs_spect [ 0, :]
    red_xyz     = xyzs_spect [-1, :]
    xyzs_purple = get_purple_colors (purple_array, violet_xyz, red_xyz, brightness)
    # Join spectral colors and purples.
    xyzs = numpy.vstack ([xyzs_spect, xyzs_purple])
    return xyzs


def get_num_pure_colors (num_spect, num_purple, brightness):
    ''' Get an array of xyz colors, for pure spectral lines and purples.

    The count of pure spectral colors and purples is as specified.
    '''
    wl_array     = numpy.linspace (PURE_VIOLET_NM, PURE_RED_NM, num=num_spect)
    purple_array = numpy.linspace (0.0, 1.0, num=num_purple)
    xyzs         = get_pure_colors (wl_array, purple_array, brightness)
    return xyzs


def get_normalized_spectral_line_colors (
    brightness=1.0, num_purples=0, dwl_angstroms=10.0):
    ''' Get an array of xyz colors, for pure spectral lines and purples.

    brightness   : Desired maximum rgb component of each color.
    num_purples  : Number of colors to interpolate in the 'purple' range.
    dwl_angstroms: Wavelength separation, in angstroms (0.1 nm).
    '''
    # This is deprecated but retained for compatibility.
    # Any previous users may want to consider the wavelength range.
    dwl_nm       = dwl_angstroms / 10.0
    num_spect    = int(round((PURE_RED_NM - PURE_VIOLET_NM) / dwl_nm)) + 1
    wl_array     = numpy.linspace (PURE_VIOLET_NM, PURE_RED_NM, num=num_spect)
    purple_array = numpy.linspace (0.0, 1.0, num=num_purples)
    xyzs         = get_pure_colors (wl_array, purple_array, brightness)
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
    xyzs = get_num_pure_colors (num_spect, num_purple, brightness)
    num_colors = xyzs.shape[0]
    # Choose either Luv or Lab (nearly) perceptually uniform color space.
    # FIXME: Should be able to pass as a parameter.
    # Would this be a colormodels object???
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
        # Now interpolate between the xyz colors at vertices.
        xyz0 = xyzs[v0, :]
        xyz1 = xyzs[v1, :]
        xyz = (1.0 - t) * xyz0 + t * xyz1
        xyz_samples[i, :] = xyz
        if verbose:
            msg = 'i: %d    f: %.4f    s: %.4f    j: %d    t: %g    v0: %d    v1: %d' % (
                i, fi, si, j, t, v0, v1)
            print (msg)
    # Interpolation may have changed brightness, so rescale.
    # Note: Usually the interpolation will not change the brightness,
    # as the two colors ususally have a max=1 in the same rgb component,
    # and the interpolation does not change that.
    # But when the max rgb component is changing (i.e. green to blue),
    # then the interpolation will in fact change the brightness.
    # So this scaling does not affect most of the colors.
    scale_rgb_max (xyz_samples, brightness)
    return xyz_samples

#
# Routines to print the color values nicely. Should move elsewhere.
#

def print_color3(xyz):
    ''' Print a 3-element color value sensibly. '''
    sxyz = xyz[0] + xyz[1] + xyz[2]
    txt = '[% .8f  % .8f  % .8f]  sum: %.8f' % (
        xyz[0], xyz[1], xyz[2], sxyz)
    return txt


def print_colors(xyzs):
    ''' Print the array of colors sensibly. '''
    num_colors = xyzs.shape[0]
    for i in range(num_colors):
        xyz = xyzs[i, :]
        rgb = colormodels.rgb_from_xyz (xyz)
        msg = '%2d:  xyz: %s    rgb: %s' % (
            i, print_color3(xyz), print_color3(rgb))
        print (msg)

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
    with io.open (filename, 'w') as f:
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


# FIXME: Move to examples?
def write_pantone_reference_html (filename='pantone_references.html'):
    ''' Write an HTML document with some references to Pantone colors.

    These have nothing to do with pure spectral colors.
    '''
    def write_link (f, url, text):
        '''Write an html link.'''
        link = '<a href="%s">%s</a><br/>\n' % (url, text)
        f.write (link)

    with io.open (filename, 'w') as f:
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
    xyzs      = get_num_pure_colors (num_spect, 0, brightness)
    plots.xyz_patch_plot (xyzs, None, None,
        'Colors of pure spectral lines',
        'PureColors-Spectral', num_across=20)
    # With 100 purples.
    xyzs      = get_num_pure_colors (num_spect, 100, brightness)
    plots.xyz_patch_plot (xyzs, None, None,
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
        xyzs, None, None, title, filename, num_across=num_across)


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
# 'Shark fin' chromaticity plot.
#

def shark_fin_plot ():
    '''Draw the 'shark fin' CIE chromaticity diagram of the pure spectral lines (plus purples) in xy space.'''
    # get array of (approximate) colors for the boundary of the fin
    xyz_list = get_num_pure_colors (
        num_spect=2351, num_purple=200, brightness=1.0)

    # get normalized colors
    xy_list = xyz_list.copy()
    (num_colors, num_cols) = xy_list.shape
    for i in range (0, num_colors):
        colormodels.xyz_normalize (xy_list [i])
    # get phosphor colors and normalize
    red   = colormodels.color_converter.PhosphorRed
    green = colormodels.color_converter.PhosphorGreen
    blue  = colormodels.color_converter.PhosphorBlue
    white = colormodels.color_converter.PhosphorWhite
    colormodels.xyz_normalize (red)
    colormodels.xyz_normalize (green)
    colormodels.xyz_normalize (blue)
    colormodels.xyz_normalize (white)

    def get_direc_to_white (xyz):
        '''Get unit vector (xy plane) in direction of the white point.'''
        direc = white - xyz
        mag = math.hypot (direc [0], direc [1])
        if mag != 0.0:
            direc /= mag
        return (direc[0], direc[1])

    # plot
    pyplot.clf ()

    # draw best attempt at pure spectral colors on inner edge of shark fin
    s = 0.025     # distance in xy plane towards white point
    for i in range (0, len (xy_list)-1):
        x0 = xy_list [i][0]
        y0 = xy_list [i][1]
        x1 = xy_list [i+1][0]
        y1 = xy_list [i+1][1]
        # get unit vectors in direction of white point
        (dir_x0, dir_y0) = get_direc_to_white (xy_list [i])
        (dir_x1, dir_y1) = get_direc_to_white (xy_list [i+1])
        # polygon vertices
        poly_x = [x0, x1, x1 + s*dir_x1, x0 + s*dir_x0]
        poly_y = [y0, y1, y1 + s*dir_y1, y0 + s*dir_y0]
        # draw (using full color, not normalized value)
        color_string = colormodels.irgb_string_from_rgb (
            colormodels.rgb_from_xyz (xyz_list [i]))
        pyplot.fill (poly_x, poly_y, color_string, edgecolor=color_string)

    # fill in the monitor gamut with true colors
    def get_brightest_irgb_string (xyz):
        '''Convert the xyz color to rgb, scale to maximum displayable brightness, and convert to a string.'''
        rgb = colormodels.brightest_rgb_from_xyz (xyz)
        color_string = colormodels.irgb_string_from_rgb (rgb)
        return color_string

    def fill_gamut_slice (v0, v1, v2):
        '''Fill in a slice of the monitor gamut with the correct colors.'''
        #num_s, num_t = 10, 10
        #num_s, num_t = 25, 25
        num_s, num_t = 50, 50
        dv10 = v1 - v0
        dv21 = v2 - v1
        for i_s in range (num_s):
            s_a = float (i_s)   / float (num_s)
            s_b = float (i_s+1) / float (num_s)
            for i_t in range (num_t):
                t_a = float (i_t)   / float (num_t)
                t_b = float (i_t+1) / float (num_t)
                # vertex coords
                v_aa = v0 + t_a * (dv10 + s_a * dv21)
                v_ab = v0 + t_b * (dv10 + s_a * dv21)
                v_ba = v0 + t_a * (dv10 + s_b * dv21)
                v_bb = v0 + t_b * (dv10 + s_b * dv21)
                # poly coords
                poly_x = [v_aa [0], v_ba [0], v_bb [0], v_ab [0]]
                poly_y = [v_aa [1], v_ba [1], v_bb [1], v_ab [1]]
                # average color
                avg = 0.25 * (v_aa + v_ab + v_ba + v_bb)
                # convert to rgb and scale to maximum displayable brightness
                color_string = get_brightest_irgb_string (avg)
                pyplot.fill (poly_x, poly_y, color_string, edgecolor=color_string)
    fill_gamut_slice (white, blue,  green)
    fill_gamut_slice (white, green, red)
    fill_gamut_slice (white, red,   blue)

    # draw the curve of the xy values of the spectral lines and purples
    pyplot.plot (xy_list [:,0], xy_list [:,1], color='#808080', linewidth=3.0)
    # draw monitor gamut and white point
    pyplot.plot ([red  [0], green[0]], [red  [1], green[1]], 'o-', color='k')
    pyplot.plot ([green[0], blue [0]], [green[1], blue [1]], 'o-', color='k')
    pyplot.plot ([blue [0], red  [0]], [blue [1], red  [1]], 'o-', color='k')
    pyplot.plot ([white[0], white[0]], [white[1], white[1]], 'o-', color='k')
    # label phosphors
    dx = 0.01
    dy = 0.01
    pyplot.text (red   [0] + dx, red   [1], 'Red',   ha='left',   va='center')
    pyplot.text (green [0], green [1] + dy, 'Green', ha='center', va='bottom')
    pyplot.text (blue  [0] - dx, blue  [1], 'Blue',  ha='right',  va='center')
    pyplot.text (white [0], white [1] + dy, 'White', ha='center', va='bottom')
    # titles etc
    pyplot.axis ([0.0, 0.85, 0.0, 0.85])
    pyplot.xlabel (r'CIE $x$')
    pyplot.ylabel (r'CIE $y$')
    pyplot.title (r'CIE Chromaticity Diagram')
    filename = 'ChromaticityDiagram'
    # Save.
    plots.plot_save (filename)

#
# Main.
#

def figures ():
    ''' Draw plots of the pure colors and purples. '''
    # Plots.
    pure_colors_patch_plots()
    perceptually_equal_spaced_color_plots()
    shark_fin_plot()
    # Html documents.
    write_pantone_reference_html()
    write_visible_spectrum_html()


if __name__ == '__main__':
    figures()
