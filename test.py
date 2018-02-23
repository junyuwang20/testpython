import logging
import logging.config
#-*-coding:utf-8-*-
#from LogConsumerConfig import LogConsumerConfig
#log = LogConsumerConfig('consumer.cfg')
logging.config.fileConfig('logconf.cfg')
log = logging.getLogger('main')
print(log.name)

log.info('=========================')
log.debug('hello_debug')
log.error('hello_error')
log.critical('hello_critical')
log.warning('hello_warning')
log.info('hello')
log.info('\n\n')
# class ReadTztLogDo(ReadLogDo):
#     def read_do(self, msg):
#         msg = str(msg)
#         c = re.search("[/d*]:[/d*]:", '12:33:11ab+cd')
#
#         print(c.group())
# file_flow = FileFlow(file_path='test.log', seek_file_path='seed.log')
# reader = ReadTztLogDo()
# file_flow.add_reader(reader)


# c = re.compile("/d")
# r = c.search('12:33:11ab+cd')
#print(r)

# m12 = re.match("ab(.|\n)cd","ab\ncd")
# print "m12 match is ", m12.group()
#
# m14 = re.match("[^abcdef]","zabcxyz")
# print "m14 match is ",m14.group()
#
# tmps = "32:aba"
# m21 = re.search('a(?!\d)',tmps)
# print tmps[4:]
# if m21:
#     print("m21 match at[{},{}], value is {}".format(m21.start(),m21.end(),str(m21.group())))
#
# tmps = "abs12:33:11.089:ab+cd"
# m22 = re.search('\d+:\d+:\d+.\d+:',tmps)
# if m22:
#     print("m22 match at[{},{}], value is {}".format(m22.start(),m22.end(),str(m22.group())))