from __future__ import print_function

from . import aacgmlib_v2 # Relative-path import, now works in Python3
import os

## Set ENVIRON variable to point at AACGM coefficients
# This is not a pretty cludge, but this is how the C code wants it
os.environ['AACGM_v2_DAT_PREFIX'] = os.path.join(__path__[0], 'coeffs', 'aacgm_coeffs-11-')

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
    
    dt = datetime.datetime(INT(yearP), INT(monthP), INT(dayP), INT(hourP), INT(minuteP), INT(secondP))

    return (status, dt, INT(daynoP))

def geo2aacgm(datetime, lons, lats, alts, Re = 6371.0, reversed = False):
    """Call AAGCM library method to compute AACGM coordinates from GEO or
    reversed. Must supply a datetime object to set the AACGM library
    internal time. Data can be in flat sequence form or Numpy arrays."""

    # Initialise library datetime
    aacgmlib_v2.AACGM_v2_SetDateTime(datetime.year, datetime.month,
                                     datetime.day, datetime.hour,
                                     datetime.minute, datetime.second)

    # Direction of coordinate conversion. 0 = geo -> aacgm, 1 = aacgm -> geo
    if reversed:
        DIRECTION_FLAG = 1
    else:
        DIRECTION_FLAG = 0

    try:
        import numpy
        # First assume the data is flatten-able Numpy arrays
        llons = lons.flatten()
        llats = lats.flatten()
        lalts = alts.flatten()

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
        status = aacgmlib_v2.AACGM_v2_Convert(llats[i], llons[i], lalts[i], lat_out, lon_out, r, DIRECTION_FLAG)
        
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

def aacgm2geo(datetime, lons, lats, alts, Re = 6371.0):
    """Convenience function to call geo2aacgm() with reversed flag set,
    for slightly more readable code."""

    return geo2aacgm(datetime, lons, lats, alts, Re, reversed=True)
