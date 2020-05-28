# django_NEWBEE_AutoAPI
## newbee_AutoAPI库的介绍
> 这是一个基于 Django 自动生成 增删改查数据库操作 http接口 的库，你仅仅需要在models中进行配置，就可以自动生成你想要的接口！

##  

### 如果newbee_AutoAPI库就已经配置完毕，你需要根据以下使用教程进行使用
[一、通过示例来学习](https://github.com/yuedashen88/newbee/blob/master/LearningByExample.md)<br>
[二、学习普通字段有哪些属性](https://github.com/yuedashen88/newbee/blob/master/LearningByExample.md)<br>
[三、学习关联字段有哪些属性](https://github.com/yuedashen88/newbee/blob/master/LearningByExample.md)<br>
[四、学习NEWBEE装饰器有哪些属性](https://github.com/yuedashen88/newbee/blob/master/LearningByExample.md)<br>
[回到安装教程](https://github.com/yuedashen88/newbee/blob/master/README.md)<br>



### 普通字段的属性操作
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