*** ReadMe for ColorPy 0.1.0. ***

ColorPy is a Python package that can convert physical descriptions of light -
    spectra of light intensity vs. wavelength - into RGB colors that can
    be drawn on a computer screen.
    It provides a nice set of attractive plots that you can make of such
    spectra, and some other color related functions as well.

Unpacking the Distribution:

The instruction depend on if you are using Windows or Linux.
If you are using Windows, you can use the binary distribution executable,
and all you need to do is run that.  Otherwise...

Windows -

Unzip the .zip distribution.  Recent versions of Windows (XP or later),
will unpack the directory automatically, you can simply enter the 
directory in Windows Explorer.  You will probably need to copy the
uncompressed files into another directory.

Linux -

The distribution is a compressed tar archive, uncompress it as follows:

	gunzip -c colorpy-0.1.0.tar.gz | tar xf -
	cd colorpy-0.1.0

Installation:

To install ColorPy from the source distributions (.zip on Windows,
or .tar.gz on Linux) you must first unpack the distribution.

Then, from the directory in which the files are unpacked, run:

	python setup.py install

It is possible that you may need to supply a path to the Python executable.
You also probably will need administrator privileges to do this.

This should complete the installation.

If you are installing from the Windows binary distribution (.win32.exe),
then all you need to do is run that executable and follow the prompts.

After installation, I recommend that you run the test cases.
In the Python interpreter, do:

	import colorpy.test
	colorpy.test.test()

This should run several test cases.
As an additional (and more interesting) test, create the sample figures:

	import colorpy.figures
	colorpy.figures.figures()

This should create a number of plot files (typically .png files) in
the current directory.  These will include all of the plots in the HTML
documentation, as well as several others.

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
