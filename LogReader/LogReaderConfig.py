import sys

if sys.version_info > (3, 0):
    from configparser import RawConfigParser
else:
    from ConfigParser import RawConfigParser

import os
import io
import copy

class LogReaderSections(object):
    kafka = 'KAFKA'
    logfile = 'LOGFILE'


class LogReaderOptions(object):
    hosts = 'hosts'
    topic = 'topic'
    log_file = 'log_file'
    offset_file = 'offset_file'
    read_len = 'read_len'

class LogReaderConfig(object):
    def __init__(self, filename):
        self.__config = RawConfigParser()
        if not os.path.exists(filename):
            f = io.open(filename, 'wb')
            self.__init_config()
            self.__config.write(f)
            f.close()
        self.__config.read(filename)

    def __init_config(self):
        #add section
        self.__config.add_section(LogReaderSections.kafka)
        self.__config.add_section(LogReaderSections.logfile)

        #set kafka section default value
        self.__config.set(LogReaderSections.kafka, LogReaderOptions.hosts, 'localhost:9092')
        self.__config.set(LogReaderSections.kafka, LogReaderOptions.topic, 'test1')
        #set logfile section default value
        self.__config.set(LogReaderSections.logfile,LogReaderOptions.log_file, 'test.log')
        self.__config.set(LogReaderSections.logfile, LogReaderOptions.offset_file, 'offset.cfg')
        self.__config.set(LogReaderSections.logfile, LogReaderOptions.read_len, '4096')

    def hosts(self):
        return self.__config.get(LogReaderSections.kafka, LogReaderOptions.hosts)

    def topic(self):
        return self.__config.get(LogReaderSections.kafka, LogReaderOptions.topic)

    def log_file(self):
        return self.__config.get(LogReaderSections.logfile, LogReaderOptions.log_file)

    def offset_file(self):
        return self.__config.get(LogReaderSections.logfile, LogReaderOptions.offset_file)

    def read_len(self):
        return self.__config.getint(LogReaderSections.logfile, LogReaderOptions.read_len)