from typing import Optional
from src.models.domains.basemodel import ScheduleBaseModel

class StartSchedule(ScheduleBaseModel):
    task_id: Optional[int]
    username: Optional[str] = ''
    # run_type: Optional[str] = 'manual'
    schedule_type: Optional[str] = '0 * * *'


class StopSchedule(ScheduleBaseModel):
    task_id: Optional[str] = None
    username: Optional[str] = None

