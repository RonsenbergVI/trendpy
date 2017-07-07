# -*- coding: utf-8 -*-

"""
trendpy
-----

trendpy is a trend filtering microframework
trendpy implements L1 filtering solved by MCMC methods

-----
Links
-----
* `website`:
* `documentation`:
"""

import os
import sys
from setuptools import setup, find_packages
from distutils.sysconfig import get_python_lib
from configparser import ConfigParser

config_file = os.path.join(os.path.dirname(__file__), 'setup.cfg')

if "install" in sys.argv:
    lib_paths = [get_python_lib()]
    if lib_paths[0].startswith("/usr/lib/"):
        lib_paths.append(get_python_lib(prefix="/usr/local"))
    for lib_path in lib_paths:
        existing_path = os.path.abspath(os.path.join(lib_path, "trendpy"))

def get_version_info():
	"""
	get_version_info
	------------
	gets software version infos from
	"""
	config=ConfigParser()
	config.read(config_file)
	MAJOR=config['version']['major']
	MINOR=config['version']['minor']
	MICRO=config['version']['micro']

	ISRELEASED = True
	
	VERSION = '%s.%s.%s' % (MAJOR, MINOR, MICRO)

	return VERSION, ISRELEASED

def write_version_py(filename="version.py"):
	"""
	write_version_py
	------------
	write software version infos in version.py file
	"""
	file_content = """ 
# FILE CONTENT GENERATED FROM SETUP.PY
short_version = '%(version)s'
version = '%(version)s'
full_version = '%(full_version)s'
release = %(isrelease)s

if not release:
	version = full_version
	"""
	filename = os.path.join(os.path.dirname(__file__), 'trendpy/%s' % filename)
	
	VERSION, ISRELEASED = get_version_info()

	_file = open(filename,'w+')

	try:
		_file.write(file_content % {'version': VERSION,
                       'full_version' : VERSION,
                       'isrelease': str(ISRELEASED)})
	finally:
		_file.close()

def setup_package():

    _version, _isReleased = get_version_info()

    write_version_py()

    setup(name = 'trendpy',
          version = str(_version),
          description = 'Trend Filtering Python Micro Framework',
          author = 'Rene-Jean Corneille',
          author_email = 'rene_jean.corneille@edu.escpeurope.eu',
          license = 'MIT',
          keywords = ['trend', 'finance', 'pandas', 'seaborn', 'filter', 'trading', 'stocks', 'equities', 'forex'],
          url = 'https://github.com/RonsenbergVI/trendpy',
          zip_safe = False,
          include_package_data = True,
          platforms = 'any',
		  packages=['trendpy'],
          install_requires = ['numpy',
                              'scipy',
                              'pandas',
                              'seaborn',
							  'tabulate'],
          classifiers = [
            'Development Status :: 2 - Pre-Alpha',
            'Environment :: Web Environment',
            'Intended Audience :: Financial and Insurance Industry',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Topic :: Scientific/Engineering :: Mathematics',
            'Topic :: Software Development :: Libraries :: Python Modules'
        ])

if __name__ == "__main__":
    setup_package()
