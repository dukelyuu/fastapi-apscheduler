from typing import  Optional, Any
from src.helpers.common_helper import  CommonHelper
from datetime import  datetime, timedelta
import json
from src.core.base_operator import  BaseOperator
from src.helpers.airflow_helper import  api_prefix, airflow_api_module, request_headers
from  src.helpers.aps_scheduler_helper import  aps_scheduler_helper
from src.models.domains.base_respone_model import  ResponeModel
from uuid import uuid1


scheduler_instance = None
class task_operator(BaseOperator):
    def __init__(self, 
                 method: str = "GET",
                 base_url: Optional[str] = None, 
                 api_prefix: Optional[str] = None, 
                 auth_type: Any = None,
                 **kwargs
                 ) -> None:
        super().__init__(method=method, base_url=base_url, api_prefix=api_prefix, **kwargs)
        self.method = method.upper()
        self.base_url = base_url
        self.api_prefix = api_prefix
        self.auth_type = auth_type
        self._header = request_headers.AUTHORIZATION
        
        global scheduler_instance 
        scheduler_instance = aps_scheduler_helper()
        print(scheduler_instance)
    
       
    def start_task(self, task_id, start: bool = True,schedule_date: Optional[Any] = None) -> Any:
        """"
        更新 etl task状态
        """
        res = ResponeModel()
        try:
            job = self.start_schedule_task(task_id=task_id,manMade=False,schedule_date=schedule_date)
            endpoint = CommonHelper.get_url(api_prefix.ETL_API_PREFIX,'data-intelligence-platform/task/update')
            data = {
                "id": task_id,
                "start": start,
            }
            headers = request_headers.CONTENT_TYPE
            # headers.update(request_headers.CONTENT_TYPE)
            request_res = self.execute(
                endpoint=endpoint,
                data=json.dumps(data),
                method='POST',
                headers=headers
            )
            res.result = request_res.text
            
        except Exception as ex:
            res.status = 'Failed'
            res.message = ex.args[0]
            res.code = 5000
        return res
    def start_schedule_task(self, task_id, manMade: bool =False, schedule_date: Optional[Any] = None):
       
        exist_job = scheduler_instance.get_job(job_id=str(task_id))
        if exist_job:
            scheduler_instance.resume_job(job_id=str(task_id))
        else:
            scheduler_instance.add_corn_job(job_id=str(task_id),job_func=self.start_etl_task,args=[task_id,manMade],trigger_date=schedule_date)
    
    def start_etl_task(self, task_id, manMade: bool=False) -> Any:
        """"
        启动 etl task状态
        """
        
        endpoint = CommonHelper.get_url(api_prefix.ETL_API_PREFIX,'data-intelligence-platform/task/start')
        data = {
            "id": task_id,
            "jobId": datetime.now().timestamp(), #f'task-{task_id}-{uuid1().__str__()}',
            "manMade": manMade
        }
        headers = request_headers.CONTENT_TYPE
        # headers.update(request_headers.CONTENT_TYPE)
        res = self.execute(
            endpoint=endpoint,
            data=data,
            method='GET',
            headers=headers
        )
        
        return res
    
    def stop_task(self, task_id) -> Any:
        """"
         task 停止
        """
        res = ResponeModel()
        try:
            job = scheduler_instance.pause_job(str(task_id))
            endpoint = CommonHelper.get_url(api_prefix.ETL_API_PREFIX,'data-intelligence-platform/task/stop')
            data = {
                "id": task_id,
                
            }
            headers = request_headers.CONTENT_TYPE
            # headers.update(request_headers.CONTENT_TYPE)
            request_res = self.execute(
                endpoint=endpoint,
                data=data,
                method='GET',
                headers=headers
            )
            res.result = request_res.text
        except Exception as ex:
            res.status = 'Failed'
            res.message = ex.args[0]
            res.code = 5000
        
        return res
    
    def delete_task(self, task_id) -> Any:
        """"
         task 删除
        """
        res = ResponeModel()
        try:
            job = scheduler_instance.remove_job(str(task_id))
            endpoint = CommonHelper.get_url(api_prefix.ETL_API_PREFIX,'data-intelligence-platform/task/delete')
            data = {
                "id": task_id,
            }
            headers = request_headers.CONTENT_TYPE
            request_res = self.execute(
                endpoint=endpoint,
                data=data,
                method='POST',
                headers=headers
            )
            res.result = request_res.text
            
        except Exception as ex:
            res.status = 'Failed'
            res.message = ex.args[0]
            res.code = 5000
        
        
        return res
    