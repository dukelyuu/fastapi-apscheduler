from pydantic import BaseModel
from typing import Any, Optional

from src.models.domains.schedule_model import StartSchedule, StopSchedule
from src.models.domains.base_respone_model import ResponeModel



class StartScheduleRespone(ResponeModel):
    code: Optional[int] = 2000
    status: Optional[str] = 'OK'
    message: Optional[Any] = None
    result: Optional[Any] = None

class StopScheduleRespone(ResponeModel):
    code: Optional[int] = 2000
    status: Optional[str] = 'OK'
    message: Optional[Any] = None
    result: Optional[Any] = None