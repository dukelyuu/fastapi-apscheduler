# -*- encoding: utf-8 -*-
#******************************************#
#Desc    :routers.py
#文件    :routers.py
#Update    :2021/02/25 02:45:36
#Author    :duke(duke.lv@hotmail.com)
#******************************************#

from fastapi import APIRouter
from src.apis.v1 import schedule_api,dags_api

router = APIRouter()
router.include_router(schedule_api.router, prefix="/task", tags=["task"])
router.include_router(dags_api.router, prefix="/dags", tags=["dags"])
