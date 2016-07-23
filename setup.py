#!/usr/bin/env python
# coding: utf-8

"""
setup.py file for AACGM_v2 SWIG bindings and wrapper functions
"""

from distutils.core import setup, Extension


aacgmlib_v2_module = Extension('_aacgmlib_v2',
                           sources=['aacgm/aacgmlib_v2.c', 'aacgm/aacgmlib_v2.i', 'aacgm/igrflib.c', 'aacgm/genmag.c'],
                           define_macros=[('DEBUG', '1')], undef_macros=['NDEBUG'],
                           )

setup (packages = ['aacgm'], 
       package_dir = {'aacgm': 'aacgm'},
       package_data = {'aacgm': ['coeffs/*']},
       name = 'aacgm',
       version = '0.2',
       author      = "Åsmund Steen Skjæveland",
       description = """Simple Python interface to aacgm_v2 module""",
       ext_modules = [aacgmlib_v2_module],
       #py_modules = ["aacgm"],
       )
