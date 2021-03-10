import json
from fastapi import APIRouter, Depends, HTTPException, Body, logger
from fastapi.responses import JSONResponse
from datetime import datetime
from typing import Any, Optional

from src.config import  Config

router = APIRouter()

from src.models.schemas.schedule import  StartSchedule, StartScheduleRespone, StopScheduleRespone, StopSchedule
from src.plugins.ETL.task_operator import  task_operator  
from src.plugins.airflow.dag_run import  dag_run_operator
from src.models.domains.base_respone_model import  ResponeModel

@router.get("", tags=["schedule"])
async def home():
    return {"health": datetime.now().timestamp()}

@router.get("/test", tags=["schedule"])
async def test():
    base_url = Config.AIRFLOW_SERVICE_URL
    dag_run_operator_instance = dag_run_operator(base_url=base_url)
    res = dag_run_operator_instance.test()
    return res

@router.post("/run/{task_id}",tags=["schedule"])
async def run_task(
    task_id: int,
    item: StartSchedule
) -> ResponeModel:
    """启动任务

    Args:
        task_id (int): [任务id]
        item (StartSchedule): [传输内容]

    Returns:
        StartScheduleRespone: [返回对象]
        
     启动步骤：
        1、 调用ETL服务，更新服务状态
        2、更新成功后，触发任务调度
    """
    # step 1
    
    base_url = Config.ETL_SERVICE_URL
    etl_task_operator_instance = task_operator(base_url = base_url)
    res = etl_task_operator_instance.start_task(task_id,True,schedule_date=item.schedule_type)
   
    return ResponeModel(code=res.code,message = res.message,result=res.result,status=res.status)

@router.post("/run/once/{task_id}", tags=["schedule"])
async  def run_task_once(
        task_id: int,
        item: StartSchedule
) -> ResponeModel:
    base_url = Config.ETL_SERVICE_URL
    etl_task_operator_instance = task_operator(base_url = base_url)
    res = etl_task_operator_instance.start_task(task_id,True,schedule_date=item.schedule_type)
    
    return  ResponeModel(code=res.code,message = res.message,result=res.result,status=res.status)

@router.put("/stop/{task_id}", tags=["schedule"])
async def stop_task(
        task_id: int,
        item: StopSchedule
) -> StopScheduleRespone:
    base_url = Config.ETL_SERVICE_URL
    etl_task_operator_instance = task_operator(base_url = base_url)
    res = etl_task_operator_instance.stop_task(task_id)
    return StopScheduleRespone(code=res.code,message = res.message,result=res.result,status=res.status)

@router.patch("/stop", tags=["schedule"])
async def patch_stop_task(
        task_ids: Optional[Any]
) -> StopScheduleRespone:
    base_url = Config.ETL_SERVICE_URL
    etl_task_operator_instance = task_operator(base_url = base_url)
    _res = StopScheduleRespone()
    _message = []
    for task_id in task_ids.split(','):
        res = etl_task_operator_instance.stop_task(task_id)
        if res.code != 2000:
            _res.code = res.code
            _message.append(res.message)
            _res.message = _message
            _res.status = res.status
        else:
            _res.result = res.result
    return StopScheduleRespone(code=_res.code,message = _res.message,result=_res.result,status=_res.status)

@router.delete("/{task_id}", tags=["schedule"])
async def delete_task(
        task_id: int,
) -> StopScheduleRespone:
    base_url = Config.ETL_SERVICE_URL
    etl_task_operator_instance = task_operator(base_url = base_url)
    res = etl_task_operator_instance.delete_task(task_id)
    return StopScheduleRespone(code=res.code,message = res.message,result=res.result,status=res.status)