import aacgmlib_v2

def geo2aacgm(datetime, lons, lats, alts, Re = 6371.0, reversed = False):
    aacgmlib_v2.AACGM_v2_SetDateTime(datetime.year, datetime.month, datetime.day, datetime.hour, datetime.minute, datetime.second)

    # First try flattened Numpy arrays
    
    try:
        llons = lons.flatten()
        llats = lats.flatten()
        lalts = alts.flatten()

    except:
        # Fall back to generic sequences of numbers
