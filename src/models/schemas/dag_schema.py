from typing import Optional
from src.models.domains.basemodel import  BaseModel, ScheduleBaseModel

from typing import  Any, Optional

class DagRun(BaseModel):
    dag_id: Optional[str] = None
    execution_date: Optional[str] = None
    conf: Optional[Any] = None
    # replace_microseconds: Optional[bool] = None
    # state: Optional[str] = 'running'
    dag_run_id: Optional[str] = None
    
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: Optional[float] = None
    tax: Optional[float] = None    