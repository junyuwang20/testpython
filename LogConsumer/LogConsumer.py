import sys
sys.path.append("..")
from pykafka import KafkaClient
import time
from LoaderTzt import LoaderTzt
from LogConsumerConfig import *
import logging.config
from pykafka.broker import Broker


debug = True
logging.config.fileConfig('logconf.cfg')
log_name = 'logconsumer'
loger = logging.getLogger(log_name)


def unblock_do():
    pass
#read config


loger.info('============================start LogConsumer===========================')
config = LogConsumerConfig('consumer.cfg')
config = config.config()
hosts = config.get(LogConsumerSections.kafka, LogConsumerOptions.hosts)
topics = config.get(LogConsumerSections.kafka, LogConsumerOptions.topics)
consumer_group = config.get(LogConsumerSections.kafka, LogConsumerOptions.consumer_group)
auto_commit_interval_ms = config.getint(LogConsumerSections.kafka, LogConsumerOptions.auto_commit_interval_ms)
consumer_id = config.get(LogConsumerSections.kafka, LogConsumerOptions.consumer_id)
partition_offset = config.getint(LogConsumerSections.kafka, LogConsumerOptions.partition_offset)

commit_batch = config.getint(LogConsumerSections.mysql, LogConsumerOptions.commit_batch)
mysql_hosts = config.get(LogConsumerSections.mysql, LogConsumerOptions.hosts)
mysql_user = config.get(LogConsumerSections.mysql, LogConsumerOptions.user)
mysql_pwd = config.get(LogConsumerSections.mysql, LogConsumerOptions.password)


#create kafka client
client = KafkaClient(hosts=hosts)
topic = client.topics[topics]
#consumer = topic.get_simple_consumer(consumer_group=consumer_group, auto_commit_enable=True, \
#                                     auto_commit_interval_ms=auto_commit_interval_ms, consumer_id=consumer_id)

consumer = topic.get_balanced_consumer(consumer_group=consumer_group, managed=True, auto_commit_enable=True, \
                                     auto_commit_interval_ms=auto_commit_interval_ms, consumer_timeout_ms=5000)

#init kafka partition offset
if partition_offset >=0:
    partition_offset_pairs = []
    loger.debug('partition num:{}'.format(len(consumer.partitions)))
    for p in consumer.partitions.itervalues():
        if p:
            loger.debug('the latest_available_offset of partion {} is: {}'.format(p.id, p.latest_available_offset()))
            if p.latest_available_offset() >= partition_offset:
                partition_offset_pairs.append((p, partition_offset))
                loger.debug('reset partition {} offset to {}'.format(p.id, partition_offset))
    try:
        consumer.reset_offsets(partition_offsets=partition_offset_pairs)
    except:
        loger.error('set partition offset error!')

#consume kafka message
loger.info('waiting for message......')

offset = partition_offset

#creat loader for saving log to database
loader = LoaderTzt(host=mysql_hosts, usr=mysql_user, pwd=mysql_pwd)
if debug:
    loader.clear_table()
while True:
    loger.info('====read from kafka start, offset:{}......'.format(offset))
    #loader = LoaderTzt(host=mysql_hosts, usr=mysql_user, pwd=mysql_pwd)
    i = 0

    message = consumer.consume(block=True)
    while message is not None:
        i+=1
        loader.LoadPack(message.value, partition_id=message.partition_id, partition_offset=message.offset)
        offset = message.offset
        broker = consumer.partitions[message.partition_id].leader
        replicas_broker = consumer.partitions[message.partition_id].replicas
        loger.debug('leader broker of partition{} is {}'.format(message.partition_id, broker.host))
        loger.debug('offset of partition{} is {}; message:{}'.format(message.partition_id, offset, message.value))
        if i >= commit_batch:
            break
        #message = consumer.consume(block=False, unblock_event=unblock_do())
        message = consumer.consume(block=False)
    try:
        loger.info('read from kafka finished, offset:{};messag num:{}'.format(offset, i))
        loader.insert_logs()
    except Exception as e:
        loger.error('{}; kafka start offset={};end offset={}'.format(e, partition_offset, offset))
    time.sleep(5)
#consumer.stop()
