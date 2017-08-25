
# -*- coding: utf-8 -*-

# release.py

# MIT License

# Copyright (c) 2017 Rene Jean Corneille

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
Release script widely inspired from flask_mail
"""

import sys
import os
import re

from datetime import datetime, date
from subprocess import Popen, PIPE
from configparser import ConfigParser

def installed_list():
	libs_list = Popen(['pip', 'freeze'], stdout=PIPE).communicate()[0].decode("utf-8").split("\r\n")
	return {str(lib.split("==")[0]).lower() : lib.split("==")[1] for lib in libs_list[:-1]}

def is_installed(lib):
	return lib in installed_list().keys()

def get_changes():
    with open('CHANGES','r+') as file:
        for line in iter(file):
            match = re.search('Version\s+(.*)', line.strip())

            if match is None:
                continue

            version = match.group(1).strip()

            if next(file).count('-') != len(line.strip()):
                print_error('Invalid hyphen count below version line: %s', line.strip())

            while 1:
                released = next(file).strip()
                if released:
                    break

            match = re.search(r'Release day: (\w+\s+\d+\w+\s+\d+)', released)

            if match is None:
                print_error('Could not find release date in version %s' % version)

            release_day = get_date(match.group(1).strip())

            return version, release_day

def get_date(string_date):
    string_date = re.compile(r'(\d+)(st|nd|rd|th)').sub(r'\1', string_date)
    return datetime.strptime(string_date, '%B %d %Y')

def print_error(message, *args):
    print('Error: %s' % (message % args),file=sys.stderr)
    sys.exit(1)

def print_info(message, *args):
	print(message % args,file=sys.stderr)

def get_version(version_string):
	try:
		parts = list(map(int, version.split('.')))
		MAJOR=parts[0]
		MINOR=parts[1]
		MICRO=parts[2]
	except ValueError:
		print_error('Current version is not numeric')
	return MAJOR, MINOR, MICRO

def write_new_version(major,minor,micro,release=""):
	filename = 'setup.cfg'
	config = ConfigParser()
	config.read(filename)
	config['version']['major'] = major
	config['version']['minor'] = minor
	config['version']['micro'] = micro
	with open(filename, 'w') as configfile:
		config.write(configfile)
		configfile.close()
	print_info("Current version is now: %s.%s.%s" % (major, minor, micro))

def build_for_release():

    Popen([sys.executable, 'setup.py', 'sdist', 'build_sphinx', '-s', './docs', 'upload', 'register']).wait()
	Popen([sys.executable, 'setup.py', 'sdist', '--formats=gztar,zip']).wait()

if __name__ == '__main__':
	version, day = get_changes()
	major,minor,micro = get_version(version)
	write_new_version(str(major),str(minor),str(micro))
	build_for_release()
