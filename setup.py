#!/usr/bin/env python

"""
setup.py file for SWIG example
"""

from distutils.core import setup, Extension


aacgmlib_v2_module = Extension('aacgmlib_v2',
                           sources=['aacgmlib_v2/aacgmlib_v2.c', 'aacgmlib_v2/aacgmlib_v2.i'],
                           )

setup (packages = ['aacgmlib_v2'], 
       package_dir = {'aacgmlib_v2': 'aacgmlib_v2'},
       package_data = {'aacgmlib_v2': ['coeffs']},
#       name = 'aacgmlib_v2',
#       version = '0.1',
#       author      = "SWIG Docs",
#       description = """Simple Python interface to aacgm_v2 module""",
       ext_modules = [aacgmlib_v2_module],
#       py_modules = ["aacgmlib_v2"],
       )
