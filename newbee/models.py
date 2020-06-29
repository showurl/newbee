from django.db import models

"""
是否支持逻辑删除 默认是
是否支持永久删除 默认否
action(model链接名) 默认 model.__name__.lower()
在执行增加操作时 附加的 add_dict是 默认 None 你可以这么写 {"key": lambda request: None} 或者 {"key": def func(request):pass}
在执行逻辑删除操作时 附加的 delete_dict是 默认 你可以这么写 {"key": lambda request: None} 或者 {"key": def func(request):pass}
在执行修改操作时 附加的 update_dict是 默认 你可以这么写 {"key": lambda request: None} 或者 {"key": def func(request):pass}
在执行查询操作时 附加的 find_dict是 默认 {"is_deleted": lambda request:False} 你可以这么写 {"key": lambda request: None} 或者 {"key": def func(request):pass}
在执行逻辑删除和修改操作时 通过一个字典去搜寻一条记录 默认是{"id": lambda request: request.data.get("id"),"is_deleted": lambda request:False} 你可以这么写 {"key": lambda request: None}
在执行永久删除操作时 通过一个字典去搜寻一条记录 默认是{"id": lambda request: request.data.get("id")} 你可以这么写 {"key": lambda request: None}

执行增加和修改操作时  返回刚增加或修改的记录 格式 默认 {"write_data": {"id": "id"}}  你可以这么写{"write_data": {"返回的key": "找寻的key"}}
"""


class NewBeeDeleteRecord(models.Model):
    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True)
    model_name = models.CharField(max_length=30)
    record_json = models.TextField()

    class Meta:
        db_table = "new_bee_delete_record"
