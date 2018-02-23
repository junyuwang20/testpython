#-*coding:UTF-8-*-
import re
from ExtractorTzt import TztExtractor
from type_limit import type_limit
import os
from ReadLogDoKafka import ReadLogDoKafka
from ReadLogDo import ReadLogDo
from time import *
from FileFlow import FileFlow

class testReader(ReadLogDo):
    def read_do(self, msg):
        Ex = TztExtractor()
        offset = Ex.Extract(msg)
        logs = Ex.pop_logs()
        print(logs)
        # msg = str(msg)
        # #tmps = "测试abs实验12:33:11:ab+cd"
        # m = re.search('\d+:\d+:\d+\.*\d*:', msg)
        # print(m.group())
        # print('msg length = {}, msg is:{}'.format(len(msg), msg))
        #return len(bytes(msg))
        return offset

hosts = '119.28.133.19:9092'
try:
    Ex = TztExtractor()
    reader = ReadLogDoKafka(Ex, hosts=hosts, topic='test1')
    #reader = testReader()
except Exception as e:
    print('create reader {} catched:{}'.format(e.__class__.__name__, e.message))
try:
    file_flow = FileFlow(reader, file_path='test_long.log', seek_file_path='seed.log', read_len=2048)
except Exception as e:
    print('init file_flow {} catched:{}'.format(e.__class__.__name__, e))
try:
    #while True:
        file_flow.read_file()
        #sleep(2)
except Exception as e:
    print('file_flow.read_file {} catched:{}'.format(e.__class__.__name__, e))

