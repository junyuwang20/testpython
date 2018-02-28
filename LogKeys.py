#-*-coding:utf-8-*-
class logkeys(object):
    action = 'act' #功能
    action_id = 'act_id' #功能号
    capital_account = 'cap_account' #资金账号
    fund_account = 'fund_account' #基金账号
    pack_type = 'pack_type' #包类型 logvalues.req_pack 或 logvalues_ans_pack
    pack_id = 'pack_id' #包唯一标识
    pack_time = 'pack_time' #包时间戳
    pack_status = 'status' #包状态  logvalues.status_ok 或 logvalues.status_err
    pack_server = 'ip'  #日志所在服务器IP
    pack_content = 'content' #包内容
    partition_id = 'partition_id'#从哪个kafka partition中获取的
    partition_offset = 'partition_offset' #消息在kafka partition中的偏移量

class logvalues(object):
    req_pack = 'req' #请求包
    ans_pack = 'ans' #应答包
    status_ok = 'ok' #包正常
    status_err = 'err' #包错误

