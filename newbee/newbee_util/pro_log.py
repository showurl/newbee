import logging

logger = logging.getLogger('pro.log')

"""
settings的示例：
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
            'handlers': ['timedRotatingFile'],
            'level': 'DEBUG',  # 这里的日志级别不能低于处理器中设置的日志级别
        },
    },
}


"""