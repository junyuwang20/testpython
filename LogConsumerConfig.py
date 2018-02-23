from ConfigParser import RawConfigParser
import os
import io
import copy

class LogConsumerSections(object):
    kafka = 'KAFKA'
    mysql = 'MYSQL'


class LogConsumerOptions(object):
    hosts = 'hosts'
    port = 'port'
    topics = 'topics'
    consumer_group = 'consumer_group'
    auto_commit_interval_ms = 'auto_commit_interval_ms'
    consumer_id = 'consumer_id'
    partition_offset = 'partition_offset'
    commit_batch = 'commit_batch'
    user = 'user'
    password = 'pwd'
    database = 'database'


class LogConsumerConfig(object):
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
        self.__config.add_section(LogConsumerSections.kafka)
        self.__config.add_section(LogConsumerSections.mysql)

        #set kafka section default value
        self.__config.set(LogConsumerSections.kafka, LogConsumerOptions.hosts, 'localhost:9092')
        self.__config.set(LogConsumerSections.kafka,LogConsumerOptions.topics, 'test1')
        self.__config.set(LogConsumerSections.kafka,LogConsumerOptions.consumer_group, 'test')
        self.__config.set(LogConsumerSections.kafka,LogConsumerOptions.auto_commit_interval_ms, '1')
        self.__config.set(LogConsumerSections.kafka,LogConsumerOptions.consumer_id, 'test')
        self.__config.set(LogConsumerSections.kafka,LogConsumerOptions.partition_offset, '-1')

        #set mysql section default value
        self.__config.set(LogConsumerSections.mysql,LogConsumerOptions.commit_batch, '100')
        self.__config.set(LogConsumerSections.mysql,LogConsumerOptions.hosts, 'localhost')
        self.__config.set(LogConsumerSections.mysql, LogConsumerOptions.port, '3306')
        self.__config.set(LogConsumerSections.mysql, LogConsumerOptions.user, 'root')
        self.__config.set(LogConsumerSections.mysql, LogConsumerOptions.password, '666666')


    def config(self):
        return self.__config