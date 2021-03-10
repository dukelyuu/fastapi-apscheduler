
#!/usr/bin/python
# -*- coding: UTF-8 -*-
#******************************************#
#Desc: 
#  自定义异常处理装饰器
#Author: jian.lv(jian.lv@hotmail.com)
#Update: 2019年11月23日
#******************************************#
from src.utils.common import _error_log_handler,_sqlalchemy_ex_handler,_unknown_ex_handler
from functools import wraps
def except_hander(fn):
    '''
        function: 用在不需要jwt校验的公开接口
        :param: fn
        :return: wrapper对象
        
    '''
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except SQLAlchemyError as err:
            # _sqlalchemy_ex_handler(err, 'db_error')
            return fn(*args, **kwargs)
            # res_ex_response(lang.resp('L_CONNECT_FAILED'), original=True)
        except Exception as err:
            _unknown_ex_handler(err)
            return fn(*args, **kwargs)
            # res_ex_response(lang.resp('L_OPER_FAILED'), original=True)
    return wrapper