from datetime import datetime, timedelta
from logging import raiseExceptions
from typing import Optional
from apscheduler.schedulers.background import  BackgroundScheduler
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.schedulers.asyncio import  AsyncIOScheduler
from apscheduler.schedulers.blocking import  BlockingScheduler
from apscheduler.events import EVENT_JOB_EXECUTED,EVENT_JOB_ERROR
from pytz import  timezone, utc
from typing import  Optional, Any
from src.helpers.common_helper import  CommonHelper
from src.config import config_map
import os

env = os.environ.get('ENV', 'dev').lower()
scheduler = None 
job_stores = None 

class aps_scheduler_helper():
    def __init__(
         self,
         job_store: Optional[Any] = None,
         executor: Optional[Any] = None, 
         job_defaults: Optional[Any] = None,
         time_zone: Optional[Any] = None,
         scheduler_type: Optional[str] = 'default',
         **kwargs
     ) -> Any:
        if not executor:
            executor = {
                'default': ThreadPoolExecutor(20),
                'processpool': ProcessPoolExecutor(5)
            }
        if not job_store:
            REDIS = {
                'host': config_map.get(env).REDIS_HOST,
                'port': config_map.get(env).REDIS_PORT, #,'32360',
                'db': config_map.get(env).REDIS_DB,
                'password': CommonHelper.base64_decode(config_map.get(env).REDIS_PASSWORD)
            }
            default_redis_jobstore = RedisJobStore(**REDIS)
            job_store = {
                'redis': default_redis_jobstore
            }
        global job_stores 
        job_stores = 'redis'
            
        if not job_defaults:
            job_defaults = {
                'coalesce': False,
                'max_instances': 3
            }    
        if not time_zone:
            time_zone = utc
        init_scheduler_options ={
            "job_defaults": job_defaults,
            "jobstores": job_store,
            "executors": executor,
            "timezone": time_zone
        }
        global scheduler
        if scheduler_type == 'default':
            scheduler = BackgroundScheduler(**init_scheduler_options)
        elif scheduler_type == 'async':
            scheduler = AsyncIOScheduler(**init_scheduler_options)
        elif scheduler_type == 'block':
            scheduler = BlockingScheduler(**init_scheduler_options)
        scheduler.add_listener(self.job_execute_listener, EVENT_JOB_EXECUTED)  
        scheduler.start()
        
    def job_execute_listener(self, evt):
        print(
        "job执行job:\ncode => {}\njob.id => {}\njobstore=>{}\n时间：{}".format(
            evt.code,
            evt.job_id,
            evt.jobstore,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))
        
    @staticmethod
    def start_scheduler():
        """
         启动
        """
        if scheduler:
            scheduler.start()
        else:
            raise Exception('scheduler cant be none!')

    @staticmethod    
    def stop_scheduler():
        if scheduler:
            scheduler.shutdown()
            
    @staticmethod
    def pause_schedule(self):
        if scheduler:
            scheduler.pause()
        else:
            raise Exception('scheduler cant be none!')
    
    @staticmethod
    def pause_job( job_id:str, job_store=None):
        """暂停任务

        Args:
            job_id (str): [description]
            job_store ([type], optional): [description]. Defaults to None.

        Raises:
            Exception: [description]
            Exception: [description]

        Returns:
            [type]: [description]
        """
        if not job_id:
            raise Exception("job id cant be none!")
        if not scheduler:
            raise Exception("scheduler instance cant be none!")
        
        if  job_store:
            job = scheduler.get_job(job_id=job_id,jobstore=job_store)
            
        else:
            job = scheduler.get_job(job_id=job_id,jobstore=job_stores)
        if job:
            job.pause()
        else:
            raise Exception(f"job id:{job_id} does not exist!")
        return job
    
    @staticmethod
    def patch_pause_jobs( job_ids:list, job_store=None):
        """
            批量暂停任务

        Args:
            job_ids (list): [description]
            job_store ([type], optional): [description]. Defaults to None.

        Raises:
            Exception: [description]
            Exception: [description]
        """
        if not job_ids:
            raise Exception("job id cant be none!")
        if not scheduler:
            raise Exception("scheduler instance cant be none!")
        jobs = []
        for job_id in job_ids:
            if not job_store:
                job = scheduler.pause_job(job_id=job_id,jobstore=job_store)
            else:
                job = scheduler.pause_job(job_id=job_id,jobstore=job_stores)
            jobs.append(job)
        return jobs
    
    @staticmethod
    def resume_job(job_id:str, job_store=None):
        """重启job

        Args:
            job_id (str): [description]
            job_store ([type], optional): [description]. Defaults to None.

        Raises:
            Exception: [description]
            Exception: [description]
        """
        if not job_id:
            raise Exception("job id cant be none!")
        if not scheduler:
            raise Exception("scheduler instance cant be none!")
        
        if not job_store:
            job = scheduler.resume_job(job_id=job_id,jobstore=job_store)
        else:
            job = scheduler.resume_job(job_id=job_id,jobstore=job_stores)
        return job
    
    @staticmethod
    def remove_job(job_id):
        """删除job

        Args:
            job_id ([type]): [description]

        Raises:
            Exception: [description]
            Exception: [description]
        """
        if not job_id:
            raise Exception("job id cant be none!")
        if not scheduler:
            raise Exception("scheduler instance cant be none!")
        try:
            scheduler.remove_job(job_id=job_id,jobstore=job_stores) 
        except Exception as ex :
            raise ex.message
         
    @staticmethod
    def remove_jobs(job_ids):
        """批量删除job

        Args:
            job_ids ([type]): [description]

        Raises:
            Exception: [description]
            Exception: [description]
        """
        if not job_ids:
            raise Exception("job id cant be none!")
        if not scheduler:
            raise Exception("scheduler instance cant be none!")
        for job_id in job_ids:
            scheduler.remove_job(job_id,jobstore=job_stores)
            
    @staticmethod
    def get_job( job_id:str, job_store=None):
        """get job detail

        Args:
            job_id (str): [description]
            job_store ([type], optional): [description]. Defaults to None.

        Raises:
            Exception: [description]
            Exception: [description]

        Returns:
            [type]: [description]
        """
        if not job_id:
            raise Exception("job id cant be none!")
        if not scheduler:
            raise Exception("scheduler instance cant be none!")
        
        if not job_store:
            job = scheduler.get_job(job_id=job_id, jobstore=job_store)
        else:
            job = scheduler.get_job(job_id=job_id,jobstore=job_stores)
        return job
    
    @staticmethod
    def get_jobs( job_ids:str, job_store=None):
        """get job detail

        Args:
            job_id (str): [description]
            job_store ([type], optional): [description]. Defaults to None.

        Raises:
            Exception: [description]
            Exception: [description]

        Returns:
            [type]: [description]
        """
        if not job_ids:
            raise Exception("job ids cant be none!")
        if not scheduler:
            raise Exception("scheduler instance cant be none!")
        jobs = []
        for job_id in job_ids:
            if not job_store:
            
                job = scheduler.get_job(job_id=job_id, jobstore=job_store)
            else:
                job = scheduler.get_job(job_id=job_id,jobstore=job_stores)
            jobs.append(job)
        return jobs
    
    @staticmethod
    def get_all_jobs(  job_store=None):
        """get job detail

        Args:
           
            job_store ([type], optional): [description]. Defaults to None.

        Raises:
            Exception: [description]
            Exception: [description]

        Returns:
            [type]: [description]
        """
       
        if not scheduler:
            raise Exception("scheduler instance cant be none!")
        
        if not job_store:
            jobs = scheduler.get_jobs(jobstore=job_store)
        else:
            jobs = scheduler.get_jobs(jobstore=job_store)
        return jobs
    
    @staticmethod
    def add_corn_job(job_id, job_func, args: Optional[Any] =None, trigger_date:Optional[Any] = None):
        from apscheduler.triggers.cron import CronTrigger
        if  trigger_date:
            t = CommonHelper.convert_cronstr_to_params(trigger_date)
            trigger = CronTrigger(*t)
            
        else:
            trigger = CronTrigger(second="*")
        job = scheduler.add_job(job_func,trigger=trigger,id=job_id,args=args,jobstore=job_stores)
        return job
    
    @staticmethod    
    def add_date_job(job_id, job_func, args: Optional[Any] =None, trigger_date:Optional[Any] = None):
        from apscheduler.triggers.date import  DateTrigger
        if not trigger_date:
            trigger_date = datetime.now()+ timedelta(seconds=5)
        trigger = DateTrigger(run_date=trigger_date,timezone=utc)
        job = scheduler.add_job(id=job_id,func=job_func,trigger=trigger,args=args,jobstore=job_stores)
        return job
    @staticmethod
    def add_interval_job(job_id, job_func, args: Optional[Any] =None, trigger_date:Optional[Any] = None):
        from apscheduler.triggers.interval import  IntervalTrigger
        if not trigger_date:
            trigger_date = timedelta(seconds=1)
        trigger = IntervalTrigger(timezone=utc,seconds=trigger_date)
        job = scheduler.add_job(id=job_id,func=job_func,trigger=trigger,args=args,jobstore=job_stores)
        return job