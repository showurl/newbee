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


### 修改你的代码
```
# 这是你之前的代码
class User(models.Model):
	name = models.CharField(max_length=8, null=False)  # 名字
	user_type = models.ForeignKey(to=UserType)  # 用户类型
	groups = models.ManyToManyField(to=Group)  # 用户所在的组
```

```
# 这是你应该修改之后的代码
from newbee import newbee_model
from newbee.newbee_util.request import get_request_body_dict

@newbee_model.decorator_factory(
	action="user",  # 前端url Path中携带的action
	find_for_write_default_dict={
		"id": lambda request: get_request_body_dict(request).get("user_id")
	},  # 设置修改模型时使用id查询模型并修改
	find_for_delete_default_dict={
		"id": lambda request: get_request_body_dict(request).get("user_id")
	},  # 设置删除模型时使用id查询模型并修改
	write_success_return_data_form={
		"user": {   # 增加或修改成功时，返回的json数据的key是user
			"用户id": "id",  # 返回操作的模型的隐藏字段id，返回的key是 用户id
			"注册时间": "create_time",  # 返回操作的模型的隐藏字段create_time，返回的key是 注册时间
			"姓名": "name",  # 返回操作的模型的字段name，返回的key是 姓名
			"用户类型": {   # 返回操作的模型的关联字段user_type，返回的key是 用户类型
				"user_type": {
					"用户类型id": "id",  # 在关联的模型中，返回关联模型的隐藏字段id, 返回的key是用户类型id
					"用户类型名": "name"  # 在关联的模型中，返回关联模型的字段name, 返回的key是用户类型名
				}
			},
			"所在的用户组": {  # 返回操作的模型的关联字段groups，返回的key是 所在的用户组
				"groups": {
					"用户组id": "id",  # 在关联的模型中，返回关联模型的隐藏字段id, 返回的key是用户组id
					"用户组名": "name"  # 在关联的模型中，返回关联模型的字段name, 返回的key是用户组名
				}
			}
		}
	},
	
	can_add=True,  #该模型该接口允许进行增加操作，即接收POST请求
	can_delete=True,  #该模型该接口允许进行删除操作，即接收DELETE请求
	can_update=True,  #该模型该接口允许进行修改操作，即接收PUT请求
	can_find=True,  #该模型该接口允许进行查询操作，即接收GET请求
	
	find_return_key="users",  # 查询操作成功时，返回的json数据的key是users
	
	find_child_field_dict_list=[  # 查询操作成功时，返回的json数据携带的关联模型的数据
		# 返回key是用户类型 选择user_type字段 关联模型返回的数据是{id: user_type模型的id, 用户类型名: user_type模型的name}
		["用户类型", "user_type", ["id", {"用户类型名": "name"}]],
		# 返回key是所在的用户组 选择groups字段 关联模型返回的数据是{用户组id: groups模型的id, 用户类型名: groups模型的name}
		["所在的用户组", "groups", [{"用户组id": "id"}, {"用户组名": "name"}]],
	]
)
class User(newbee_model.NewBeeBaseModel):
	name = newbee_model.NewBeeCharField(
			new_bee_request_key="username",  # 前端传递的时候需要传递的key是username
			new_bee_response_key="username",  # 查询成功返回时的key
			new_bee_can_add=True, #支持新增时(POST请求)传递username
			new_bee_is_add_tran=True,  # 新增时必须传递username参数
			new_bee_add_key="name",  # 写入数据库时model.objects.create(name=前端传递的username值)
			new_bee_can_update=True,  # 支持修改时(PUT请求)传递username
			new_bee_update_key="name",  # 写入数据库时obj.update(name=前端传递的username值)
			new_bee_can_found=True,  # 查询该User模型成功后，返回此字段值
			new_bee_can_find_by_self=True,  # 允许通过此字段进行搜索
			new_bee_find_by_self_key='name__icontains',  # 搜索时的key是name__icontains，代表
				# model.objects.filter(name__icontains=前端传递的username值)
			max_length=8,  # 这是原来的属性
			null=False  # 这是原来的属性
		)
	user_type = newbee_model.NewBeeForeignKey(
			new_bee_request_key="type_id",  # 前端传递的时候需要传递的key是type_id
			new_bee_response_key="type_id",  # 查询成功返回时的key
			new_bee_can_add=True, #支持新增时(POST请求)传递type_id
			new_bee_add_key="user_type_id",  # 写入数据库时model.objects.create(name=前端传递的type_id值)
			new_bee_can_update=True,  # 支持修改时(PUT请求)传递type_id
			new_bee_update_key="user_type_id",  # 写入数据库时obj.update(name=前端传递的type_id值)
			new_bee_can_found=True,  # 查询该User模型成功后，返回此字段值
			new_bee_can_find_by_self=True,  # 允许通过此字段进行搜索
			new_bee_find_by_self_key='user_type_id',  # 搜索时的key是user_type_id，代表
				# model.objects.filter(user_type_id =前端传递的type_id值)
			related_name='user_set',  # 可以设置可以不设置，方便其他模型类的API可以增加或修改或查询与此模型的关系
			to=UserType, # 这是原来的属性
		)
	groups = newbee_model.NewBeeManyToManyField(
			new_bee_request_key="group_ids",  # 前端传递的时候需要传递的key是group_ids
			new_bee_response_key="group_ids",  # 查询成功返回时的key
			new_bee_can_add=True, #支持新增时(POST请求)传递group_ids
			new_bee_add_key="groups",  # 写入数据库时model.objects.create(name=前端传递的group_ids值)
			new_bee_can_update=True,  # 支持修改时(PUT请求)传递group_ids
			new_bee_update_key="groups",  # 写入数据库时obj.update(name=前端传递的group_ids值)
			new_bee_can_found=True,  # 查询该User模型成功后，返回此字段值
			new_bee_can_find_by_self=True,  # 允许通过此字段进行搜索
			new_bee_find_by_self_key='groups',  # 搜索时的key是groups，代表
				# obj.groups.add(*前端传递的group_ids值)
			related_name='group_set',  # 可以设置可以不设置，方便其他模型类的API可以增加或修改或查询与此模型的关系
			to=Group,  # 这是原来的属性
		)
```
#### 修改好之后 你将拥有以下接口
```
用户接口
path: /newbee/v1.0.1/user/data  ## 具体path根据你的配置文件而定
```

#### 功能一：增加一个用户

##### 前端传递参数表格


| 参数名  | 类型 | 是否必传  | 示例  |
|:----------|:----------|:----------|:----------|
| name    |str| 是    | 马守越    |
| type\_id    |int| 否    | 1    |
| group\_ids    |list[int]或int| 否    | [1, 2, 3]或1    |

##### 后端响应参数表格


| 参数名  | 类型 | 是否必传  | 示例  |
|:----------|:----------|:----------|:----------|
| status    |str| 是    | OK 或者 FAIL    |
| code    |int| 是    | 200    |
| data    |Object| 否    | {<br>&nbsp;&nbsp;user:{<br>&nbsp;&nbsp;&nbsp;&nbsp;用户id: 1,<br>&nbsp;&nbsp;&nbsp;&nbsp;注册时间: 2020-05-28 16\:44\:36,<br>&nbsp;&nbsp;&nbsp;&nbsp;姓名: 马守越,<br>&nbsp;&nbsp;&nbsp;&nbsp;用户类型: {<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;用户类型id: 1,<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;用户类型名: 创造者<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;},<br>&nbsp;&nbsp;&nbsp;&nbsp;用户组: [<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;用户组id: 1,<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;用户组名: 创建者组<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;},<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;用户组id: 2,<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;用户组名: NEWBEE组<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;},<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;]<br>&nbsp;&nbsp;&nbsp;&nbsp;}<br>}    |


#### 功能二：删除一个用户

##### 前端传递参数表格


| 参数名  | 类型 | 是否必传  | 示例  |
|:----------|:----------|:----------|:----------|
| user_id    |int| 是    | 1    |

##### 后端响应参数表格


| 参数名  | 类型 | 是否必传  | 示例  |
|:----------|:----------|:----------|:----------|
| status    |str| 是    | OK 或者 FAIL    |
| code    |int| 是    | 200    |



#### 功能三：修改一个用户

##### 前端传递参数表格


| 参数名  | 类型 | 是否必传  | 示例  |
|:----------|:----------|:----------|:----------|
| user_id    |int| 是    | 1    |
| name    |str| 否    | 马守越    |
| type\_id    |int| 否    | 1    |
| group\_ids    |list[int]或int| 否    | [1, 2, 3]或1    |

##### 后端响应参数表格


| 参数名  | 类型 | 是否必传  | 示例  |
|:----------|:----------|:----------|:----------|
| status    |str| 是    | OK 或者 FAIL    |
| code    |int| 是    | 200    |
| data    |Object| 否    | {<br>&nbsp;&nbsp;user:{<br>&nbsp;&nbsp;&nbsp;&nbsp;用户id: 1,<br>&nbsp;&nbsp;&nbsp;&nbsp;注册时间: 2020-05-28 16\:44\:36,<br>&nbsp;&nbsp;&nbsp;&nbsp;姓名: 马守越,<br>&nbsp;&nbsp;&nbsp;&nbsp;用户类型: {<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;用户类型id: 1,<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;用户类型名: 创造者<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;},<br>&nbsp;&nbsp;&nbsp;&nbsp;用户组: [<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;用户组id: 1,<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;用户组名: 创建者组<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;},<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;用户组id: 2,<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;用户组名: NEWBEE组<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;},<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;]<br>&nbsp;&nbsp;&nbsp;&nbsp;}<br>}    |



#### 功能四：查询用户

##### 前端传递参数表格


| 参数名  | 类型 | 是否必传  | 示例  |
|:----------|:----------|:----------|:----------|
| name    |str| 否    | 越(模糊查询)    |
| type\_id    |int| 否    | 1    |
| group\_ids    |int| 否    | 1    |

##### 后端响应参数表格


| 参数名  | 类型 | 是否必传  | 示例  |
|:----------|:----------|:----------|:----------|
| status    |str| 是    | OK 或者 FAIL    |
| code    |int| 是    | 200    |
| data    |Object| 否    | {users:[<br>&nbsp;&nbsp;{<br>&nbsp;&nbsp;&nbsp;&nbsp;id: 1,<br>&nbsp;&nbsp;&nbsp;&nbsp;username: 马守越,<br>&nbsp;&nbsp;&nbsp;&nbsp;用户类型: {<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;id: 1,<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;用户类型名: 创造者<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;},<br>&nbsp;&nbsp;&nbsp;&nbsp;用户组: [<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;用户组id: 1,<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;用户组名: 创建者组<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;},<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;用户组id: 2,<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;用户组名: NEWBEE组<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;}<br>&nbsp;&nbsp;]}   |

