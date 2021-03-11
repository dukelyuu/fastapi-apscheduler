# fastapi with apscheduler 实现python 任务调度服务 ,默认用RedisJobStore
```
项目模板
```
```
├── docs                               # 存放文档
├── build                              # 存放项目的 Dockerfile 以及与构建相关的文件
│   └── myproject                      #
│       └── Dockerfile                 #
├── cmd                                # 存放项目的启动命令
│   └── boot.sh                        #
├── db                                 # 存放数据库脚本文件
├── tests                              # 存放测试脚本文件
├── deploy                             # 存放部署文件
│   └── demo                           #
│   └── dev                            #
│   └── test                           #
├── manuals                            # 存放多语言脚本
├── src                                # 所有的业务逻辑都应该在这个目录中
│   ├── apis                           # 所有与 API 定义相关的代码都在这个目录中
│   │   └── v1                         # 存放项目 v1 版本所有的 API 定义
│   ├── config                         # 存放配置
│   ├── dao                            # 存放数据库操作逻辑
│   ├── models                         # 存放数据库模型文件 
│   ├── modules                        # 存放模块业务代码 
│   ├── plugins                        # 存放插件代码
│   ├── utils                          # 存放业务无关公共代码
│   └── version                        # 项目版本信息目录
│       └── version                    #
├── README.md                          #
├── app.py                             # 启动文件
└── requirements.txt                   # pip libs
```

# How to use

<H2>运行服务</H2>
<H3> 运行应用</H3>

- window
  
```
pip install virtualenv -i https://pypi.doubanio.com/simple/
virtualenv env
双击 env/Scripts/activated
pip install -r requirements.txt -i https://pypi.doubanio.com/simple/
python app.py 或 uvicorn app:app --reload --port 80
```
- *nix

```
$ pip install virtualenv -i https://pypi.doubanio.com/simple/
$ virtualenv env
$ /env/Scripts/activated
$pip install -r requirements.txt -i https://pypi.doubanio.com/simple/
$ python app.py 或 uvicorn app:app --reload --port 80
```
