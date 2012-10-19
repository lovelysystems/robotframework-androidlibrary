robotframework-androidlibrary
-----------------------------

**robotframework-androidlibrary** is a `Robot Framework
<http://code.google.com/p/robotframework/>`_ test library for all your Android
automation needs.

It uses `Calabash Android <https://github.com/calabash/calabash-android>`_ to
communicate with your instrumented Android application similar to how `Selenium
WebDriver <http://seleniumhq.org/projects/webdriver/>`_ talks to your web
browser.


Installation
++++++++++++

To install, just fetch the latest version from PyPI::

    pip install --upgrade robotframework-androidlibrary

Prepare your App
++++++++++++++++

robotframework-androidlibrary uses calabash-android underneath. To install calabash-android (we've only tested this with v0.3.2 yet), use the following command::

    gem install --version '= 0.3.2' calabash-android

To prepare your android app look at  <https://github.com/calabash/calabash-android#installation>


License
+++++++

robotframework is a port of the ruby-based `calabash-android` and therefore
licensed under the  `Eclipse Public License (EPL) v1.0
<http://www.eclipse.org/legal/epl-v10.html>`_

Development by `Lovely Systems GmbH <http://www.lovelysystems.com/>`_,
sponsored by `Axel Springer AG <http://www.axelspringer.de/>`_.

Documentation
+++++++++++++

The keyword documentation could be found at <http://lovelysystems.github.com/robotframework-androidlibrary/>
