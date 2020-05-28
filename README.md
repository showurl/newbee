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

## 配置教程
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


3. 在你有需要的前提下，你可以配置请求响应加密中间件，来加密前后端的数据。打开你项目的settings.py，在MIDDLEWARE中加入一条 `'newbee.newbee_middleware.DataTransMiware.DTMiddleware'`，并且在你项目根目录新建一个名为sing_key的文件，里面填写32个字符(16位数字字符串组成)，例如:d86d7bab3d6ac01ad9dc6a897652f2d

    ![avatar](https://github.com/yuedashen88/newbee/blob/master/images/MIDDLEWARE.png)

    ![avatar](https://github.com/yuedashen88/newbee/blob/master/images/sing_key.png)

4. 打开你项目的urls.py，在urlpatterns列表中新增一行

    `path('', include(('newbee.urls', 'newbee'), namespace='newbee')),`

    ![avatar](https://github.com/yuedashen88/newbee/blob/master/images/urls.png)
5. 当你首次运行你的django项目时，你会发现你项目根目录自动创建了newbee_config.ini，下面是newbee_config.ini的配置讲解

```
# 数据加密中间件配置
[DT]
# 是否允许接收json数据(未加密)
is_recv_json = True
# 是否返回加密响应
is_send_text = True
# 不包含哪些路径 格式：["newbee/v1.0.1/area/data", "newbee/v1.0.1/user/data"&&"POST", ...]
exclude_path = []

# 查询时的配置
[FIND]
# 分页查询时默认一页的行数
FINDDEFUALTPAGESIZE = 10
# URL配置
[URL]
# 填写你需要修改的PATH, 无论修改成什么, 都必须有/<str:action>/
PATH = newbee/v1.0.1/<str:action>/data

```

### 至此，newbee_AutoAPI库就已经配置完毕，你需要根据以下使用教程进行使用
##  

## 使用教程~~`(以下操作全部都在你app目录下models.py中进行)`~~
### 一、普通字段
#### 先上代码
```
# 角色
@newbee_model.decorator_factory()
class Character(newbee_model.NewBeeBaseModel):
    name = newbee_model.NewBeeCharField(new_bee_can_found=True, new_bee_can_add=True, new_bee_is_add_tran=True,
                                            new_bee_can_update=True, new_bee_update_key='name',
                                            db_column="name", max_length=48, null=True,
                                            help_text="名字")
    mobile = newbee_model.NewBeeCharField(new_bee_request_key='mobile', new_bee_response_key='mobile',
                                          new_bee_can_add=True, new_bee_add_key='mobile',
                                          new_bee_can_update=True, new_bee_update_key='mobile', new_bee_can_found=True,
                                          max_length=11, null=True,
                                          verbose_name='手机号')
    level = newbee_model.NewBeeIntegerField(new_bee_request_key='level', new_bee_response_key='level',
                                            new_bee_can_add=True, new_bee_add_key='level',
                                            new_bee_can_update=True, new_bee_update_key='level',
                                            new_bee_can_found=True, default=PNormalUser,
                                            verbose_name='角色级别')
    company = newbee_model.NewBeeForeignKey(new_bee_request_key='company_id', new_bee_can_add=True,
                                            new_bee_can_update=True, new_bee_update_key='company_id',
                                            new_bee_can_find_by_self=True,
                                            new_bee_find_by_self_key='company_id', to=Company, on_delete=models.CASCADE,
                                            null=True)
    creater = newbee_model.NewBeeCharField(new_bee_can_found=True, max_length=48, null=True, default=None,
                                           verbose_name='用户的创建者')

    class Meta:
        db_table = 'character'
```

#### 以上是数据库中的一张表，字段如下:

![avatar](https://github.com/yuedashen88/newbee/blob/master/images/character.png)

#### 通过下表，你可以了解到普通字段(无关联关系字段，比如NewBeeCharField, NewBeeIntegerField)中对比Django自带的普通字段(如CharField, IntegerField)增加的属性。
| 属性名  | 值的类型  | 属性解释  | 值的示例  |
|:----------|:----------|:----------|:----------|
|`new_bee_can_add`|`bool`|`当执行新增操作时<br>该字段是否允许传递<br>默认否`|`True`|
|`new_bee_is_add_tran `|`bool `|`当执行新增操作时，该字段是否必须传递<br>默认否`|`True `|
|`new_bee_add_key`|`str`|`当执行新增操作时<br>model.objects.create(?=value)<br>默认是请求的key(request_key)`|`name`|
|`new_bee_request_key `|`str`|`前端传递参数时<br>要求此字段的key是?`|`name`|
|`1`|`2`|`3`|`4`|
|`1`|`2`|`3`|`4`|
|`1`|`2`|`3`|`4`|
|`1`|`2`|`3`|`4`|
|`1`|`2`|`3`|`4`|
|`1`|`2`|`3`|`4`|
|`1`|`2`|`3`|`4`|
|`1`|`2`|`3`|`4`|
|`1`|`2`|`3`|`4`|
|`1`|`2`|`3`|`4`|
|`1`|`2`|`3`|`4`|
|`1`|`2`|`3`|`4`|
|`1`|`2`|`3`|`4`|
|`1`|`2`|`3`|`4`|
|`1`|`2`|`3`|`4`|


### 二、关联字段
#### 先上代码
```
# 角色
@newbee_model.decorator_factory()
class Menu(newbee_model.NewBeeBaseModel):
    path = newbee_model.NewBeeCharField(
        new_bee_can_found=True, db_column="path", max_length=48, null=True,
        help_text="path"
    )
    icon = newbee_model.NewBeeCharField(
        new_bee_can_found=True, db_column="icon", max_length=48, null=True,
        help_text="icon"
    )
    name = newbee_model.NewBeeCharField(new_bee_can_found=True, db_column="name", max_length=48, null=True,
                                        help_text="name")
    component = newbee_model.NewBeeCharField(new_bee_can_found=True, db_column="component", max_length=48, null=True,
                                             help_text="component")
    desc = newbee_model.NewBeeCharField(db_column="desc", max_length=64, null=True, help_text="菜单描述")
    pid = newbee_model.NewBeeForeignKey(to="self", null=True, on_delete=models.CASCADE,
                                        help_text="父亲id",
                                        related_name='pid_set')
    characters = newbee_model.NewBeeManyToManyField(to=Character)  # 和jwtUser 是 多对多关系

    class Meta:
        db_table = "menu"
```

#### 以上是数据库中的一张表，字段如下:

![avatar](https://github.com/yuedashen88/newbee/blob/master/images/menu.png)

#### 通过下表，你可以了解到关联关系字段(比如NewBeeManyToManyField, NewBeeForeignKey)中对比Django自带的普通字段(如ManyToManyField, ForeignKey)增加的属性。
| 属性名  | 值的类型  | 属性解释  | 值的示例  |
|:----------|:----------|:----------|:----------|
| Cell 1    | Cell 2    | Cell 3    | Cell 3    |
| Cell 1    | Cell 2    | Cell 3    | Cell 3    |

### 三、装饰器decorator_factory
#### 你会发现每一个model都加了一个装饰器，装饰器中可以填写哪些参数呢？都代表什么含义呢？请看下表！
| 属性名  | 值的类型  | 属性解释  | 值的示例  |
|:----------|:----------|:----------|:----------|
| Cell 1    | Cell 2    | Cell 3    | Cell 3    |
| Cell 1    | Cell 2    | Cell 3    | Cell 3    |


## 完成截图

![avatar](https://github.com/yuedashen88/newbee/blob/master/images/character_postman.png)

![avatar](https://github.com/yuedashen88/newbee/blob/master/images/character_response.png)

## 贡献者
yuedashen88@163.com 马守越
### 关于打赏

![avatar](https://github.com/yuedashen88/newbee/blob/master/images/zfb.png)

