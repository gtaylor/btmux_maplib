#!/usr/bin/env python

from distutils.core import setup

LONG_DESCRIPTION = (
    "btmux_maplib is a set of utility classes and functions for parsing, "
    "manipulating, and visualizing BattletechMUX .map files."
)

CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU General Public License (GPL)',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Games/Entertainment :: Multi-User Dungeons (MUD)',
    'Topic :: Software Development :: Libraries :: Python Modules'
]

KEYWORDS = 'btmux battletech mux battletechmux btech mud mush map mapping'

setup(
    name='btmux_maplib',
    version='1.0.0',
    description='BattletechMUX map utility library.',
    long_description=LONG_DESCRIPTION,
    author='Gregory Taylor',
    author_email='gtaylor@gc-taylor.com',
    url='https://github.com/gtaylor/btmux_maplib',
    packages=[
        'btmux_maplib',
        'btmux_maplib.img_generator',
        'btmux_maplib.map_generator',
        'btmux_maplib.map_parser',
        'btmux_maplib.map_exporters'],
    platforms='Platform Independent',
    requires=['Pillow', 'noise'],
    license='BSD',
    classifiers=CLASSIFIERS,
    keywords=KEYWORDS,
)
