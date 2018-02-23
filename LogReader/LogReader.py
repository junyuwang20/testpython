#-*coding:UTF-8-*-
from ExtractorTzt import TztExtractor
from ReadLogDoKafka import ReadLogDoKafka
from FileFlow import FileFlow
import logging.config
from LogReaderConfig import LogReaderConfig


logging.config.fileConfig('logconf.cfg')
log_name = 'logreader'
log = logging.getLogger(log_name)
config = LogReaderConfig('LogReader.cfg')


hosts = config.hosts()
try:
    Ex = TztExtractor()
    reader = ReadLogDoKafka(Ex, hosts=hosts, topic=config.topic())
except Exception as e:
    log.error('create reader {} catched:{}'.format(e.__class__.__name__, e.message))

try:
    file_flow = FileFlow(reader, file_path=config.log_file(), seek_file_path=config.offset_file(), read_len=config.read_len())
except Exception as e:
    log.error('init file_flow {} catched:{}'.format(e.__class__.__name__, e))
try:
        file_flow.read_file()
except Exception as e:
    log.error('file_flow.read_file {} catched:{}'.format(e.__class__.__name__, e))

