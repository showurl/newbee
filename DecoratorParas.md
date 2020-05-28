# django_NEWBEE_AutoAPI
## newbee_AutoAPI库的介绍
> 这是一个基于 Django 自动生成 增删改查数据库操作 http接口 的库，你仅仅需要在models中进行配置，就可以自动生成你想要的接口！

##  

### 如果newbee_AutoAPI库就已经配置完毕，你需要根据以下使用教程进行使用
[一、通过示例来学习](https://github.com/yuedashen88/newbee/blob/master/LearningByExample.md)<br>
[二、学习普通字段有哪些属性](https://github.com/yuedashen88/newbee/blob/master/NormalFieldParas.md)<br>
[三、学习关联字段有哪些属性](https://github.com/yuedashen88/newbee/blob/master/RelatedFieldParas.md)<br>
[四、学习NEWBEE装饰器有哪些属性](https://github.com/yuedashen88/newbee/blob/master/DecoratorParas.md)<br>
[回到安装教程](https://github.com/yuedashen88/newbee/blob/master/README.md)<br>



### 装饰器decorator_factory
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

