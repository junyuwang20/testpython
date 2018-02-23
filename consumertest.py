from pykafka import KafkaClient
import time
from LoaderTzt import LoaderTzt
from LogConsumerConfig import *
import FileFlow
from pykafka.partition import Partition


def unblock_do():
    pass

#read config
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
consumer = topic.get_simple_consumer(consumer_group=consumer_group, auto_commit_enable=True, \
                                     auto_commit_interval_ms=auto_commit_interval_ms, consumer_id=consumer_id)

#init kafka partition offset
if partition_offset >0:
    partition_offset_pairs = []
    print('patition num:{}'.format(len(consumer.partitions)))
    for p in consumer.partitions.itervalues():
        if p:
            if p.latest_available_offset() >= partition_offset:
                partition_offset_pairs.append((p, partition_offset))
    try:
        consumer.reset_offsets(partition_offsets=partition_offset_pairs)
    except:
        print('except::::::')

#consume kafka message
message = consumer.consume(block=True, unblock_event=unblock_do())
i = 0
while True:
    print('=========start load=========')
    loader = LoaderTzt(host=mysql_hosts, usr=mysql_user, pwd=mysql_pwd)
    while message is not None:
        i+=1
        loader.LoadPack(message.value)
        print message.offset, '  ', message.value
        message = consumer.consume(block=False, unblock_event=unblock_do())
        if i == commit_batch:
            break

    print('========load finished=======')
    loader.insert_logs()
    time.sleep(5)
#consumer.stop()
