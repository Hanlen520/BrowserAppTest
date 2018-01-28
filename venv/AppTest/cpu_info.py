# /usr/bin/python
# encoding:utf-8
import csv
import os
import time
import re


class Browser(object):
    def get_cpu_info(self):
        cmd = 'adb shell dumpsys cpuinfo | grep com.qihoo.contents'
        output = os.popen(cmd)
        for line in output.readlines():
            return re.search(r'(\d+)%\s*\d+/com.qihoo.contents:', line, flags=0).group(1)


class Controller(object):
    def __init__(self, count, interval):
        self.browser = Browser()
        self.count = count
        self.interval = interval
        self.data = [('time', 'cpu_info')]

    def test(self):
        self.data.append((self.cur_time(), self.browser.get_cpu_info()))

    def cur_time(self):
        return time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime())

    def run(self):
        while self.count > 0:
            self.test()
            self.count = self.count - 1
            time.sleep(self.interval)

    def sava_data(self):
        cpu_info_csv = file('cpu_info_' + self.cur_time() + '.csv', 'wb')
        w = csv.writer(cpu_info_csv)
        w.writerows(self.data)
        cpu_info_csv.close()


if __name__ == "__main__":
    os.popen('adb kill-server')
    os.popen('adb start-server')
    controaller = Controller(20, 2)
    controaller.run()
    controaller.sava_data()
