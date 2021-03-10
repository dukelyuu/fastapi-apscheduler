import os
from flask import jsonify, make_response, Response, current_app


def res_response(res_result_dict):
    """标准正常响应,结果必须可以作json序列化  
        参数: data # 返回数据
            code # 状态码,默认200
    """
    return jsonify(res_result_dict), 200

def res_unauthorized(msg=None):
    """无权限
        参数: data # 返回数据
            code # 状态码,默认200
    """
    from src.common import lang
    if msg is None:
        msg = lang.resp('L_OPER_FORBIDDEN')
    return jsonify({"msg":msg, "code":4001, "status":False}), 401

def res_ex_response(e, original=False):
    """异常响应,结果必须可以作json序列化  
        参数: e # 原始错误信息
             original # 是否返回原始错误信息，默认flase
    """
    from src.common import lang
    if os.getenv('ENV') != 'UnitTest':
        current_app.logger.error(e)
    msg = lang.resp('L_OPER_FAILED')
    if original:
        msg = str(e)
    return jsonify({"msg":msg, "code":4001, "status":False}), 200


