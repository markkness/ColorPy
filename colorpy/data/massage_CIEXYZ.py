#!/usr/bin/env python
'''
massage_CIEXYZ.py - Convert CIE XYZ tables (1931 matching functions, D65)
into appropriate Python syntax to be inserted into ColorPy.

This was used in developing ColorPy.

References:

CVRL Color and Vision Database - http://cvrl.ioo.ucl.ac.uk/index.htm - (accessed 17 Sep 2008)
    Color and Vision Research Laboratories.
    Provides a set of data sets related to color vision.
    ColorPy uses the tables from this site for the 1931 CIE XYZ matching functions,
    and for Illuminant D65, both at 1 nm wavelength increments.
    
CIE Standards - http://cvrl.ioo.ucl.ac.uk/cie.htm - (accessed 17 Sep 2008)
    CIE standards as maintained by CVRL.
    The 1931 CIE XYZ and D65 tables that ColorPy uses were obtained from the following files, linked here:
        http://cvrl.ioo.ucl.ac.uk/database/data/cmfs/ciexyz31_1.txt
        http://cvrl.ioo.ucl.ac.uk/database/data/cie/Illuminantd65.txt

CIE International Commission on Illumination - http://www.cie.co.at/ - (accessed 17 Sep 2008)
    Official website of the CIE.
    There are tables of the standard functions (matching functions, illuminants) here:
        http://www.cie.co.at/main/freepubs.html
        http://www.cie.co.at/publ/abst/datatables15_2004/x2.txt
        http://www.cie.co.at/publ/abst/datatables15_2004/y2.txt
        http://www.cie.co.at/publ/abst/datatables15_2004/z2.txt
        http://www.cie.co.at/publ/abst/datatables15_2004/sid65.txt
    ColorPy does not use these specific files.

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

# Conversions for data (5 nm increments) from CIE website:
#   http://www.cie.co.at/main/freepubs.html
#   http://www.cie.co.at/publ/abst/datatables15_2004/x2.txt
#   http://www.cie.co.at/publ/abst/datatables15_2004/y2.txt
#   http://www.cie.co.at/publ/abst/datatables15_2004/z2.txt
# ColorPy is not using this data.

# filenames as downloaded
CIE_x = 'CIEXYZ_1931_x2.txt'
CIE_y = 'CIEXYZ_1931_y2.txt'
CIE_z = 'CIEXYZ_1931_z2.txt'

def read_CIE_file (filename):
    rtn = dict()
    f = open (filename, 'r')
    lines = f.readlines()
    f.close()
    # discard first and last lines
    lines = lines [1:-1]
    for i in lines:
        # fields are: wl (nm), intensity (with comma as decimal separator)
        fields = i.split()
        wl_nm = int (fields [0])
        intensity = fields[1].replace (',', '.')
        rtn [wl_nm] = intensity
    return rtn

def create_CIE_XYZ_1931_table_5nm ():
    '''Create the table, in (mostly) correct Python.'''
    msgs = []
    dict_x = read_CIE_file (CIE_x)
    dict_y = read_CIE_file (CIE_y)
    dict_z = read_CIE_file (CIE_z)
    # get keys
    keys = dict_x.keys()   # all should be the same
    keys.sort()
    msgs.append ('_CIEXYZ_1931_table = [\n')
    for i in xrange (0, len (keys)):
        ikey = keys [i]
        wl_nm = ikey
        x = dict_x [ikey]
        y = dict_y [ikey]
        z = dict_z [ikey]
        sep = ','
        if i == len (keys)-1:
            sep = ''
        msgs.append ('    [ %3d, %s, %s, %s ]%s\n' % (
            wl_nm, x, y, z, sep))
    msgs.append (']\n')
    return msgs

def doit_CIE_XYZ_1931_5nm ():
    '''Create tables from the official CIE data.'''
    msgs = create_CIE_XYZ_1931_table_5nm()
    for i in msgs:
        print i,
    f = open ('CIE_XYZ_1931_5nm.txt', 'w')
    f.writelines (msgs)
    f.close()

# Conversions for data (1 nm increments) from CVRL (Color and Vision Research Laboratories)
#   http://cvrl.ioo.ucl.ac.uk/database/data/cmfs/ciexyz31_1.txt
#   http://cvrl.ioo.ucl.ac.uk/database/data/cie/Illuminantd65.txt
# ColorPy IS using this data.

def create_CVRL_XYZ_1931_table_1nm ():
    msgs = []
    filename = 'ciexyz31_1.txt'
    f = open (filename, 'r')
    lines = f.readlines()
    f.close()
    msgs.append ('_CIEXYZ_1931_table = [\n')
    for i in xrange (0, len (lines)):
        iline = lines [i].rstrip()
        sep = ','
        if i == len (lines)-1:
            sep = ''
        msgs.append ('    [ %s ]%s\n' % (iline, sep))
    msgs.append (']\n')
    return msgs

def doit_CVRL_XYZ_1931_table_1nm ():
    msgs = create_CVRL_XYZ_1931_table_1nm()
    for i in msgs:
        print i,
    f = open ('CVRL_XYZ_1931_1nm.txt', 'w')
    f.writelines (msgs)
    f.close()

# Data for CIE Illuminant D65

def create_CVRL_D65_table_1nm ():
    msgs = []
    filename = 'Illuminantd65.txt'
    f = open (filename, 'r')
    lines = f.readlines()
    f.close()
    msgs.append ('_Illuminant_D65_table = [\n')
    for i in xrange (0, len (lines)):
        iline = lines [i].rstrip()
        sep = ','
        if i == len (lines)-1:
            sep = ''
        msgs.append ('    [ %s ]%s\n' % (iline, sep))
    msgs.append (']\n')
    return msgs

def doit_CVRL_D65_table_1nm ():
    msgs = create_CVRL_D65_table_1nm()
    for i in msgs:
        print i,
    f = open ('CVRL_D65_1nm.txt', 'w')
    f.writelines (msgs)
    f.close()

# Main - perform all of the conversions.
# The resulting source files are manually incorporated into the ColorPy code.

def main ():
    doit_CIE_XYZ_1931_5nm ()
    doit_CVRL_XYZ_1931_table_1nm ()
    doit_CVRL_D65_table_1nm ()
    
