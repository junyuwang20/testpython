#-*coding:UTF-8-*-
import sys
sys.path.append("..")
import time
from ExtractorTzt import TztExtractor
from ReadLogDoKafka import ReadLogDoKafka
from FileFlow import FileFlow
import logging.config
from LogReaderConfig import LogReaderConfig



logging.config.fileConfig('logconf.cfg')
log_name = 'logreader'
log = logging.getLogger(log_name)
config = LogReaderConfig('LogReader.cfg')

log.info('============================start LogReader==============================')

hosts = config.hosts()
try:
    Ex = TztExtractor()
    topics = str.encode(config.topic())
    reader = ReadLogDoKafka(Ex, hosts=hosts, topic=topics)
except Exception as e:
    log.error('create reader {} catched:{}'.format(e.__class__.__name__, e.message))

try:
        file_flow = FileFlow(reader, file_path=config.log_file(), seek_file_path=config.offset_file(), read_len=config.read_len())
except Exception as e:
    log.error('create file_flow {} catched:{}'.format(e.__class__.__name__, e))
try:
    while True:
        file_flow.read_file()
        time.sleep(5)
except Exception as e:
    log.error('file_flow.read_file {} catched:{}'.format(e.__class__.__name__, e))

