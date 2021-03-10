
#!/usr/bin/python
# -*- coding: UTF-8 -*-
#******************************************#
#Desc: 
#  metrics装饰器
#Author: jian.lv(jian.lv@hotmail.com)
#Update: 2019年11月23日
#******************************************#
# from functools import wraps
# from prometheus_flask_exporter import PrometheusMetrics
# from flask import current_app
# def Metrics(fn):
#     '''
#         function: 是否开启metrics
#         params: fn
#         return: wrapper
#     '''
#     @wraps(fn)
#     def wrapper(*args, **kwargs):
#         try:
#
#             if_metrics = current_app.config["METRICS"] or True
#             app_name = current_app.config["APPNAME"] or 'flask-app'
#             app_ver = current_app.config["APPVERSION"] or 'v1'
#             if if_metrics:
#
#                 metrics = PrometheusMetrics(current_app)
#                 metrics.info(app_name, app_name,version=app_ver)
#                 print("launch prometheus metrics plugin!",metrics)
#             return fn(*args, **kwargs)
#         except Exception as err:
#             print("error: launch metircs plugin error!", err)
#             return fn(*args, **kwargs)
#     return wrapper
