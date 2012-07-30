import logging
import os
import subprocess
import json
import telnetlib
import os

import robot
from robot.variables import GLOBAL_VARIABLES
from robot.api import logger

class AndroidLibrary(object):

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self, android_sdk_path):

        self._android_sdk_path = android_sdk_path
        self._screenshot_index = 0

        sdk_path = lambda suffix: os.path.abspath(os.path.join(self._android_sdk_path, suffix))

        self._adb = sdk_path('platform-tools/adb')
        self._emulator = sdk_path('tools/emulator')

        assert os.path.exists(self._adb), "Couldn't find adb binary at %s" % self._adb
        assert os.path.exists(self._adb), "Couldn't find emulator binary at %s" % self._emulator

    def start_android_emulator(self, avd_name, no_window=False):
        cmd = [self._emulator, '-avd', avd_name]

        if no_window:
            cmd.append('-no-window')

        self._emulator_proc = subprocess.Popen(cmd)

    def stop_android_emulator(self):
        self._emulator_proc.terminate()
        self._emulator_proc.kill()
        self._emulator_proc.wait()

    def set_package_name(self, package_name):
        self._package_name = package_name

    def install_apk(self, test_apk_path, app_apk_path):
        execute = subprocess.check_output

        execute([self._adb, "uninstall", "%s.test" % self._package_name])
        execute([self._adb, "uninstall", self._package_name])
        execute([self._adb, "install", "-r", test_apk_path])
        execute([self._adb, "install", "-r", app_apk_path])

    def wait_for_device(self):
        subprocess.check_output([self._adb, 'wait-for-device'])

    def send_key_event(self, key_code):
        subprocess.check_output([self._adb, 'shell', 'input', 'keyevent', '%d' % key_code])

    def press_menu_button(self):
        self.send_key_event(82)

    def start_testserver(self, port=34777):
        execute = subprocess.check_output

        subprocess.check_output([
          self._adb,
          "forward",
          "tcp:%d" % port,
          "tcp:7101"
        ])

        self._testserver_proc = subprocess.Popen([
          self._adb,
          "shell",
          "am",
          "instrument",
          "-w",
          "-e",
          "class",
          "sh.calaba.instrumentationbackend.InstrumentationBackend",
          "%s.test/sh.calaba.instrumentationbackend.CalabashInstrumentationTestRunner" % self._package_name,
        ])


    def connect_to_testserver(self, host='localhost', port=34777):
        self._connection = telnetlib.Telnet(host, port)

        # secret calabash handshake
        self._connection.write("Ping!\n")
        self._connection.read_until("Pong!\n")

    def _perform_action(self, command, *arguments):
        action = json.dumps({
          "command": command,
          "arguments": arguments,
        }) + '\n'
        logging.debug(">> %r", action)
        self._connection.write(action)
        result = self._connection.read_until('\n')
        logging.debug("<< %r", result)
        return json.loads(result)

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
        path, link = self._get_screenshot_paths(filename)

        jar = os.path.join(os.path.dirname(__file__), 'screenShotTaker.jar')

        screenshot_taking_proc = subprocess.Popen(
          ["java", "-jar", jar, path],
          env={
            "ANDROID_HOME": self._android_sdk_path
          }
        )

        logger.info('</td></tr><tr><td colspan="3"><a href="%s">'
                   '<img src="%s"></a>' % (link, link), True, False)

    def screen_contains_text(self, text):
        result = self._perform_action("wait_for_text", text)
        assert result["success"] == True, "Screen does not contain text '%s': %s" % (
                text, result.get('message', 'No specific error message given'))

