from src.core.base_operator import  BaseOperator
from src.helpers.airflow_helper import  api_prefix, airflow_api_module, request_headers
from typing import  Optional, Any
from src.helpers.common_helper import  CommonHelper
import json
class dag_operator(BaseOperator):
    
    def __init__(self, 
                 base_url: str,
                 api_prefix: Optional[str] = None, 
                 method: Optional[str] = "",
                 auth_type: Any = None,
                 **kwargs
                 ) -> None:
        super().__init__(**kwargs)
        self.method = method.upper()
        self.base_url = base_url
        self.api_prefix = api_prefix
        self.auth_type = auth_type
        self._header = request_headers.AUTHORIZATION
    
    def get_dags(self) -> Any:
        """
         获取dag列表
         @return dag对象
         {
            "dags": [
                {
                "dag_id": "string",
                "description": "string",
                "file_token": "string",
                "fileloc": "string",
                "is_paused": true,
                "is_subdag": true,
                "owners": [
                    "string"
                ],
                "root_dag_id": "string",
                "tags": [
                    {
                    "name": "string"
                    }
                ]
                }
            ],
            "total_entries": 0
            }
        """
  
        
        endpoint = f'{api_prefix.AIRFLOW_API_PREFIX}{airflow_api_module.DAG.value}'
        headers = request_headers.AUTHORIZATION
        headers.update(request_headers.CONTENT_TYPE)
        self.log.info(f'header:{headers},endpoint:{endpoint}')
        res = self.execute(
            endpoint=endpoint,
            method='GET',
            headers=headers
        )
        return res
        
    def create_dag(self,
                   dag_file,
                   force : Optional[bool] = True,
                   pause: Optional[bool] = False,
                   unpause: Optional[bool] = False
                ):
        '''
        @Desc: 通过rest_api_plugin 创建一个dag对象
        @param dag_file dag 文件路径
        @param force 遇到已有同名文件是否强制保存
        @param pause true：dag被强制更新为pause状态
        @param unpause  true：dag被强制更新为unpause状态
        @returns: 
        '''
        self.api_prefix = 'rest_api/api'
        headers = request_headers.AUTHORIZATION
        headers = headers.update(request_headers.FORM_DATA_TYPE)
        data = {
            'dag_file': dag_file,
            'force': force,
            "pause": pause,
            "unpause": unpause
            
        }
        res = self.execute(
            endpoint='?api=deploy_dag',
            method='POST',
            data=data,
            headers=headers
        )
        return res.json()

    def delete_dag(self, dag_id:str):
        '''
        @Desc: 删除dag 
        :param dag_id 删除dag的 id
        :type dag_id:str
        @return
            {
            "message": "DAG [dag_test] deleted",
            "status": "success"
            }
        '''
        self.api_prefix = api_prefix.REST_PLUGIN_API_PREFIX
        endpoint = f'?api=delete_dag&dag_id={dag_id}'
        method = 'GET'
        headers = request_headers.AUTHORIZATION
        res = self.execute(
            endpoint=endpoint,
            method=method,
            headers = headers
        )
        return res.json()
    
    def update_dag_pause(self, dag_id: str,is_paused: bool):
        """
         更新dag 状态
        """
        endpoint = CommonHelper.get_url(api_prefix.AIRFLOW_API_PREFIX, f'/dags/{dag_id}')
        headers = request_headers.AUTHORIZATION
        headers.update(request_headers.CONTENT_TYPE)
        data = {
            "is_paused": is_paused
        }
        self.log.info(f'header:{headers},endpoint:{endpoint}')
        res = self.execute(
            endpoint=endpoint,
            method='PATCH',
            headers=headers,
            data=json.dumps(data)
        )
        return res
        
    def dag_state(self, dag_id:str, run_id:str):
        """
            获取dag run状态
            :param dag_id 
            :type dag_id:str
            :param run_id
            :type run_id:str\
             
            @return
                {
                "state": "success",
                "startDate": "2020-10-28T16:15:19.436693+0000",
                "endDate": "2020-10-28T16:21:36.245696+0000",
                "status": "success"
                }
            
        """
        self.api_prefix = api_prefix.REST_PLUGIN_API_PREFIX

        headers = request_headers.AUTHORIZATION
        headers = headers.update(request_headers.CONTENT_TYPE)
        endpoint = f'?api=dag_state&dag_id={dag_id}&run_id={run_id}'
        method = 'GET'
        res = self.execute(
            endpoint=endpoint,
            method=method,
            headers=headers
        )
        return res.json()
    def run_task_instance(self,dag_id:str, run_id: str, tasks: str, conf: str):
        self.api_prefix = api_prefix.REST_PLUGIN_API_PREFIX
        headers = request_headers.AUTHORIZATION
        headers = headers.update(request_headers.CONTENT_TYPE)
        endpoint = f'?api=run_task_instance'
        method = 'POST'
        res = self.execute(
            endpoint=endpoint,
            method=method,
            heaers=headers
        )
        return res.json()
            
        
    