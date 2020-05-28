# django_NEWBEE_AutoAPI
## newbee_AutoAPI库的介绍
> 这是一个基于 Django 自动生成 增删改查数据库操作 http接口 的库，你仅仅需要在models中进行配置，就可以自动生成你想要的接口！

##  

## 安装教程
1. 你可以在[https://github.com/yuedashen88/newbee/releases](https://github.com/yuedashen88/newbee/releases)中获取最新版本进行下载
1. 
	- 进入你项目的虚拟环境中, 执行命令
	- `pip install /Users/yuedashen88/Downloads/newbee-1.0.1.tar.gz`
	- 注意：你需要修改此路径为你下载后的路径
	- 如果报错, 请执行 `pip uninstall django djangorestframework pycryptodome` 后再次安装，项目会自动为你安装这三项依赖

     ![avatar](https://github.com/yuedashen88/newbee/blob/master/images/pip%E5%AE%89%E8%A3%85.png)
     ### 至此，newbee_AutoAPI库就已经安装完毕，下面你需要进行一些配置，才能使用它
##  

## 使用教程
1. 打开你项目的settings.py，在INSTALLED_APPS中添加`'rest_framework', 'newbee',`

    ![avatar](https://github.com/yuedashen88/newbee/blob/master/images/installed_apps.png)
2. 打开你项目的settings.py，新增日志配置(不配置也可以)
```
# 日志
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,  # 是否禁用logger，建议设置为False
    'formatters': {  # 日志格式，提供给handler使用，非必须，如果不设置格式，默认只会打印消息体
        'verbose': {  # 格式名称
            # INFO 2018-04-25 15:43:27,586 views 8756 123145350217728 这是一个日志
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            # INFO  这是一个日志
            'format': '%(levelname)s %(message)s'
        },
        'standard': {
            # 2018-04-25 16:40:00,195 [Thread-7:123145575223296] [myapp.log:282] [views:user_query_json_get] [INFO]-
            # 这是一个日志
            'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(module)s:%(funcName)s] [%(levelname)s]- %(message)s'
        },
    },
    'filters': {  # 过滤器，提供给handler使用，非必须
        'require_debug_true': {  # 要求DEBUG=True时才打印日志
            '()': 'django.utils.log.RequireDebugTrue',
        },

    },
    'handlers': {  # 处理器，设置日志记录方式，必须
        'console': {  # 处理器名称
            'level': 'DEBUG',  # 设置级别
            'filters': ['require_debug_true'],  # 设置过滤器，多个用逗号分割
            'class': 'logging.StreamHandler',  # 处理器，这里是控制台打印
            'formatter': 'verbose'  # 设置日志格式
        },
        'timedRotatingFile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',  # 按时间切割日志
            'filename': 'logs/pro.log',  # 日志输出文件
            'when': 'D',  # 按天分割
            'backupCount': 0,  # 保留日志份数，只保留最后5份，如果都保留，设置为0，默认就是0
            'formatter': 'standard',  # 使用哪种formatters日志格式
        },
    },
    'loggers': {  # 日志记录器
        'django.request': {
            'handlers': ['timedRotatingFile'],
            'level': 'ERROR',
            'propagate': False,  # 设置为False，表示不像其父级别传递日志内容
        },
        'pro.log': {  # 也可以这样创建logger对象，logging.getLogger('myapp.log')
            'handlers': ['console', 'timedRotatingFile'],
            'level': 'DEBUG',  # 这里的日志级别不能低于处理器中设置的日志级别
        },
    },
}
```

3. 打开你项目的urls.py，在urlpatterns列表中新增一行

    `path('', include(('newbee.urls', 'newbee'), namespace='newbee')),`

    ![avatar](https://github.com/yuedashen88/newbee/blob/master/images/urls.png)
