
from enum import Enum
import  os
class api_prefix():
    AIRFLOW_API_PREFIX = 'api/v1'
    REST_PLUGIN_API_PREFIX = '/admin/rest_api/api'
    REST_API_EXPERIMENTAL_PREFIX = '/api/experimental/'
    ETL_API_PREFIX = '/etl/api'

class airflow_api_module(Enum):
    CONFIG = '/config'
    CONNECTION = '/connections/'
    DAG = '/dags'
    DAG_OPERATOR = '/dags/{dag_id}/'
    DAG_SOURCE_CODE = '/dagSource/{file_token}'
    DAG_RUN ='/dags/{dag_id}/dagRuns'
    POOL = '/pools'
    TASK_INSTANCE = '/dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances'
    VARIABLE = '/variables'
    XCOM_LIST = '/dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}/xcomEntries'
    XCOM_ENTRY = '/dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}/xcomEntries/dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}/xcomEntries/{xcom_key}'
    
class request_headers():
    CONTENT_TYPE = {"Content-Type": "application/json"}
    ACCEPT_TYPE = {"Accept": "application/json"}
    FORM_DATA_TYPE = {"Content-Type": "multipart/form-data"}
    AUTHORIZATION = {"Authorization": os.environ.get('AUTHORIZATION',default='Basic  dXNlcjphaXJmbG93')}
    
    
class airflow_api_endpoints():
    EXPERIMENTAL_ENDPOINT_POST_CREATE_DAGRUN =  'dags/<DAG_ID>/dag_runs'
    
class airflow_dag_list():
    BASE_DAG = os.environ.get('BASE_DAG', default='test_base_operator')