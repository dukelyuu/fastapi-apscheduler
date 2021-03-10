#!/usr/bin/python
# -*- coding: UTF-8 -*-
#******************************************#
#Desc: 
#  自定义公共方法
#Author: jian.lv(jian.lv@hotmail.com)
#Update: 2019年11月23日
#******************************************#
import os
import time
from functools import wraps
from flask import g, request, current_app

def _unknown_ex_handler(err):
    '''
        function: 未知错误捕获
        :param: err
        :return: wrapper对象
    '''
    try:
        _error_log_handler(err, 'unknown_error')
        current_app.logger.error(err)
    except Exception as ex:
        current_app.logger.error(ex)
        
def _error_log_handler(err, log_name):
    import time
    import traceback
    log_root = os.path.join('logs', os.getenv('ENV'))
    if not os.path.exists(log_root):
        os.makedirs(log_root)
    log_file = os.path.join(log_root, '{}.txt'.format(log_name))
    if os.path.exists(log_file) and os.path.getsize(log_file) > 10 * 1024 * 1024:
        backup_log_file = '{}_{}.txt'.format(log_name, time.strftime("%Y%m%d%H%M%S",time.localtime(time.time())))
        log_file_backup = os.path.join(log_root, backup_log_file)
        os.rename(log_file, log_file_backup)
    with open(log_file, 'a+') as f:
        title = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
        f.write('{} SQLAlchemyError'.format(title))
        traceback.print_exc(file=f)

def _sqlalchemy_ex_handler(err, log_name):
    '''
        function: 数据库相关错误处理:
            1. 记录堆栈日志
            2. 尝试回滚事务
        :param: err
        :return: wrapper对象
    
    '''
    try:
        _error_log_handler(err, 'db_error')
        current_app.logger.error(err)
        # from src.models.base import BaseModel
        # BaseModel.rollback()
    except Exception as ex:
        current_app.logger.error(ex)