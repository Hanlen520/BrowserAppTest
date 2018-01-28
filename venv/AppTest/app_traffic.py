# /usr/bin/python
# encoding:utf-8
import csv
import os
import time
import re


class Controller(object):
    def __init__(self, count):
        self.count = count
        self.data = [('time', 'app_traffic')]

    def get_uid(self):
        cmd = 'adb shell ps | grep com.qihoo.contents'
        pid = ""
        output = os.popen(cmd).readlines()
        for line in output:
            if line.strip().endswith('com.qihoo.contents'):
                pid = re.search("\w+\s+(\d+)\s+.+", line, flags=0).group(1)

        uid_output = os.popen('adb shell cat /proc/' + pid + '/status').readlines()
        for l in uid_output:
            if l.strip().startswith('Uid'):
                return re.search("Uid:\s+(\d+)", l.strip(), flags=0).group(1)

    def test(self):
        uid = self.get_uid()
        snd_cmd = 'adb shell cat /proc/uid_stat/' + uid + '/tcp_snd'
        rcv_cmd = 'adb shell cat /proc/uid_stat/' + uid + '/tcp_rcv'
        cur_time = self.cur_time()
        snd_output = os.popen(snd_cmd).readlines()
        rcv_output = os.popen(rcv_cmd).readlines()
        for s in snd_output:
            if re.search('\d+', s, flags=0) > 0:
                for r in rcv_output:
                    if re.search('\d+', r, flags=0):
                        self.data.append((cur_time, str(int(re.search('(\d+)', s, flags=0).group(1)) + int(
                            re.search('(\d+)', r, flags=0).group(1)))))

    def cur_time(self):
        return time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime())

    def run(self):
        while self.count > 0:
            self.test()
            time.sleep(5)
            self.count = self.count - 1

    def save_data(self):
        traffic_csv = file('traffic_' + self.cur_time() + '.csv', 'wb')
        w = csv.writer(traffic_csv)
        w.writerows(self.data)
        traffic_csv.close()


if __name__ == "__main__":
    c = Controller(10)
    c.run()
    c.save_data()
