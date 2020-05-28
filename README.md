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
|**以下是请求与响应**|
|`new_bee_request_key `|`str`|`前端传递参数时`<br>`要求此字段的key是?`|`name`|
|`new_bee_response_key `|`str`|`后端返回参数时`<br>`返回此字段的key是?`|`name`|
|**以下是添加操作时可能用到的属性**|
|`new_bee_can_add`|`bool`|`当执行新增操作时`<br>`该字段是否允许传递`<br>`默认否`|`True`|
|`new_bee_is_add_tran `|`bool `|`当执行新增操作时`<br>`该字段是否必须传递`<br>`默认否`|`True `|
|`new_bee_add_key`|`str`|`当执行新增操作时`<br>`model.objects.create(?=value)`<br>`默认是请求的key(request_key)`|`name`|
|**以下是修改操作时可能用到的属性**|
|`new_bee_can_update`|`bool`|`当执行修改操作时`<br>`该字段是否允许传递`<br>`默认否`|`True`|
|`new_bee_update_key`|`str`|`当执行修改操作时`<br>`objs.update(?=value)`<br>`默认是请求的key(request_key)`|`name`|
|**以下是查询操作时可能用到的属性**|
|`new_bee_can_found`|`bool`|`当执行查询操作时`<br>`该字段是否被返回到前端`<br>`默认否`|`True`|
|`new_bee_can_find_by_self`|`bool`|`当执行查询操作时`<br>`是否允许前端传递此参数`<br>`进行数据的过滤`<br>`默认否`|`True`|
|`new_bee_find_by_self_key `|`str`|`当执行查询操作时`<br>`前端传递了此参数`<br>`使用哪个key去过滤`<br>`model.objects.filter(?=value)`<br>`无默认值`|`name__icontains`|


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
|**以下是请求与响应**|
|`new_bee_request_key `|`str`|`前端传递参数时`<br>`要求此字段的key是?`|`name`|
|`new_bee_response_key `|`str`|`后端返回参数时`<br>`返回此字段的key是?`|`name`|
|**以下是添加操作时可能用到的属性**|
|`new_bee_can_add`|`bool`|`当执行新增操作时`<br>`该字段是否允许传递`<br>`默认否`|`True`|
|`new_bee_add_key`|`str`|`当执行新增操作时`<br>`model.objects.create(?=value)`<br>`默认是请求的key(request_key)`|`name`|
|**以下是修改操作时可能用到的属性**|
|`new_bee_can_update`|`bool`|`当执行修改操作时`<br>`该字段是否允许传递`<br>`默认否`|`True`|
|`new_bee_update_key`|`str`|`当执行修改操作时`<br>`objs.update(?=value)`<br>`默认是请求的key(request_key)`|`name`|
|**以下是查询操作时可能用到的属性**|
|`new_bee_can_found`|`bool`|`当执行查询操作时`<br>`该字段是否被返回到前端`<br>`默认否`|`True`|
|`new_bee_can_find_by_self`|`bool`|`当执行查询操作时`<br>`是否允许前端传递此参数进行数据的过滤`<br>`默认否`|`True`|
|`new_bee_find_by_self_key `|`str`|`当执行查询操作时`<br>`前端传递了此参数，使用哪个key去过滤`<br>`model.objects.filter(?=value)`<br>`无默认值`|`name__icontains`|

### 三、装饰器decorator_factory
#### 你会发现每一个model都加了一个装饰器，装饰器中可以填写哪些参数呢？都代表什么含义呢？请看下表！
| 属性名  | 值的类型  | 属性解释  | 值的示例  |
|:----------|:----------|:----------|:----------|
|**以下是全局设置**|
|`action`|`str`|`前端的URL path传参中的action`<br>`以此对应一个model`<br>`默认是你模型类名的全小写`|`menu`|
|`find_for_write`<br>`_default_dict`|`dict`|`model.objects.filter(**?).update()`<br>`执行修改操作时`<br>`通过某条字典过滤结果集进行更新`<br>`默认是{"id": lambda request:`<br>`get_request_body_by_request(`<br>`request).get("id")}`<br>`注意：`<br>`1.value一定是一个带有一个参数的方法`<br>`因为我们会传递request`<br>`2.key就是filter时的key`|`{`<br>`"id": lambda request:`<br>`get_request_body_by_request(`<br>`request).get("id") or -1`<br>`}`|
|`find_for_delete`<br>`_default_dict`|`dict`|`model.objects.filter(**?).delete()`<br>`执行删除操作时`<br>`通过某条字典过滤结果集进行更新`<br>`默认是{"id": lambda request:`<br>`get_request_body_by_request(`<br>`request).get("id")}`<br>`注意：`<br>`1.value一定是一个带有一个参数的方法`<br>`因为我们会传递request`<br>`2.key就是filter时的key`|`{`<br>`"id": lambda request:`<br>`get_request_body_by_request(`<br>`request).get("id") or -1`<br>`}`|
|`write_success_`<br>`return_data_form`|`dict`|`新增和修改操作成功时`<br>`后端会返回前端新增或修改的数据`<br>`此属性将规定格式是什么`<br>`{`<br>`返回的模型key: {`<br>`返回的字段key: 字段名, `<br>`返回的关联字段key: {`<br>`关联字段名: {`<br>`关联表字段key:关联表字段名`<br>`}`<br>`}`<br>`}`<br>`}`|`{`<br>`"user": {`<br>`"id": "id",`<br>`"name": "name",`<br>`"type": {`<br>`"type": {`<br>`"id": "id",`<br>`"name": "name"`<br>`}`<br>`}`<br>`}`<br>`}`|
|**以下是添加操作可能用到的属性**|
|`can_add`|`bool`|`此接口是否允许执行添加操作`<br>`默认是True`|`False`|
|`add_default_dict`|`dict`|`执行增加操作时`<br>`默认的增加字典`<br>`model.objects.create(**增加字典)`<br>`填写此项`<br>`在你执行添加操作时`<br>`此项会增加到你的增加字典中`<br>`代码是：`<br>`add_default_dict.update(`<br>`前端传递的json字典)`<br>`默认是空`<br>`注意：`<br>`1.此字典的key是你新增字段名`<br>`2.此字典的value是一个`<br>`带有一个参数的方法`|`{`<br>`"number": `<br>`lambda request: get_random_number()`<br>`}`|
|`set_default_add`<br>`_data_to_database`|`def`|`当我们的工具解析了前端的请求`<br>`准备写入数据库时`<br>`此项为写入数据库之前执行的方法`<br>`参数和返回值(一定按照顺序返回)有:`<br>`model: 添加操作使用的数据模型类`<br>`add_dict: 添加字典`<br>`many_to_many_dict: 多对多字典`<br>`return_data_key: 添加成功时返回data字典的key`<br>`return_data_dict: 添加成功后返回的data格式`|`def add_user(model,`<br>`add_dict,`<br>`many_to_many_dict,`<br>`return_data_key,`<br>`return_data_dict):`<br>`return model,\`<br>`add_dict,\`<br>`many_to_many_dict,\`<br>`return_data_key,\`<br>`return_data_dict`|
|`add_re_realte`<br>`_dict_list`|`list`|`新增时`<br>`可以增加的反向关联对象`<br>`意思是其他模型B关联了本模型A`<br>`本模型A的POST接口也可以`<br>`添加与其他模型B的关系`<br>`结构是:`<br>`[{接收前端传递的key:`<br>`对应的反向related_name}]`<br>`注意：`<br>`1.其他模型B中关联模型A字段`<br>`建议写related_name="新名字"`<br>`方便对应的反向related_name的填写`|`@decorator_factory(`<br>`add_re_realte_dict_list=[{"b_ids":"bs"}])`<br>`class B`<br><br>`class A:`<br>`b=NewBeeManyToManyField(`<br>`to=B, related_name="bs")`|
|**以下是删除操作可能用到的属性**|
|`can_delete`|`bool `|`此接口是否允许执行删除操作`<br>`默认是False`|`True`|
|`find_for_delete`<br>`_default_dict`|`dict`|`model.objects.filter(**?).delete()`<br>`执行删除操作时`<br>`通过某条字典过滤结果集进行更新`<br>`默认是{"id": lambda request:`<br>`get_request_body_by_request(`<br>`request).get("id")}`<br>`注意：`<br>`1.value一定是一个带有一个参数的方法`<br>`因为我们会传递request`<br>`2.key就是filter时的key`|`{`<br>`"id": lambda request:`<br>`get_request_body_by_request(`<br>`request).get("id") or -1`<br>`}`|
|`set_default_delete`<br>`_data_to_database`|`def`|`当我们的工具解析了前端的请求`<br>`准备删除数据库的数据时`<br>`此项为删除数据前执行的方法`<br>`参数和返回值(一定要按照顺序返回)有:`<br>`model:从哪个模型类中删除数据`<br>`find_dict:通过什么查询数据并删除`|`def user_delete(model, find_dict):`<br>&nbsp;&nbsp;`return model, find_dict`|
|**以下是修改操作可能用到的属性**|
|`can_update`|`bool `|`此接口是否允许执行修改操作`<br>`默认是True`|`False`|
|`update_default_dict`|`dict`|`执行修改操作时`<br>`默认的修改字典`<br>`objs.update(**修改字典)`<br>`填写此项`<br>`在你执行修改操作时`<br>`此项会增加到你的修改字典中`<br>`代码是：`<br>`update_default_dict.update(`<br>`前端传递的json字典)`<br>`默认是空`<br>`注意：`<br>`1.此字典的key是你新增字段名`<br>`2.此字典的value是一个`<br>`带有一个参数的方法`|`{`<br>`"number": `<br>`lambda request: get_random_number()`<br>`}`|
|`update_re_realte`<br>`_dict_list`|`list`|`修改时`<br>`可以修改的反向关联对象`<br>`意思是其他模型B关联了本模型A`<br>`本模型A的PUT接口也可以`<br>`修改与其他模型B的关系`<br>`结构是:`<br>`[{接收前端传递的key:`<br>`对应的反向related_name}]`<br>`注意：`<br>`1.其他模型B中关联模型A字段`<br>`建议写related_name="新名字"`<br>`方便对应的反向related_name的填写`|`@decorator_factory(`<br>`update_re_realte_dict_list=[{"b_ids":"bs"}])`<br>`class B`<br><br>`class A:`<br>`b=NewBeeManyToManyField(`<br>`to=B, related_name="bs")`|
|`set_default_update`<br>`_data_to_database`|`def `|`当我们的工具解析了前端的请求`<br>`准备修改数据库时`<br>`此项为修改数据库之前执行的方法`<br>`参数和返回值(一定按照顺序返回)有:`<br>`model: 添加操作使用的数据模型类`<br>`find_for_write_default_dict:通过该字典获取查询集`<br>`update_dict: 修改字典`<br>`many_to_many_dict: 多对多字典`<br>`return_data_key: 添加成功时返回data字典的key`<br>`return_data_dict: 添加成功后返回的data格式`|`def add_user(model,`<br>`find_for_write_default_dict,`<br>`add_dict,`<br>`many_to_many_dict,`<br>`return_data_key,`<br>`return_data_dict):`<br>`return model,\`<br>`find_for_write_default_dict,`<br>`add_dict,\`<br>`many_to_many_dict,\`<br>`return_data_key,\`<br>`return_data_dict`|
|**以下是查询操作可能用到的属性**|
|`can_find`|`bool `|`此接口是否允许执行查询操作`<br>`默认是True`|`False`|
|`find_default_dict`|`dict`|`执行查询操作时`<br>`默认的查询字典`<br>`model.objects.filter(**查询字典)`<br>`填写此项`<br>`在你执行查询操作时`<br>`此项会增加到你的查询字典中`<br>`代码是：`<br>`find_default_dict.update(`<br>`前端传递的json字典)`<br>`默认是空`<br>`注意：`<br>`1.此字典的key是你新增字段名`<br>`2.此字典的value是一个`<br>`带有一个参数的方法`|`{`<br>`"type": `<br>`lambda request: `<br>`request.GET.get("type_id") or -1`<br>`}`|
|`find_return_key`|`str`|`查询成功后`<br>`会返回给前端该模型json数据`<br>`此项为填写json数据的key`|`users`|
|`find_child_field`<br>`_dict_list`|`list`|`前端请求查询该模型`<br>`以及该模型关联模型的一些数据`<br>`请配置此项`<br>`格式是：`<br>&nbsp;&nbsp;`[返回的key,`<br>&nbsp;&nbsp;&nbsp;&nbsp;`关联模型在此模型的字段名,`<br>&nbsp;&nbsp;&nbsp;&nbsp;`[关联模型的字段名,`<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`关联模型的字段名,`<br>&nbsp;&nbsp;&nbsp;&nbsp;`{`<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`返回的关联模型字段的key:关联模型字段名`<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`}`<br>&nbsp;&nbsp;`]`<br>`]`|`[`<br>&nbsp;&nbsp;`"type",`<br>&nbsp;&nbsp;`"user_type",`<br>&nbsp;&nbsp;`[`<br>&nbsp;&nbsp;&nbsp;&nbsp;`"id",`<br>&nbsp;&nbsp;&nbsp;&nbsp;`"name",`<br>&nbsp;&nbsp;&nbsp;&nbsp;` {"描述": "desc"}`<br>&nbsp;&nbsp;`]`<br>`]`|
|`if_find_`<br>`dict_none`|`dict`|`如果前端在查询该模型时`<br>`没有传递任何值`<br>`那么默认的查询字典是什么`|`{`<br>`"type_id": `<br>`lambda request: `<br>`request.GET.get("type_id") or -1`<br>`}`|
|`find_add_`<br>`dict_list`|`list`|`查询的结果想要返回其他值该怎么办`<br>`配置此项`<br>`你可以随意返回任何已有的数据`<br>`格式是：`<br>`[{要返回的key:该模型已有的字段名}]`|`[{"更新时间":"update_time"}]`|


## 完成截图

![avatar](https://github.com/yuedashen88/newbee/blob/master/images/character_postman.png)

![avatar](https://github.com/yuedashen88/newbee/blob/master/images/character_response.png)

## 贡献者
yuedashen88@163.com 马守越
### 关于打赏

![avatar](https://github.com/yuedashen88/newbee/blob/master/images/zfb.png)

