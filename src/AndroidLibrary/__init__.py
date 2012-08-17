import json
import logging
import os
import subprocess
import requests

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
execfile(os.path.join(THIS_DIR, 'version.py'))

__version__ = VERSION

import robot
from robot.variables import GLOBAL_VARIABLES
from robot.api import logger

if hasattr(subprocess, 'check_output'):
    # Python >= 2.7
    from subprocess import check_output as execute
else:
    # Python < 2.7
    def execute(*popenargs, **kwargs):
        if 'stdout' in kwargs:
            raise ValueError('stdout argument not allowed, it will be overridden.')
        process = subprocess.Popen(stdout=subprocess.PIPE, *popenargs, **kwargs)
        output, unused_err = process.communicate()
        retcode = process.poll()
        if retcode:
            cmd = kwargs.get("args")
            if cmd is None:
                cmd = popenargs[0]
            raise subprocess.CalledProcessError(retcode, cmd, output=output)
        return output

    class CalledProcessError(Exception):
        def __init__(self, returncode, cmd, output=None):
            self.returncode = returncode
            self.cmd = cmd
            self.output = output
        def __str__(self):
            return "Command '%s' returned non-zero exit status %d" % (
                self.cmd, self.returncode)
    # overwrite CalledProcessError due to `output` keyword might be not available
    subprocess.CalledProcessError = CalledProcessError


class AndroidLibrary(object):

    ROBOT_LIBRARY_VERSION = VERSION
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self, ANDROID_HOME=None):
        '''
        Path to the Android SDK. Optional if the $ANDROID_HOME environment variable is set.
        '''

        if ANDROID_HOME is None:
            ANDROID_HOME = os.environ['ANDROID_HOME']

        self._ANDROID_HOME = ANDROID_HOME
        self._screenshot_index = 0

        sdk_path = lambda suffix: os.path.abspath(os.path.join(self._ANDROID_HOME, suffix))

        self._adb = sdk_path('platform-tools/adb')
        self._emulator = sdk_path('tools/emulator')

        assert os.path.exists(self._adb), "Couldn't find adb binary at %s" % self._adb
        assert os.path.exists(self._adb), "Couldn't find emulator binary at %s" % self._emulator

    def _execute(self, args, **kwargs):
        logging.debug("$> %s", ' '.join(args))
        output = execute(args, **kwargs)
        logging.debug(output)
        return output

    def start_emulator(self, avd_name, no_window=False):
        '''
        Starts the Android Emulator.

        `avd_name` Identifier of the Android Virtual Device, for valid values on your machine run "$ANDROID_HOME/tools/android list avd|grep Name`
        `no_window` Set to True to start the emulator without GUI, useful for headless environments.
        '''
        args = [self._emulator, '-avd', avd_name]

        if no_window:
            args.append('-no-window')

        logging.debug("$> %s", ' '.join(args))

        self._emulator_proc = subprocess.Popen(args)

    def stop_emulator(self):
        '''
        Halts a previously started Android Emulator.
        '''

        if not hasattr(self, '_emulator_proc'):
            logging.warn("Could not stop Android Emulator: It was not started.")
            return

        self._emulator_proc.terminate()
        self._emulator_proc.kill()
        self._emulator_proc.wait()

        self._emulator_proc = None

    def _execute_and_output_does_not_contain_error(self, *args):
        output = self._execute(*args)
        assert 'Error' not in output, output
        return output

    def uninstall_application(self, package_name):
        self._execute_and_output_does_not_contain_error([self._adb, "uninstall", package_name])

    def install_application(self, apk_file):
        '''
        Installs the given Android application package file (APK) on the emulator along with the test server.

        For instrumentation (and thus all remote keywords to work) both .apk
        files must be signed with the same key.

        `apk_file` Path the the application to install
        '''

        # TODO polling for package manager
        # http://code.google.com/p/android/issues/detail?id=842#c7

        self._execute_and_output_does_not_contain_error([self._adb, "install", "-r", apk_file])

    def wait_for_device(self):
        '''
        Wait for the device to become available
        '''
        self._execute([self._adb, 'wait-for-device'])

    def send_key(self, key_code):
        '''
        Send key event with the given key code. See http://developer.android.com/reference/android/view/KeyEvent.html for a list of available key codes.

        `key_code` The key code to send
        '''
        self._execute([self._adb, 'shell', 'input', 'keyevent', '%d' % key_code])

    def press_menu_button(self):
        '''
        Press the menu button ("KEYCODE_MENU"), same as '| Send Key | 82 |'
        '''
        self.send_key(82)

    def start_testserver(self, package_name):
        '''
        Start the remote test server inside the Android Application.

        `package_name` fully qualified name of the application to test

        '''
        self._execute([
          self._adb,
          "wait-for-device",
          "forward",
          "tcp:%d" % 34777,
          "tcp:7102"
        ])

        args = [
          self._adb,
          "wait-for-device",
          "shell",
          "am",
          "instrument",
          "-w",
          "-e",
          "class",
          "sh.calaba.instrumentationbackend.InstrumentationBackend",
          "%s.test/sh.calaba.instrumentationbackend.CalabashInstrumentationTestRunner" % package_name,
        ]

        self._host = 'localhost'
        self._port = 34777
        self._url = 'http://%s:%d' % (self._host, self._port)

        logging.debug("$> %s", ' '.join(args))
        self._testserver_proc = subprocess.Popen(args)


    def connect_to_testserver(self):
        '''
        Connect to the previously started test server inside the Android
        Application. Performs a handshake.
        '''

        response = requests.get(self._url + '/ping')

        assert response.status_code == 200, "InstrumentationBackend sent status %d, expected 200" % response.status_code
        assert response.text == 'pong', "InstrumentationBackend replied '%s', expected 'pong'" % response.text

    def _perform_action(self, command, *arguments):
        action = json.dumps({
          "command": command,
          "arguments": arguments,
        })

        logging.debug(">> %r", action)

        response = requests.post(self._url,
          data = { 'command': action },
          headers = { 'Content-Type': 'application/x-www-form-urlencoded' },
        )

        logging.debug("<< %r", response.text)
        assert response.status_code == 200, "InstrumentationBackend sent status %d, expected 200" % response.status_code
        return response.json

    # BEGIN: STOLEN FROM SELENIUM2LIBRARY

    def _get_log_dir(self):
        logfile = GLOBAL_VARIABLES['${LOG FILE}']
        if logfile != 'NONE':
            return os.path.dirname(logfile)
        return GLOBAL_VARIABLES['${OUTPUTDIR}']

    def _get_screenshot_paths(self, filename):
        if not filename:
            self._screenshot_index += 1
            filename = 'android-screenshot-%d.png' % self._screenshot_index
        else:
            filename = filename.replace('/', os.sep)
        logdir = self._get_log_dir()
        path = os.path.join(logdir, filename)
        link = robot.utils.get_link_path(path, logdir)
        return path, link

    # END: STOLEN FROM SELENIUM2LIBRARY

    def capture_screenshot(self, filename=None):
        '''
        Captures a screenshot of the current screen and embeds it in the test report

        Also works in headless environments.

        `filename` Location where the screenshot will be saved.
        '''

        path, link = self._get_screenshot_paths(filename)
        response = requests.get(self._url + '/screenshot')

        with open(path, 'w') as f:
            f.write(response.content)
            f.close()

        assert response.status_code == 200, "InstrumentationBackend sent status %d, expected 200" % response.status_code

        logger.info('</td></tr><tr><td colspan="3"><a href="%s">'
                   '<img src="%s"></a>' % (link, link), True, False)

    def screen_should_contain(self, text):
        '''
        Asserts that the current screen contains a given text

        `text` String that should be on the current screen
        '''
        result = self._perform_action("assert_text", text, True)
        assert result["success"] == True, "Screen does not contain text '%s': %s" % (
                text, result.get('message', 'No specific error message given'))

    def screen_should_not_contain(self, text):
        '''
        Asserts that the current screen does not contain a given text

        `text` String that should not be on the current screen
        '''
        result = self._perform_action("assert_text", text, False)
        assert result["success"] == True, "Screen does contain text '%s', but shouldn't have: %s" % (
                text, result.get('message', 'No specific error message given'))

    def touch_button(self, text):
        '''
        Touch an android.widget.Button

        `text` is the text the button that will be clicked contains
        '''
        result = self._perform_action("press_button_with_text", text)
        assert result["success"] == True, "GNAH! '%s': %s" % (
                text, result.get('message', 'No specific error message given'))

    def touch_text(self, text):
        '''
        Touch an android.widget.Button

        `text` is the text the button that will be clicked contains
        '''
        result = self._perform_action("click_on_text", text)
        assert result["success"] == True, "GNAH! '%s': %s" % (
                text, result.get('message', 'No specific error message given'))

    def scroll_up(self):
        '''
        Scroll up
        '''
        result = self._perform_action("scroll_up")
        assert result["success"] == True, "GNAH! '%s': %s" % (
                text, result.get('message', 'No specific error message given'))

    def scroll_down(self):
        '''
        Scroll down
        '''
        result = self._perform_action("scroll_down")
        assert result["success"] == True, "GNAH! '%s': %s" % (
                text, result.get('message', 'No specific error message given'))

    def set_webview_text(self, locator, value):
        '''
        Set the <input> field in the webview to the given value

        `locator` the locator to find the element to change. Valid locators are in the form of css=#element_id or xpath=//input[0]
        `value` the new value
        '''

        try:
            strategy, query = locator.split("=")
        except ValueError, e:
            strategy = "css"
            query = locator

        result = self._perform_action("set_text", strategy, query, value)

        assert result["success"] == True, "GNAH! '%r'" % result

    def touch_webview_element(self, locator):
        '''
        Touch an element in a webview

        `locator` locator for element to trigger a click event (only css locators are supported at the moment)
        '''

        try:
            strategy, query = locator.split("=")
        except ValueError, e:
            strategy = "css"
            query = locator

        assert strategy == "css"

        result = self._perform_action("touch", strategy, query)
        assert result["success"] == True, "GNAH! '%r'" % result

