
# # -*- coding: UTF-8 -*-
# #******************************************#
# #Desc: 
# #  主入口
# #Author: jian.lv(jian.lv@hotmail.com)
# #Update: 2019年11月23日
# #******************************************#

# #----------------------------Import----------------------------------#
# import os
# from flask import Flask, current_app
# import glob
# import importlib
# import logging
# import sys
# from src.utils.decorators.except_hander import except_hander
# from src.config import DevConfig, TestConfig, DemoConfig, ProdConfig, UnitTestConfig
# #----------------------------End Import------------------------------#
# @except_hander
# def create_app(config_type=None,template_folder=None):
#     ''' 
#         function: 初始化 并创建app对象
#         :param config_type: 配置类型
#         :return: flask app对象
#     '''
#     app = Flask(__name__,instance_relative_config=True, template_folder=template_folder)
#     init_config(app, config_type)
#     return app

# def init_config(app,config_type):
#     if config_type is None or config_type == 'dev':
#         app.config.from_object(DevConfig)
#     if config_type == 'test':
#         app.config.from_object(TestConfig)
        
#     if config_type == 'UnitTest':
#         app.config.from_object(UnitTestConfig)

#     if config_type == 'demo':
#         app.config.from_object(DemoConfig)

#     if config_type == 'production':
#         app.config.from_object(ProdConfig)
        
# def import_modules(pathname: str):
#     """
#     function：
#       导入指定路径或者目录下的模块，并返回模块信息

#     :param pathname: 要导入的模块路径(相对路径)，可以导入指定目录下的模块，只要符合glob路径表达式写法即可
#     :return: 模块信息字典
#     """
#     modules_dict = {}
#     module_paths = glob.glob(pathname)
#     valid_paths = []
    
#     for p in module_paths:
#         full_name = p.replace(os.sep, '.')[:-3]
#         print(full_name)
#         module_name = full_name[full_name.find('src'):]
#         if module_name.find("_api") > 0:
#             valid_paths.append(module_name)
    
#     for path in valid_paths:
#         # full_name = path.replace(os.sep, '.')[:-3]
#         # module_name = full_name[full_name.find('src'):]
#         module = importlib.import_module(path)
#         # modules_dict[module_name]

#         for element in dir(module):
#              if not element.startswith('__') and element == "api":
#             # 获取用户自定义的函数和变量名称
#                 cls_obj = getattr(module, element)
#                 is_class = hasattr(cls_obj, '__class__')
#                 if is_class:
#                     modules_dict[module]= eval('module.{}'.format(element))
#     return modules_dict

# def register_blueprint(app, path=None):
#     ''' 
#         function:
#           注册自动注册api blueprint 模块，文件格式要求，必须以_api为文件名，如：menus_api.py
#         :param app:当前运行的app 
#         :return: none
#     ''' 
#     _entries = []
#     if path is None:
#         path = os.path.abspath(os.path.dirname(__file__)) #获取绝对路径
#         path = os.path.join(path, "apis")
#         _entries = os.scandir(path)
#     for d in _entries:
#         path = os.path.join(path, "apis", d)
       
#         if os.path.isdir(path):
#             file_path = os.path.join(path, "**.py")
        
#             modules = import_modules(file_path)
          
#             app.logger.info("========================Begin register api modules=========================")
#             for m in modules:
#                 app.logger.info("file:%s-----router:%s",m.__name__,m.api.url_prefix)
#                 app.register_blueprint(m.api)
#             app.logger.info("========================End register api modules=========================") 
# -*- encoding: utf-8 -*-
#******************************************#
#Desc    :webapp.py
#文件    :webapp.py
#Update    :2021/02/24 19:36:49
#Author    :duke(duke.lv@hotmail.com)
#******************************************#

import  os
import glob
import logging
from src.config import config_map
API_PREFIX = config_map.get(os.environ.get('ENV', 'dev').lower()).API_PREFIX
PROJECT_NAME = config_map.get(os.environ.get('ENV', 'dev').lower()).PROJECT_NAME
DEBUG=config_map.get(os.environ.get('ENV', 'dev').lower()).DEBUG
VERSION=config_map.get(os.environ.get('ENV', 'dev').lower()).VERSION
ALLOWED_HOSTS=config_map.get(os.environ.get('ENV', 'dev').lower()).ALLOWED_HOSTS
 
import sys

from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException

from src.helpers.http_error_hepler import http_error_handler
from src.helpers.validation_error import http422_error_handler

from src.core.events import create_start_app_handler, create_stop_app_handler

from src.helpers.aps_scheduler_helper import aps_scheduler_helper

#导入路由
from src.apis.routers import router

def  create_app() -> FastAPI:
    """[创建 fastapi 应用]

    Returns:
        [FastAPI]: [description]
    """    
    app = FastAPI(title=PROJECT_NAME, debug=DEBUG, version=VERSION)
    
    app.include_router(router,prefix=API_PREFIX)
    init_config(app)
    return app

def init_config(app) -> None:
    """
    [初始化配置]

    Args:
        app ([None]): 
    """    
    if os.getenv('isCORS'):
        app.add_middleware(
            CORSMiddleware,
            allow_origins=ALLOWED_HOSTS or ["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    # init handler
    app.add_event_handler("startup", create_start_app_handler(app))
     
    app.add_event_handler("shutdown", create_stop_app_handler(app))
    
    app.add_exception_handler(HTTPException, http_error_handler)
    app.add_exception_handler(RequestValidationError, http422_error_handler)

app = create_app()

@app.on_event('startup')
async def init_schedule():
    scheduler = aps_scheduler_helper()
