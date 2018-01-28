# /usr/bin/python
# encoding:utf-8
import csv
import os
import time
import re


class Browser(object):
    def launch_browser(self):
        cmd = 'adb shell am start -W -n com.qihoo.contents/.launcher.LauncherActivity'
        output = os.popen(cmd)
        for line in output.readlines():
            if "ThisTime" in line:
                return re.search(r'(\d+)', line, flags=0).group(1)

    def stop_browser(self):
        cmd = 'adb shell am force-stop com.qihoo.contents'
        os.popen(cmd)

    def get_cpu(self):
        cmd = 'adb shell dumpsys cpuinfo | grep com.qihoo.contents'
        output = os.popen(cmd)
        for line in output.readlines():
            return re.search(r'(\d+)%\s*\d+/com.qihoo.contents:', line, flags=0).group(1)

    def get_meminfo(self):
        cmd = 'adb shell top -d 1| grep com.qihoo.contents > meminfo.txt'
        os.popen(cmd)
        meminfo_value = [('id', 'vss', 'rss')]
        meminfo_file = file('meminfo.txt', 'r')
        i = 1;
        results = meminfo_file.readlines()
        for r in results:
            if r.endswith('com.qihoo.contents'):
                meminfo_value.append((i, r.split()[5].strip('K')), r.split()[6].strip('K'))
                i = i + 1
        meminfo_file.close()


class Controller(object):
    def __init__(self, count):
        self.browser = Browser()
        self.count = count
        self.data = [('ts', 'running_time')]

    def launche_time_process(self):
        running_time = self.browser.launch_browser()
        time.sleep(5)
        self.browser.stop_browser()
        self.data.append((self.cur_time(), running_time))

    def cur_time(self):
        return time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime())

    def run(self):
        while self.count > 0:
            self.test_process()
            self.count = self.count - 1

    def save_data(self):
        lau_time_csv = file('launchertime_' + self.cur_time() + '.csv', 'wb')
        w = csv.writer(lau_time_csv)
        w.writerows(self.data)
        lau_time_csv.close()


if __name__ == "__main__":
    controller = Controller(10)
    controller.run()
    controller.save_data()
