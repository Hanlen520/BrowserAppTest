# /usr/bin/python
# encoding:utf-8
import csv
import os
import time
import re


class Controller(object):
    def __init__(self, count):
        self.count = count
        self.data = [('time', 'battery_info')]

    def test_process(self):
        cmd = 'adb shell dumpsys battery'
        output = os.popen(cmd).readlines()
        cur_time = self.cur_time()
        for line in output:
            if 'level' in line:
                self.data.append((cur_time, re.search('(\d+)', line, flags=0).group(1)))
                break

    def cur_time(self):
        return time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime())

    def run(self):
        os.popen('adb shell dumpsys battery set status 1')
        while self.count > 0:
            self.test_process()
            self.count = self.count - 1
            time.sleep(10)

    def save_data(self):
        battery_csv_name = file('battery_' + self.cur_time() + '.csv', 'wb')
        w = csv.writer(battery_csv_name)
        w.writerows(self.data)
        battery_csv_name.close()


if __name__ == "__main__":
    os.popen('adb kill-server')
    os.popen('adb start-server')
    c = Controller(6)
    c.run()
    c.save_data()
