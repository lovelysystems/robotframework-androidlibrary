robotframework-androidlibrary
-----------------------------

**robotframework-androidlibrary** is a `Robot Framework
<http://code.google.com/p/robotframework/>`_ test library for all your Android
automation needs.

It uses `Calabash's Android test server
<https://github.com/calabash/calabash-ios-server>`_ to communicate with your
instrumented Android application similar to how `Selenium WebDriver
<http://seleniumhq.org/projects/webdriver/>`_ talks to your web browser.


Installation
++++++++++++

To install, just fetch the latest version from PyPI::

    pip install --upgrade robotframework-androidlibrary

Prepare your App
++++++++++++++++

robotframework-androidlibrary uses calabash-android underneath. To install calabash-android (we've only tested this with v0.2.17 yet), use the following command::

    gem install --version '= 0.2.17' calabash-android

To prepare your android app look at  <https://github.com/calabash/calabash-android#installation>


License
+++++++

robotframework is a port of the ruby-based `calabash-android` and therefore
licensed under the  `Eclipse Public License (EPL) v1.0
<http://www.eclipse.org/legal/epl-v10.html>`_

Documentation
+++++++++++++

The keyword documentation could be found at <http://lovelysystems.github.com/robotframework-androidlibrary/>
