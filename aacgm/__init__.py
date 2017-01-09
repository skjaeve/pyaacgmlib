from __future__ import print_function

from . import aacgmlib_v2 # Relative-path import, now works in Python3
import os

"""
Copied from C functions:
;     Input Arguments:  
;       in_lat        - latitude in degrees
;       in_lon        - longitude in degrees
;       height        - height above Earth in km
;       code          - bitwise code for passing options into converter
;                       G2A         - geographic (geodetic) to AACGM-v2
;                       A2G         - AACGM-v2 to geographic (geodetic)
;                       TRACE       - use field-line tracing, not coefficients
;                       ALLOWTRACE  - use trace only above 2000 km
;                       BADIDEA     - use coefficients above 2000 km
;       order         - integer order of spherical harmonic expansion
"""

## Set ENVIRON variable to point at AACGM coefficients
# This is not a pretty cludge, but this is how the C code wants it
os.environ['AACGM_v2_DAT_PREFIX'] = os.path.join(__path__[0], 'coeffs', 'aacgm_coeffs-12-')


# Bitwise flags for sending options to C functions:
G2A        =  0
A2G        =  1
TRACE      =  2
ALLOWTRACE =  4
BADIDEA    =  8
GEOCENTRIC = 16

"""
#define G2A        0    /* convert geographic (geodetic) to AACGM-v2 coords  */
#define A2G        1    /* convert AACGM-v2 to geographic (geodetic) coords  */
#define TRACE      2    /* use field-line tracing to compute coordinates     */
#define ALLOWTRACE 4    /* if height is >2000 km use tracing, else use coefs */
#define BADIDEA    8    /* use coefficients above 2000 km; Terrible idea!!   */
#define GEOCENTRIC 16   /* assume inputs are geocentric with sphere RE       */
"""
def setNow():
    """Sets the AACGM library internal datetime to current time (UTC). Not
    sure if it handles timezones or assumes the computer clock to be in
    UTC."""
    
    return aacgmlib_v2.AACGM_v2_SetNow()

def setDateTime(datetime):

    """Sets AACGM library internal datetime to that of Datetime object. All
    times are assumed to be in UTC regardless of what the Datetime
    timezone info is, if any."""

    return aacgmlib_v2.AACGM_v2_SetDateTime(datetime.year, datetime.month, datetime.day, datetime.hour, datetime.minute, datetime.second)

def getDateTime():
    """Retrieves AACGM library internal datetime as a TZ-unaware Datetime
    object. Time returned is in UTC regardless of what the Datetime
    timezone info is, if any.
    """

    import datetime

    # Function pointer, for simpler-to-read code
    # Gets the value from a C pointer
    INT = aacgmlib_v2.intp_value

    # C pointers
    yearP = aacgmlib_v2.new_intp()
    monthP = aacgmlib_v2.new_intp()
    dayP = aacgmlib_v2.new_intp()
    hourP = aacgmlib_v2.new_intp()
    minuteP = aacgmlib_v2.new_intp()
    secondP = aacgmlib_v2.new_intp()
    daynoP = aacgmlib_v2.new_intp()    

    status = aacgmlib_v2.AACGM_v2_GetDateTime(yearP, monthP, dayP, hourP, minuteP, secondP, daynoP)
    
    try:
        dt = datetime.datetime(INT(yearP), INT(monthP), INT(dayP), INT(hourP), INT(minuteP), INT(secondP))
    except:
        print('NOTICE: Invalid datetime returned - AACGM datetime not set')
        dt = (INT(yearP), INT(monthP), INT(dayP), INT(hourP), INT(minuteP), INT(secondP))

    return (status, dt, INT(daynoP))

def geo2aacgm(datetime, lons, lats, alts, Re = 6371.2, reversed = False, FLAG=None):
    """Call AAGCM library method to compute AACGM coordinates from GEO or
    reversed. Must supply a datetime object to set the AACGM library
    internal time. Data can be in flat sequence form or Numpy arrays.

    returns: lon, lat arrays of same shape as input input is numpy arrays,
    otherwise Python lists."""

    # Initialise library datetime
    aacgmlib_v2.AACGM_v2_SetDateTime(datetime.year, datetime.month,
                                     datetime.day, datetime.hour,
                                     datetime.minute, datetime.second)

    # Direction of coordinate conversion. 0 = geo -> aacgm, 1 = aacgm -> geo
    # Definition text copied near top of file
    if reversed:
        DIRECTION_FLAG = A2G
    else:
        DIRECTION_FLAG = G2A
    if FLAG:
        DIRECTION_FLAG = FLAG

    try:
        import numpy
        # First assume the data is flatten-able Numpy arrays
        llons = numpy.asarray(lons).flatten()
        llats = numpy.asarray(lats).flatten()
        lalts = numpy.asarray(alts).flatten()

        # Output arrays, flattened (to be reshaped after computation)
        result_llons = numpy.zeros(llons.shape)
        result_llats = numpy.zeros(llats.shape)
        
    except:
        # Fall back to generic sequences of numbers
        llons = lons
        llats = lats
        lalts = alts

        # Output lists
        result_llons = [0] * len(llons)
        result_llats = [0] * len(llats)


    # C pointers: coordinate coefficients
    lat_out = aacgmlib_v2.new_doublep()
    lon_out = aacgmlib_v2.new_doublep()
    r = aacgmlib_v2.new_doublep()
    # The variable r is included as a return value but will always be 1.0.
    
    for i in range(len(llons)):
        status = aacgmlib_v2.AACGM_v2_Convert(float(llats[i]), float(llons[i]), float(lalts[i]), lat_out, lon_out, r, DIRECTION_FLAG)
        
        if status == 0:
            result_llons[i] = aacgmlib_v2.doublep_value(lon_out)
            result_llats[i] = aacgmlib_v2.doublep_value(lat_out)
        else:
            print("ERROR: Status %d" % status)
            result_llons[i] = float('nan')
            result_llats[i] = float('nan')

    try:
        return numpy.reshape(result_llons, lons.shape), numpy.reshape(result_llats, lats.shape)
    except:
        return result_llons, result_llats

def aacgm2geo(datetime, lons, lats, alts, Re = 6371.2):
    """Convenience function to call geo2aacgm() with reversed flag set,
    for slightly more readable code."""

    return geo2aacgm(datetime, lons, lats, alts, Re, reversed=True)


def map_geo_to_alt(datetime, lons, lats, alts, map_to_alts, Re = 6371.2):
    """Calls geo2aacgm() and aacgm2geo() to map geographic coordinates to new altitudes along magnetic field."""

    import numpy

    lons = numpy.asarray(lons)
    lats = numpy.asarray(lats)
    alts = numpy.asarray(alts)
    map_to_alts = numpy.asarray(map_to_alts)

    if map_to_alts.size == 1:
        map_to_alts = numpy.zeros(lons.shape) + map_to_alts

    mlons, mlats = geo2aacgm(datetime, lons, lats, alts)
    return aacgm2geo(datetime, mlons, mlats, map_to_alts)

def mlon2mlt(datetime, mlons):
    """Computes magnetic local time (MLT) from datetime, MLON. MLAT has little effect (shepherd, 2014; shepherd, 2016)"""

    import numpy as n

    setDateTime(datetime)


    if not isinstance(mlons, (n.ndarray, list, tuple)):
        mlon = [mlons]

    out_mlt = n.zeros(len(mlons))
    for idx, mlon in enumerate(mlons):
        out_mlt[idx] = aacgmlib_v2.MLTConvert_v2(datetime.year, datetime.month, datetime.day, datetime.hour, datetime.minute, datetime.second, mlon)
    return out_mlt