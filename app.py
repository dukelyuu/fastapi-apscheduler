#!/usr/bin/python
# -*- coding: UTF-8 -*-
#******************************************#
#Desc: 
#  主入口
#Author: jian.lv(jian.lv@hotmail.com)
#Update: 2019年11月23日
#******************************************#

import os
# import re
import sys
import uvicorn
import logging
logger = logging.Logger(__name__)
from datetime import datetime
from src.webapp import app
# from src.utils.decorators.metrics import Metrics
from fastapi import  status
# create app





@app.get("/heartbeat")
def root(
        *,
        status_code=status.HTTP_200_OK
):
    return {"health": f"OK {datetime.now().timestamp()}"}


def launch(*arg, **kwargs):
    """
    启动应用
    """    
    port = os.getenv('PORT')  or 80
    host = os.getenv('HOST') or "0.0.0.0"
    uvicorn.run(app,host=host,  port=port)

# launch app
if __name__ == '__main__':
    launch()