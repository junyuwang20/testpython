# -*- coding:utf8 -*-


def type_limit(*param_type, **kw_type):
    def type_limit_decorator(func):

        def wrapper(*param, **kw):
            #Check param length
            type_len = len(param_type)
            param_len = len(param)
            if type_len != param_len:
                raise Exception('{} Error: param num incorrect,correct num is {}, but {} param found'.format(func.__name__, type_len, param_len))

            #check param type
            for i in range(type_len):
                t = param_type[i]
                p = param[i]

                if not isinstance(p, t):
                     raise Exception("{} Error: the {} param type error,{} needed, but {} found".format(func.__name__, i+1, type(t()), type(p)))

            #check dict type
            for i in kw_type.keys():
                if i == 'return_type':
                    continue
                if not (i in kw):
                    raise Exception('{} Error: key {} not found in param'.format(func.__name__, i))

            #check return type
            res = func(*param, **kw)
            if "return_type" in kw_type:
                rt = kw_type["return_type"]
                if not isinstance(res, rt):
                    raise Exception("{} Error: return type error,{} needed, but {} found".format(func.__name__, type(rt()), type(res)))

            return res
        return wrapper

    return type_limit_decorator
    #end of def type_limit(*param_type, **kw_type)


def check_ip(ip_str):
    pass
'''
@type_limit(int, int, return_type=str)
def test_type_limit(a, b):
    ret = str(a+b)
    return ret


try:
    test_type_limit("1",2)
except Exception, Argument:
    print Argument
'''
