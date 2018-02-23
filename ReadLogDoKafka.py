from pykafka import KafkaClient
from type_limit import type_limit
from ReadLogDo import ReadLogDo
from ExtractorObj import ExtractorObj
from ExtractorTzt import TztExtractor


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
        print(self.__client.topics)

    def read_do(self, msg_str):

        ret = 0
        try:
            offset = self.__Extractor.Extract(msg_str)
            ret = offset
            logs = self.__Extractor.pop_logs()
            for log in logs:
                blog = bytes(log)
                print('send to kafka========', blog)
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
