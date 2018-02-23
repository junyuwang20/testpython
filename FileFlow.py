#-*coding:UTF-8-*-
import io
import os
from ReadLogDo import ReadLogDo
import errno
from type_limit import type_limit

#ReadFile = "test.log"
#SeekFile = "Seek.log"
#Encoding="utf-8"
#ReadLimit=5
#Seek=0

#函数：读取文件索引
def ReadSeek(FileName):
    iseek = 0
    if os.path.exists(FileName):
        with io.open(FileName, 'rb') as f:
            seek=f.readline()
            if seek.isdigit():
                iseek=int(seek)
    return iseek

#函数：写文件索引
def WriteSeek(FileName, seek):
    writeNum = 0
    #if not os.path.exists(FileName):
     #   os.path
    with io.open(FileName, 'w') as f:
        if seek.isdigit():
            Str = str(seek)
            writeNum=f.write(unicode(Str))

    return writeNum


class FileFlow(object):

    @type_limit(object, ReadLogDo, file_path=str, seek_file_path=str)
    def __init__(self, reader, file_path='', seek_file_path='', read_len=1024):
        if not os.path.exists(file_path):
            raise Exception('File {} not found', format(file_path))
        self.__file = file_path
        self.__read_len = read_len
        self.__seek_file = seek_file_path
        self.__reader = reader

        d = os.path.dirname(seek_file_path)
        if (not os.path.exists(d)) and (d != ''):
            raise Exception('SeekFile directory {} not found', format(d))

    def read_file(self):
        seek = ReadSeek(self.__seek_file)
        with io.open(self.__file, 'rb') as f:
            f.seek(0, os.SEEK_END)
            end_pos = f.tell()
            if seek < end_pos:
                f.seek(seek)
                #line = f.readline()
                line = f.read(self.__read_len)
                #line = line.encode(self.__encoding)
                try:
                    while line:
                        print('**************************************start read at offset {}******************************'.format(seek))
                        seek_offset = self.__reader.read_do(line)
                        seek = seek + seek_offset
                        #print('seek is {};offset is {}; f.tell() is {}; line[0] is \'{}\''.format(seek, seek_offset, f.tell(), line[0]))

                        if f.tell() == end_pos:
                            break

                        #print(line + ":" + str(seek))
                        f.seek(seek)
                        line = f.read(self.__read_len)
                        #line = f.readline()
                        #line = line.encode(self.__encoding)
                    WriteSeek(self.__seek_file, str(seek))
                except Exception as e:
                    raise e
#######################################################################################
####主程序
#######################################################################################
# Seek = ReadSeek(SeekFile)
# print("seek:"+str(Seek))
# with io.open(ReadFile, 'r', encoding=Encoding) as f:
#     f.seek(0, 2)
#     if Seek < f.tell():
#         f.seek(Seek)
#         Line = f.read(ReadLimit)
#         while Line:
#             #print("{}:{}".format(Line,f.tell()))
#             Seek=f.tell()
#             print(Line+":"+str(Seek))
#             Line = f.read(ReadLimit)
#         WriteSeek(SeekFile, str(Seek))