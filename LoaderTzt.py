#-*-coding:utf-8-*-
from FileFlow import FileFlow
from ReadLogDo import ReadLogDo
import re
import io
import MySQLdb
from LogKeys import *

class TableFields:
    Pack_ID = 'Pack_ID'
    TimeStamp = 'TimeStamp'
    Action = 'Action'
    Status = 'Status'
    ServerIP = 'ServerIP'
    LogContent = 'LogContent'


class LoaderTzt:
    def __init__(self, host='localhost', usr='root', pwd='666666'):
        self.__args = []
        self.__host = host
        self.__usr = usr
        self.__pwd = pwd

    def LoadPack(self, packstr):
        dict = eval(packstr)

        action = ''
        if logkeys.action in dict.keys():
            action = dict[logkeys.action]  # 功能

        pack_id = ''
        if action.upper().strip() == 'INTERFACEREQ':
            pack_id = dict[logkeys.pack_time] + dict[logkeys.action]
        else:
            if logkeys.pack_id in dict.keys():
                pack_id = dict[logkeys.pack_id]  # 包唯一标识

        pack_time = ''
        if logkeys.pack_time in dict.keys():
            pack_time = dict[logkeys.pack_time]  # 包时间戳

        pack_status = ''
        if logkeys.pack_status in dict.keys():
            pack_status = dict[logkeys.pack_status]  # 包状态

        pack_server = ''
        if logkeys.pack_server in dict.keys():
            pack_server = dict[logkeys.pack_server]  # 日志所在服务器

        pack_content = packstr.replace("'", '"')
        arg = (pack_id, pack_time, action, pack_status, pack_server, pack_content)
        self.__args.append(arg)

    def insert_logs(self):
        if len(self.__args) == 0:
            return

        sql = "INSERT INTO LogFlowTZT ({}, {}, {}, {}, {}, {}) VALUES (%s, %s, %s, %s, %s, %s)".\
            format(TableFields.Pack_ID, TableFields.TimeStamp, TableFields.Action, TableFields.Status, \
                   TableFields.ServerIP, TableFields.LogContent)

        con = MySQLdb.connect(self.__host, self.__usr, self.__pwd, 'LogAnalyDB')
        with con:
            try:
                cursor = con.cursor()
                cursor.execute("delete from LogFlowTZT")
                cursor.executemany(sql, self.__args)
                con.commit()
            except Exception as e:
                con.rollback()
                raise e