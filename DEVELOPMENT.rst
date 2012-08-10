========================================
Hacking on robotframework-androidlibrary
========================================

This is a guide on how to work on robotframework-androidlibrary itself, that is -
if you want to use the library to test your own application, please consult
README.rst


Prerequisites
=============

- Install the `Android SDK <http://developer.android.com/sdk/index.html>`_
- Install calabash-android v0.1.0::

    gem install --version '= 0.1.0' calabash-android

- Create a debug keystore::

    $ANDROID_SDK/tools/android create project -n dummy_project_to_create_debug_keystore -t 8 -p dummy_project_to_create_debug_keystore -k what.ever -a whatever
    cd dummy_project_to_create_debug_keystore
    ant debug 
    cd -

Development environment
=======================

To get started, use the following commands::

    git clone https://github.com/lovelysystems/robotframework-androidlibrary
    cd robotframework-androidlibrary/
    python bootstrap.py --distribute
    bin/buildout

Running tests
=============

The library itself is tested using robotframework, to run the tests type::
 
   export ANDROID_HOME=path/to/android/sdk
   bin/robotframework tests/

Optionally, the following parameters can be specified:

**Highest debug level**::

  -L TRACE

**Show the android emulator when running tests**::

  -v HEADLESS:False

