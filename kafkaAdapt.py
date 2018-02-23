from pykafka import KafkaClient
import time
client = KafkaClient(hosts='localhost:9092')
print(client.topics)

topic = client.topics['test1']
producer = topic.get_producer()
print('send message:')
producer.produce("hello form python")
print('stop producer')
producer.stop()

time.sleep(5)
print('start consumer:')
consumer = topic.get_simple_consumer(consumer_group='test', auto_commit_enable=True, auto_commit_interval_ms=1, consumer_id='test')
for message in consumer:
    if message is not None:
        print message.offset, message.value
