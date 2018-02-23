import ReadLogDoKafka
import type_limit
import ReadLogDo


class ReadLogDoFactory(object):
    @type_limit(str)
    def __init__(self, subclass_name):
        subclass_name = str(subclass_name)
        if 'KAFKA' in subclass_name.upper():
            self.__subclass = ReadLogDoKafka.ReadLogDoKafka()

    def get_readlogdo(self):
        return self.__subclass
