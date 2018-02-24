from pykafka import KafkaClient
from type_limit import type_limit
from ReadLogDo import ReadLogDo
from ExtractorObj import ExtractorObj
import logging


log_name = 'logreader'
loger = logging.getLogger(log_name)


class ReadLogDoKafka(ReadLogDo):
    @type_limit(object, ExtractorObj, hosts=str, topic=str)
    def __init__(self, extractor, hosts='', topic=''):
        self.__Extractor = extractor
        #set Kafka producer hosts list
        self.__hosts = hosts

        #set Kafka topic
        self.__topic = topic

        #create Kafka producer
        self.__client = KafkaClient(hosts=self.__hosts, socket_timeout_ms=50000)
        self.__topics = self.__client.topics[self.__topic]
        self.__producer = self.__topics.get_producer()
        loger.debug(self.__client.topics)

    def read_do(self, msg_str):

        ret = 0
        try:
            offset = self.__Extractor.Extract(msg_str)
            ret = offset
            logs = self.__Extractor.pop_logs()
            msgnum = len(logs)
            if msgnum>0:
                loger.info('read {} messages, ready for sending to kafka'.format(msgnum))
            for log in logs:
                blog = bytes(log)
                loger.debug('send to kafka========{}'.format(blog))
                self.__producer.produce(blog)
            #self.__producer .produce(bytes(msg_str))
            return ret
        except Exception as e:
            raise e

    def __del__(self):
        #free producer
        try:
            self.__producer.stop()
        except:
            pass
