# AACGM python wrapper

This is a Python wrapper for the Altitude Adjusted Corrected
Geomagnetic Coordinates (AACGM) C implementation found at
https://engineering.dartmouth.edu/superdarn/aacgm.html. License is
undetermined, please assume same as the C code found at above URL if
possible.  The C code and coefficient files (version 20140918) are
duplicated in this repository, but please check the source for more
updated versions.

## usage

There are wrapper functions in \_\_init\_\_.py to avoid the hassle of C
pointers. The main function is:

    *geo2aacgm(__datetime__, __lons__, __lats__, __alts__, Re = 6371.0, reversed = False)*

datetime: a Python datetime object.

lons, lats, alts: input coordinates. Units degrees/km. Can be Numpy
arrays or flat Python sequences of numbers.

The Re value does nothing, a Re of 6371.2 km is hardcoded in the C source.

Reversed: If False: convert geo -> aacgm. True: aacgm -> geo.

Return value: Arrays of converted (lon, lat). If input was numpy
arrays, returned arrays are numpy arrays of the same shape. If input
was Python sequence, flat lists will be returned.

There's also a function _aacgm2geo(…)_ which simply calls
_geo2aacgm(…)_ with the _reversed_ flag set.

Note that the C source uses (lat,lon) order. I prefer (lon,lat), so
that's what the wrapper code uses.

