"""
Trendpy
-----

Trendpy is a trend filtering microframework
Trendpy implements L1 and L2 filtering methods solved by interior points or
MCMC methods

-----
Links
-----
* `website`:
* `documentation`:
"""
import os
import sys
from setuptools import setup, find_packages
from ConfigParser import RawConfigParser

def get_version_info(configuration_file="configuration.cfg"):
    """
    get_version_info
    ------------
    gets software version infos from
    """

    RawConfigParser().read(configuration_file)

    MAJOR = config.getint('version', 'major')
    MINOR = config.getint('version', 'minor')
    MICRO = config.getint('version', 'micro')

    ISRELEASED = config.getbool('release', 'is_release')

    VERSION = '%d.%d.%d' % (MAJOR, MINOR, MICRO)

    return VERSION, ISRELEASED

def write_version_py(filename="trendpy/version.py"):
    file_content= """
    # FILE CONTENT GENERATED FROM SETUP.PY
    #
    # To compare versions robustly, use `numpy.lib.NumpyVersion`
    short_version = '%(version)s'
    version = '%(version)s'
    full_version = '%(full_version)s'
    release = %(isrelease)s

    if not release:
        version = full_version
    """

def configuration(parent_package='',top_path=None):
    #from numpy.distutils.misc_util import Configuration

    #config = Configuration(None, parent_package, top_path)
    #config.set_options(ignore_setup_xxx_py=True,
    #                   assume_default_configuration=True,
    #                   delegate_options_to_subpackages=True,
    #                   quiet=True)

    #config.add_subpackage('numpy')

    #config.get_version('numpy/version.py') # sets config.version

    #return config

def setup_package():

    _version, _isRelease = get_version_info()

    write_version_py()

    setup(name='trendpy',
          version=str(_version),
          description='Trend Filtering Python MicroFramework',
          author='Rene-Jean Corneille',
          author_email='rene_jean.corneille@edu.escpeurope.eu',
          license='MIT',
          keywords = ['trend', 'finance', 'pandas', 'seaborn', 'filter', 'trading', 'stocks', 'equities', 'forex'],
          url = 'https://github.com/RonsenbergVI/trendpy',
          packages = find_packages(),
          zip_safe=False,
          include_package_data = True,
          platforms='any',
          install_requires = ['numpy',
                              'scipy',
                              'pandas',
                              'seaborn'],
          classifiers=[
            'Development Status :: 1 - Planning',
            'Environment :: Web Environment',
            'Intended Audience :: Financial and Insurance Industry',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
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
