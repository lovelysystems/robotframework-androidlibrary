#!/usr/bin/env python

from os.path import join, dirname

execfile(join(dirname(__file__), 'src', 'AndroidLibrary', 'version.py'))

from distutils.core import setup

CLASSIFIERS = """
Programming Language :: Python
Topic :: Software Development :: Testing
"""[1:-1]

long_description=open(join(dirname(__file__), 'README.rst',)).read()

setup(
  name             = 'robotframework-androidlibrary',
  version          = VERSION,
  description      = 'Robot Framework Automation Library for Android',
  long_description = long_description,
  author           = "Lovely Systems GmbH",
  author_email     = "office@lovelysystems.com",
  url              = 'https://github.com/lovelysystems/robotframework-androidlibrary',
  license          = 'EPL',
  keywords         = 'robotframework testing testautomation android calabash robotium',
  platforms        = 'any',
  zip_safe         = False,
  classifiers      = CLASSIFIERS.splitlines(),
  package_dir      = {'' : 'src'},
  install_requires = ['robotframework', 'requests'],
  packages         = ['AndroidLibrary'],
  package_data     = {'AndroidLibrary': ['src/AndroidLibrary/*.jar']}
)
