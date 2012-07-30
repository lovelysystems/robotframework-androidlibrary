#!/usr/bin/env python

from distutils.core import setup

CLASSIFIERS = """
Programming Language :: Python
Topic :: Software Development :: Testing
"""[1:-1]

from os.path import join, dirname
long_description=open(join(dirname(__file__), 'README.rst',)).read()

setup(
  name             = 'robotframework-androidlibrary',
  version          = "0.0.1",
  description      = 'Robot Framework Automation Library for Android',
  long_description = long_description,
  author           = '',
  author_email     = '',
  url              = 'https://github.com/lovelysystems/robotframework-androidlibrary',
  license          = 'EPL',
  keywords         = 'robotframework testing testautomation android calabash robotium',
  platforms        = 'any',
  zip_safe         = False,
  classifiers      = CLASSIFIERS.splitlines(),
  package_dir      = {'' : 'src'},
  install_requires = ['robotframework'],
  packages         = ['AndroidLibrary']
)
