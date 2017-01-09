# AACGM python wrapper

This is a Python wrapper for the Altitude Adjusted Corrected Geomagnetic
Coordinates (AACGM) v2 C implementation found at
https://engineering.dartmouth.edu/superdarn/aacgm.html. License is assumed to be GPL v3; se below.
The C code and coefficient files (version 20160505 code/20150207 coeffs) are
duplicated in this repository, but please check the source for more updated
versions.

The wrappers should work in Python 2.7 and Python 3.4 and 3.5.


## Installation

Install SWIG if you don't already have it, and the headers for the
Python version you're compiling for, for example (Ubuntu/Debian)

    sudo aptitude install swig python-dev python3-dev

then install the library:

    python setup.py install --user

Or if you're in a virtualenv:

    python setup.py install

Installation via `pip install . --user` doesn't work, because it doesn't
actually compile anything.

## Usage

There are wrapper functions in \_\_init\_\_.py to avoid the hassle of C
pointers. The main function is:

    geo2aacgm(datetime, lons, lats, alts, Re = 6371.0, reversed = False)

datetime: a Python datetime object.

lons, lats, alts: input coordinates. Units degrees/km. Can be Numpy
arrays or flat Python sequences of numbers.

The Re value does nothing, a Re of 6371.2 km is hardcoded in the C source.

Reversed: If False: convert geo -> aacgm. True: aacgm -> geo.

Return value: Arrays of converted (lon, lat). If input was numpy
arrays, returned arrays are numpy arrays of the same shape. If input
was Python sequence, flat lists will be returned.

There's also a convenience function `aacgm2geo(…)` which simply calls
`geo2aacgm(…)` with the _reversed_ flag set.

`mlon2mlt(datetime, mlons)` computes MLT from MLON and datetime. MLON can be a
single float or a sequence of floats. Only one datetime may be specified. Uses
the MLT algorithm in the C code, and may disagree with other MLT calculators'
results. Apparently MLT isn't as well-defined and agreed upon as we like to
pretend.

Note that the C source uses (lat, lon) order of function parameters. I prefer
(lon, lat), so that's what the wrapper code uses.

Other functions: _setNow()_, _setDateTime(**datetime**)_,
_getDateTime()_ exist but aren't really needed, unless you're going to
bypass the wrapper functions and use the C functions directly.




# License

Short story: GPL v3.

Long story: Version 2.3 of the AACGMv2 C code includes the AstAlg library,
which is licensed under GPL v2 or later. The magnetic local time (MLT) code
uses the AstAlg code. Since I wrap the MLT functions, my code is automatically
GPL. Older versions of the AACGMv2 code (without MLT) didn't have an explicit
license, so I simply assume that it had an implicit GPL-compatible license.
The time.c/h files refer to a different license file which I haven't been able
to find.
