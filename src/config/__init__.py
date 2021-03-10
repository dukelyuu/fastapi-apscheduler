import os
import logging
import sys
from typing import List
from databases import DatabaseURL
from loguru import logger
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret
from src.core.logging import InterceptHandler

config = Config(".env")

class Config():
    ### APP
    basedir = os.path.abspath(os.path.dirname(__file__))
    APPVERSION = os.environ.get('VERSION',  'v2')
    APPNAME = os.environ.get('APPNAME',  'flask_app')
    
    ###Plugins###
    METRICS = os.environ.get('METRICS',  True)
    ###DBconfig###
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get("SSL_REDIRECT", True) #True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL',"")
    # QueuePool SQLALCHEMY_POOL_SIZE default 5
    # QueuePool SQLALCHEMY_MAX_OVERFLOW default 10

    # SQLALCHEMY_POOL_SIZE default 10
    # SQLALCHEMY_POOL_SIZE = os.environ.get('SQLALCHEMY_POOL_SIZE', 20)
    # SQLALCHEMY_MAX_OVERFLOW default 20
    # SQLALCHEMY_MAX_OVERFLOW = os.environ.get('SQLALCHEMY_MAX_OVERFLOW', 40)
    REDIS_URL = os.environ.get('REDIS_URL', "")
    # 运行时redis异常重连次数
    REDIS_RECONNECT_COUNT = 3

    SSL_REDIRECT = os.environ.get("SSL_REDIRECT", False) #False
    FLASKY_POSTS_PER_PAGE = os.environ.get("FLASKY_POSTS_PER_PAGE", 20) #20
    FLASKY_FOLLOWERS_PER_PAGE = os.environ.get("FLASKY_FOLLOWERS_PER_PAGE", 50) #50
    FLASKY_COMMENTS_PER_PAGE = os.environ.get("FLASKY_COMMENTS_PER_PAGE", 30) #30
    FLASKY_SLOW_DB_QUERY_TIME = os.environ.get("FLASKY_SLOW_DB_QUERY_TIME", 0.5) #0.5
    """JWT CONFIGS"""
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "jwt_flask_app@2019") #os.getenv("JWT_SECRET_KEY") or 
    #token有效时长 minutes为单位
    JWT_TOKEN_EXPIRES = os.environ.get("JWT_TOKEN_EXPIRES", 200)#os.getenv("JWT_TOKEN_EXPIRES") or 200
    JWT_TOKEN_EXPIRES_FOR_PIPELINE = os.environ.get("JWT_TOKEN_EXPIRES", 1440 * 7)#os.getenv("JWT_TOKEN_EXPIRES") or 200
    #refresh token有效时长 day为单位
    JWT_REFRESH_TOKEN_EXPIRES = os.environ.get("JWT_REFRESH_TOKEN_EXPIRES", 7)#os.getenv("JWT_REFRESH_TOKEN_EXPIRES") or 7
    #token黑名单
    JWT_BLACKLIST_TOKEN_CHECKS = os.environ.get("access", [])#["access"]

    """验证码有效期"""
    VERIFY_CODE_EXPIRES =  os.environ.get("VERIFY_CODE_EXPIRES", 30)#30  #minuts

    INGRESS_PATH = os.environ.get("INGRESS_PATH", '/bam')#'/bam'
    

    # 短信服务
    SMS_HOST=""
    VOICE_HOST=""
    PORT = os.environ.get("PORT", 443)
    VERSION = os.environ.get("VERSION", "v2")

    #Mail 邮件配置
    MAIL_SERVER =  os.environ.get("MAIL_SERVER", 'smtp.exmail.qq.com')
    MAIL_PORT = os.environ.get("MAIL_PORT", '465') 
    MAIL_USE_TLS =  os.environ.get("MAIL_USE_TLS", False)
    MAIL_USE_SSL =  os.environ.get("MAIL_USE_SSL", True)
    MAIL_DEBUG =   os.environ.get("MAIL_DEBUG", 0)
    MAIL_USERNAME =  os.environ.get("MAIL_USERNAME", '') 
    MAIL_PASSWORD =  os.environ.get("MAIL_PASSWORD", '') 
    MAIL_DEFAULT_SENDER =  ('AIOS', 'aios@intellif.com')
    MAIL_MAX_EMAILS =  None
    # MAIL_SUPPRESS_SEND =  'app.testing'
    MAIL_ASCII_ATTACHMENTS = False
    # 客服邮箱，用户反馈信息邮件通知客服
    MAIL_CUSTOM_SERVICE = os.environ.get("MAIL_PASSWORD", 'aios@intellif.com')
    # **********************初始化脚本静态数据***********************
    SUPPER_ADMIN_ID = 1
    INTELLIF_TENANT_ID = 1
    AIOS_SUPER_ADMIN_ROLE_KEY = 'AIOS_SUPER_ADMIN'
    # **********************初始化脚本静态数据***********************
    REDIS_CACHE_EXPIRE = 30 * 60
    REDIS_CACHE_EXPIRE_PIPELINE = 7 * 24 * 60 * 60

    # 消息中心

    MSG_BASE_URL = os.getenv("MSG_BASE_URL", "http://messagehub")

    # 私有云部署
    PRIVATE_DEPLOY = os.getenv("PRIVATE_DEPLOY", False)

   

    # 日志信息
    LOG_FILE_MAX_BYTES = 10 * 1024 * 1024
    # 轮转数量是 10 个
    LOG_FILE_BACKUP_COUNT = 10

    # 单用户登录白名单
    MUTEX_LOGIN_WHITE_LIST = ['message.get_countchange']
    HOST =  os.environ.get("HOST", '0.0.0.0')

    

  

    # from app.core.logging import InterceptHandler

    API_PREFIX = "/api"

    JWT_TOKEN_PREFIX = "Token"  # noqa: S105
    VERSION = "0.0.1"


    DEBUG: bool = config("DEBUG", cast=bool, default=False)

    DATABASE_URL: DatabaseURL = config("DB_CONNECTION", cast=DatabaseURL,default="")
    MAX_CONNECTIONS_COUNT: int = config("MAX_CONNECTIONS_COUNT", cast=int, default=10)
    MIN_CONNECTIONS_COUNT: int = config("MIN_CONNECTIONS_COUNT", cast=int, default=10)

    SECRET_KEY: Secret = config("SECRET_KEY", cast=Secret,default="")

    PROJECT_NAME: str = config("PROJECT_NAME", default="data-platform-schedule")
    ALLOWED_HOSTS: List[str] = config(
        "ALLOWED_HOSTS",
        cast=CommaSeparatedStrings,
        default="",
    )
    
    # ETL SERVICE
    ETL_SERVICE_URL = os.environ.get('ETL_SERVICE_URL', default="http://dataplatform.dev.test.com")
    
    #Airflow Service
    AIRFLOW_SERVICE_URL = os.environ.get('AIRFLOW_SERVICE_URL', default="http://airflow.test.com/")
    
    
    # logging configuration

    LOGGING_LEVEL = logging.DEBUG if DEBUG else logging.INFO
    LOGGERS = ("uvicorn.asgi", "uvicorn.access")

    logging.getLogger().handlers = [InterceptHandler()]
    for logger_name in LOGGERS:
        logging_logger = logging.getLogger(logger_name)
        logging_logger.handlers = [InterceptHandler(level=LOGGING_LEVEL)]

    logger.configure(handlers=[{"sink": sys.stderr, "level": LOGGING_LEVEL}])

    # REDIS config
    REDIS_HOST = os.environ.get('REDIS_HOST', default='192.168.20.12')
    REDIS_PORT = os.environ.get('REDIS_PORT', default=32360)
    REDIS_DB = os.environ.get('REDIS_DB', default=5)
    REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD', default='YWlyZmxvdw==')

class DevConfig(Config):
    ENV = os.environ.get("ENV", "dev")
    PORT = os.environ.get("HTTPPORT", 8080)
    DEBUG =  os.environ.get("DEBUG", False)
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_RECORD_QUERIES = False


class UnitTestConfig(Config):
    ENV = os.environ.get("ENV", "UnitTest")
    PORT = os.environ.get("HTTPPORT", 8080)
    DEBUG =  os.environ.get("DEBUG", True)
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_RECORD_QUERIES = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

class TestConfig(Config):
    ENV = os.getenv("ENV", default="test")
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_RECORD_QUERIES = False
    PORT = os.getenv("HTTPPORT", default=80)
    DEBUG =  os.getenv("DEBUG", default=False)

class DemoConfig(Config):
    ENV = os.getenv("ENV", default="demo")
    PORT = os.getenv("HTTPPORT", default=80)
    DEBUG = os.getenv("DEBUG", default=False)
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_RECORD_QUERIES = False

class ProdConfig(Config):
    ENV = os.getenv("ENV", default="proc")
    PORT = os.getenv("HTTPPORT", default=8080)
    DEBUG =  os.getenv("DEBUG", default=False)
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_RECORD_QUERIES = False

config_map = {
    'dev': DevConfig,
    'test': TestConfig,
    'proc': ProdConfig,
    'unittest': UnitTestConfig,
    'demo': DemoConfig
}

# # todo FastAPI settings 
# from pydantic import BaseSettings
# class Settings(BaseSettings):
#     API_PREFIX='/api'
#     ALLOWED_HOSTS= "*"
