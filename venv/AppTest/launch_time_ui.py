import csv
import os
import time
import re
import commands
import string
from appium import webdriver
import logging
import datetime

logging.basicConfig(level=logging.INFO)
apk_path = os.path.join(os.getcwd(), 'lite.apk')


class Browser(object):
    platform_name = 'Android'
    platform_version = string.strip(commands.getoutput('adb shell getprop ro.build.version.release'))
    devices_name = string.strip(commands.getoutput('adb shell getprop ro.serialno'))
    phone_name = string.strip(commands.getoutput('adb shell getprop ro.build.id'))

    def __init__(self):
        self.desired_caps = {}
        self.desired_caps['platformName'] = 'Android'
        self.desired_caps['platformVersion'] = '6.0'
        self.desired_caps['deviceName'] = '80QBCP9224W2'
        self.desired_caps['app'] = apk_path
        self.desired_caps['appPackage'] = 'com.qihoo.contents'
        self.desired_caps['appActivity'] = 'com.qihoo.contents.launcher.LauncherActivity'
        self.desired_caps['noReset'] = True
        self.desired_caps['unicodeKeyboard'] = False
        self.desired_caps['resetKeyboard'] = False
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', self.desired_caps)
        self.driver.implicitly_wait(600)

    def install_app(self):
        cmd = 'adb install ' + apk_path
        os.popen(cmd)
        logging.info('install app done')

    def uninstall_app(self):
        cmd = 'adb uninstall com.qihoo.contents'
        os.popen(cmd)
        logging.info('uninstall app done')

    def is_app_installed(self):
        cmd = 'adb shell pm list packages'
        output = os.popen(cmd)
        app_status = False
        for line in output.readlines():
            if 'com.qihoo.contents' in line:
                app_status = True
        return app_status

    def test_launch_time(self):
        start_time = self.get_cur_time()
        # logging.info('StartTime is ' + string(start_time))
        ele = self.driver.find_element_by_id('com.qihoo.contents:id/home_top_user')
        if ele.is_displayed():
            end_time = self.get_cur_time()
            # logging.info("Endtime is " + string(end_time))
        launch_time = end_time - start_time
        return launch_time

    def get_cur_time(self):
        return datetime.datetime.strptime(str(datetime.datetime.now()), '%Y-%m-%d %H:%M:%S.%f')


class Controller(object):
    def __init__(self, count):
        self.browser = Browser()
        self.count = count
        self.data = [{'#', 'launch_time'}]

    def run(self):
        while self.count > 0:
            self.browser.test_launch_time()
            time.time(3)
            self.count = self.count - 1

    def save_data(self):
        csv_file = file(self.browser.phone_name + '_launchTime_' + cur_time() + '.csv', 'wb')
        w = csv.writer(csv_file)
        w.writerows(self.data)
        csv_file.close()

    def tearDown(self):
        os.popen('adb uninstall com.qihoo.contents')
        self.browser.driver.quit()


if __name__ == "__main__":
    logging.info(apk_path)
    controller = Controller(10)
    controller.run()
    controller.save_data()
