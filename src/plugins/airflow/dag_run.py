from src.core.base_operator import  BaseOperator
from src.helpers.airflow_helper import  api_prefix, airflow_api_module, request_headers
from typing import  Optional, Any
import json
from src.helpers.common_helper import  CommonHelper

class dag_run_operator(BaseOperator):
    
    def __init__(self, 
                 base_url: str,
                 api_prefix: Optional[str] = None, 
                 method: Optional[str] = "",
                 auth_type: Any = None,
                 **kwargs
                 ) -> None:
        super().__init__(**kwargs)
        self.method =  method.upper()
        self.base_url = ( base_url or 'http://127.0.0.1:8080')
        self.api_prefix = api_prefix
        self.auth_type = auth_type
    def create_dag_run(self, dag_id:str, execution_date: str, conf: Any) -> Any:
        """
        创建一个dag run
        """
        
        endpoint = CommonHelper.get_url(api_prefix.REST_API_EXPERIMENTAL_PREFIX, f'dags/{dag_id}/dag_runs')
        data = {
            "execution_date": execution_date,
            "conf": conf
        }
        headers = request_headers.AUTHORIZATION
        headers.update(request_headers.CONTENT_TYPE)
        res = self.execute(
            endpoint=endpoint,
            data=json.dumps(data),
            method='POST',
            headers=headers
        )
        
        return res.json()
    def get_dag_run(self, dag_id:str) -> Any:
        endpoint = f"{api_prefix.REST_API_EXPERIMENTAL_PREFIX}dags/{dag_id}/dag_runs"
        
        headers = request_headers.AUTHORIZATION
        headers.update(request_headers.CONTENT_TYPE)
        res = self.execute(
            endpoint=endpoint,
            method='GET',
            headers=headers
        )
        return res.json()
    
    def test(self) -> Any:
        endpoint = f"{api_prefix.REST_API_EXPERIMENTAL_PREFIX}test"
        headers = request_headers.AUTHORIZATION
        headers.update(request_headers.CONTENT_TYPE)
        
        res = self.execute(
            endpoint=endpoint,
            method='GET',
            headers=headers
        )
        return res.json()
    
