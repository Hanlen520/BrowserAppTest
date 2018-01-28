# /usr/bin/python
# encoding:utf-8
import csv
import os
import time
import re


class Browser(object):
    def dumpsys_info(self):
        f_name = 'dumpsys_info' + '_' + time.strftime("%Y%m%d%H%M%S", time.localtime()) + '.txt'
        cmd = 'adb shell top -d 2 | grep com.qihoo.contents > ' + f_name
        os.popen(cmd)
    
class Controller(object):
    def __init__(self):
        self.data = [('id','cpu_info','vss','rss')]
        self.f_name = ''

    def get_cur_time(self):
        return  time.strftime("%Y%m%d%H%M%S", time.localtime())

    def dumpsys_info(self):
        self.f_name = 
        cmd = 'adb shell top -d 2 | grep com.qihoo.contents > ' + self.f_name + '.txt'
