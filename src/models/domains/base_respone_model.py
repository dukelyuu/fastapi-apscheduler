# from pydantic import  BaseModel
from src.models.domains.basemodel import ScheduleBaseModel
from typing import  Optional, Any

class ResponeModel(ScheduleBaseModel):
    """
    返回对象鸡肋
    """
    code: Optional[int] = 2000
    status: Optional[str] = 'OK'
    message: Optional[Any] = None
    result: Optional[Any] = None
    # def __init__(self,
    #              code: Optional[int] = 200,
    #              status: Optional[bool] = True,
    #              message: Optional[Any] = None,
    #              result: Optional[Any] = None
    #              ):
    #     self.result = result
    #     self.code = code
    #     self.status = status
    #     self.message = message
        