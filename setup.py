"""
trendpy
-----

trendpy is a trend filtering microframework
trendpy implements L1, L2 and Lp filtering solved by MCMC methods

-----
Links
-----
* `website`:
* `documentation`:
"""
import os
import sys
from setuptools import setup, find_packages

def get_version_info():
    """
    get_version_info
    ------------
    gets software version infos from
    """

    MAJOR = 0
    MINOR = 2
    MICRO = 6

    ISRELEASED = False

    VERSION = '%d.%d.%d' % (MAJOR, MINOR, MICRO)

    return VERSION, ISRELEASED

def write_version_py(filename="trendpy/version.py"):
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
    VERSION, ISRELEASED = get_version_info()

    _file = open(filename,"w")

    try:
        _file.write(file_content % {'version': VERSION,
                       'full_version' : VERSION,
                       'isrelease': str(ISRELEASED)})
    finally:
        _file.close()

#def configuration(parent_package='',top_path=None):
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

    _version, _isReleased = get_version_info()

    write_version_py()

    setup(name = 'trendpy',
          version = str(_version),
          description = 'Trend Filtering Python MicroFramework',
          author = 'Rene-Jean Corneille',
          author_email = 'rene_jean.corneille@edu.escpeurope.eu',
          license = 'MIT',
          keywords = ['trend', 'finance', 'pandas', 'seaborn', 'filter', 'trading', 'stocks', 'equities', 'forex'],
          url = 'https://github.com/RonsenbergVI/trendpy',
          zip_safe = False,
          include_package_data = True,
          platforms = 'any',
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
