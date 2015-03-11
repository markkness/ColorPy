#!/usr/bin/env python
'''
setup.py - Setup script to install the ColorPy package.

To install the ColorPy package:
From the directory in which the ColorPy distribution was unpacked, run:

python setup.py install

You should now be able to say 'import colorpy' in your programs and use the package.

Creating the distribution:

python setup.py sdist --formats=zip
python setup.py sdist --formats=gztar
python setup.py bdist_wininst
'''
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from distutils.core import setup

data_files = [
    'README.txt',
    'COPYING.txt',
    'COPYING.LESSER.txt',
    'license.txt',
    'ColorPy.html',
]

long_description = '''
ColorPy is a Python package to convert physical descriptions of light -
    spectra of light intensity vs. wavelength - into RGB colors that can
    be drawn on a computer screen.
    It provides a nice set of attractive plots that you can make of such
    spectra, and some other color related functions as well.
'''

# FIXME: There may be some Programming Language description that should
# indicate Python 2 and 3.  See: https://docs.python.org/3/howto/pyporting.html
setup (
    name='colorpy',
    version='0.1.0',
    description='Color calculations with physical descriptions of light spectra',
    long_description=long_description,
    author='Mark Kness',
    author_email='mkness@alumni.utexas.net',
    url='http://markkness.net/colorpy/',
    license='GNU Lesser GPL Version 3',
    package_dir={'colorpy': ''},
    packages=['colorpy'],
    package_data={'colorpy': data_files},
)
