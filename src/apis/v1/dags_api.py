
from fastapi import APIRouter, Depends, HTTPException, Body, logger
from fastapi.responses import JSONResponse
from datetime import datetime
from typing import Any, Optional

import  json

from src.config import  Config
from src.models.schemas.dag_schema import DagRun, Item
from src.core.log.logging_mixin import  Logger, LoggingMixin
_logger = Logger(__name__)
router = APIRouter()

from src.models.domains.base_respone_model import ResponeModel
from src.plugins.airflow.dag import  dag_operator
from src.plugins.airflow.dag_run import dag_run_operator

@router.get("/health", tags=["dag"])
async def health():
    return {"status": "ok","health": datetime.now().timestamp()}

@router.get("/test", tags=["dag"])
async def test() -> ResponeModel:
    from src.plugins.airflow.dag_run import  dag_run_operator
    base_url = Config.AIRFLOW_SERVICE_URL
    dag_run_operator_instance = dag_run_operator(base_url=base_url)
    res = dag_run_operator_instance.test()
    return ResponeModel(result=res.json())

@router.get("/dags",tags=["dag"])
async def get_dag_list() -> ResponeModel:
    dag_operator_instance = dag_operator(Config.AIRFLOW_SERVICE_URL)
    res = dag_operator_instance.get_dags()
    return ResponeModel(result=res.json())

@router.get("/{dag_id}/dagRuns",tags=["dag"])
async def get_dag_runs(dag_id:str) -> ResponeModel:
    dag_run_operator_instance = dag_run_operator(Config.AIRFLOW_SERVICE_URL)
    res = dag_run_operator_instance.get_dag_run(dag_id)
    return ResponeModel(result=res)

@router.post("/run/once",tags=["dag"])
async  def dag_run_once(
        item:DagRun
    ) -> ResponeModel:
    """
     @data
      {
          "execution_date": "YYYY-mm-DDTHH:MM:SS.ssssss",
          "conf": "{"key":"value"}",
          "replace_microseconds": "false"
      }
    """
    dag_run_operator_instance = dag_run_operator(Config.AIRFLOW_SERVICE_URL)
    item.dag_run_id = item.dag_id+'-'+'{}'.format(datetime.now().timestamp()).replace('.','-')
    #create dagrun
    res = dag_run_operator_instance.create_dag_run(item.dag_id, item.execution_date, item.conf)
    #check dag is paused, update state
    return ResponeModel(result=res)

@router.patch("/{dag_id}",tags=["dag"])
async  def update_dag_pause(
        dag_id:str,
        is_paused: bool = False
    ) -> ResponeModel:
    """
     
    """
    
    #check dag is paused, update state
    dag_operator_instance = dag_operator(Config.AIRFLOW_SERVICE_URL)
    res_update = dag_operator_instance.update_dag_pause(dag_id,is_paused)
    return ResponeModel(result=res_update.json())
 