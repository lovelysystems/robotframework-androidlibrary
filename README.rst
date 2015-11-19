robotframework-androidlibrary
-----------------------------

**robotframework-androidlibrary** is a `Robot Framework
<http://code.google.com/p/robotframework/>`_ test library for all your Android
automation needs.

It uses `Calabash Android <https://github.com/calabash/calabash-android>`_ to
communicate with your instrumented Android application similar to how `Selenium
WebDriver <http://seleniumhq.org/projects/webdriver/>`_ talks to your web
browser.

Deprecation Warning
+++++++++++++++++++

Lovely Systems does not not support this package anymore and 
do not have any follow up package in the same area. If anyone is
interested to continue our efforts and would like to 
manage the contributors in this open source project,
feel free to fork the package and give me a hint, so I can 
create a link to your fork! 

best regards, Manfred (Github: schwendinger, schwendinger at lovelysystems.com)

Installation
++++++++++++

To install, just fetch the latest version from PyPI::

    pip install --upgrade robotframework-androidlibrary


Usage
+++++

To use the library, import it at the beginning of a Robot Framework Test:

============  ================
  Setting          Value      
============  ================
Library       AndroidLibrary  
============  ================

Documentation
+++++++++++++

The keyword documentation can be found at <http://lovelysystems.github.com/robotframework-androidlibrary/>

Prepare your App
++++++++++++++++

robotframework-androidlibrary uses calabash-android underneath. To install calabash-android (we've only tested this with v0.3.2 yet), use the following command::

    gem install --version '= 0.4.18' calabash-android

To prepare your android app look at  <https://github.com/calabash/calabash-android#installation>


License
+++++++

robotframework is a port of the ruby-based `calabash-android` and therefore
licensed under the  `Eclipse Public License (EPL) v1.0
<http://www.eclipse.org/legal/epl-v10.html>`_

Development by `Lovely Systems GmbH <http://www.lovelysystems.com/>`_,
sponsored by `Axel Springer AG <http://www.axelspringer.de/>`_.
