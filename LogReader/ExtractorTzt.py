import re
from ExtractorObj import ExtractorObj
from LogKeys import *

class TztExtractor(ExtractorObj):
    def __init__(self):
        self.__logs = []

    def pop_logs(self):
        logs = self.__logs
        self.__logs = []
        return logs
    '''
    #######################################
    ########split log file to each action
    #######################################
    '''
    def Extract(self, msg):
        count = 0
        #find start of a log
        last = len(msg)-1
        offset = 0
        end = 0

        #find first pack time(it's where the pack start)
        m = re.search('\d+:\d+:\d+\.*\d*:', msg)
        last_pack_complete = True
        while m:
            count += 1
            pack_time = m.group().strip()
            last_end = end
            start = offset + m.start()
            offset = offset + m.end()
            tmps = msg[offset:last]

            #find next pack time, if get the next pack time means we find the end of the current pack
            m = re.search('\d+:\d+:\d+\.*\d*:', tmps)
            if m:
                end = offset + m.start()
            else:
                offset = last_end
                last_pack_complete = False
                break

            #get the pack content as log
            log = msg[start:end]

            print('===================={}:start={};end={}; offset={}'.format(count, start,end, offset))
            #get the action id of the pack
            action_m = re.search('action=\S*\s', log, re.IGNORECASE)
            if action_m:
                action = action_m.group().split('=')[1].strip()


                #extract the log pack to structed pack
                self.__log_packing(log, pack_time, action)
            else:
                detect_pack = re.search('InterFaceReq:', log, re.IGNORECASE)
                if detect_pack:
                    action = 'InterFaceReq'
                    self.__log_packing(log, pack_time, action)



            m = re.search('\d+:\d+:\d+\.*\d*:', msg[offset:last])

        if last_pack_complete:
            offset = last+1
        return offset


    '''
    ########################################################
    ######## the router of treating the log for each action
    ########################################################
    '''
    def __log_packing(self, log, time, action):
        ret = False
        if action.upper() == 'ENTRUSTSTOCK':
            ret = self.__action_entruststock(log, time)
        elif action.upper() == 'INTERFACEREQ':
            ret = self.__action_InterFaceReq(log, time)
        return ret


    def __action_entruststock(self, log, time):
        pack = {logkeys.action: 'ENTRUSTSTOCK', logkeys.pack_time:time}
        #print('MSG:'+log)
        #get pack_type value
        m = re.search('ClientReq', log, re.IGNORECASE)
        if m:
            pack[logkeys.pack_type] = logvalues.req_pack
        else:
            pack[logkeys.pack_type] = logvalues.ans_pack
        #get capital account
        account_m = re.search('Account=\S*\s', log, re.IGNORECASE)
        if account_m:
            pack[logkeys.capital_account] = account_m.group().strip()

        #get pack_id
        id_m = re.search('HandleSerialNo=\S*\s*', log, re.IGNORECASE)

        if id_m:
            pack[logkeys.pack_id] = id_m.group().strip()

        #print('pack:{}'.format(pack))
        self.__logs.append(pack)
        return True

    def __action_InterFaceReq(self, log, time):
        pack = {logkeys.action: 'InterFaceReq', logkeys.pack_time:time}
        self.__logs.append(pack)
        return True
        # while m:
        #     count += 1
        #     print('offset={},TztExtractor ({}):{}'.format(offset, count, msg))
        #     start = m.start()
        #     #msg = msg[m.end():]
        #     m = re.search('\d+:\d+:\d+\.*\d*:', msg)
        #find action id of the log


