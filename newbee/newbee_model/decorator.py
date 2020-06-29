from newbee.newbee_util.request import get_request_body_dict

model_dict = {}


def decorator_factory(can_delete=False, can_add=True, can_update=True, can_find=True,
                      action=None, add_default_dict=None, update_default_dict=None, find_default_dict=None,
                      find_return_key=None, add_re_realte_dict_list=None, update_re_realte_dict_list=None,
                      find_parent_field_dict_list=None, find_child_field_dict_list=None,
                      find_for_write_default_dict=None, find_for_delete_default_dict=None,
                      if_find_dict_none=None, find_id_key=None, find_add_dict_list=None,
                      write_success_return_data_form=None, set_default_add_data_to_database=None,
                      set_default_update_data_to_database=None, set_default_delete_data_to_database=None, set_default_find_data_to_database=None):
    """

    :param can_delete: 是否支持逻辑删除 默认是
    :param can_delete_forever: 是否支持永久删除 默认否
    :param action: action(model链接名) 默认 model.__name__.lower()
    :param add_default_dict: 在执行增加操作时 附加的 add_dict是 默认 None 你可以这么写 {"key": lambda request: None} 或者 {"key": def func(request):pass}
    :param on_delete_dict_list: 有关外键删除时的操作字典 默认 None 你可以这么写{"action": "foreign", "on_delete": NEWBEECASCADE, "field": "foreign"}
    :param delete_default_dict: 在执行逻辑删除操作时 附加的 delete_dict是  你可以这么写 {"key": lambda request: None} 或者 {"key": def func(request):pass}
    :param update_default_dict: 在执行修改操作时 附加的 update_dict是 默认 你可以这么写 {"key": lambda request: None} 或者 {"key": def func(request):pass}
    :param find_default_dict: 在执行查询操作时 附加的 find_dict是 默认 {"is_deleted": lambda request:False} 你可以这么写 {"key": lambda request: None} 或者 {"key": def func(request):pass}
    :param find_return_key: 查询成功  返回时的key  默认是action名加_list
    :param add_re_realte_dict_list: 增加时可以反向多对多增加的对象
    :param update_re_realte_dict_list: 修改时可以反向多对多修改的对象
    :param find_parent_field_dict_list: 在执行查询操作时 有字段为关联字段(Foreign or OneToOne or ManyToMany) 把关联字段写进去  你将会查询此条记录关于这些字段所有的child [("返回的key", "原本字段名", ["返回的模型 选取那些字段",])]
    :param find_child_field_dict_list: 在执行查询操作时 有字段为关联字段(ReForeign or ReOneToOne or ReManyToMany) 把关联字段写进去  你将会查询此条记录关于这些字段所有的child [("返回的key", "原本字段名", ["返回的模型 选取那些字段",])]
    :param find_for_write_default_dict: 在执行逻辑删除和修改操作时 通过一个字典去搜寻一条记录 默认是{"id": lambda request: request.data.get("id"),"is_deleted": lambda request:False} 你可以这么写 {"key": lambda request: None}
    :param find_for_delete_default_dict: 在执行永久删除操作时 通过一个字典去搜寻一条记录 默认是{"id": lambda request: request.data.get("id")} 你可以这么写 {"key": lambda request: None}
    :param if_find_dict_none: 执行查询操作时  如果前端传递的为空  默认添加的dict
    :param find_id_key: 查询成功时，返回的id key 默认是id
    :param find_add_dict_list: 查询成功时，返回前端增加的项
    :param write_success_return_data_form: 执行增加和修改操作时  返回刚增加或修改的记录 格式 默认 {"write_data": {"id": "id"}}  你可以这么写{"write_data": {"返回的key": "找寻的key"}}
    :param set_default_add_data_to_database: 数据库事务中新增操作
    :param set_default_update_data_to_database: 数据库事务中新增操作
    :param set_default_delete_data_to_database: 数据库事务中新增操作
    :param set_default_find_data_to_database: 数据库事务中查询操作
    :return:
    """

    def record_model(class_obj):
        if not action:
            action_ = class_obj.__name__.lower()
        else:
            action_ = action
        if not add_default_dict and add_default_dict != {}:
            add_default_dict_ = {}
        else:
            add_default_dict_ = add_default_dict
        if not update_default_dict and update_default_dict != {}:
            update_default_dict_ = {}
        else:
            update_default_dict_ = update_default_dict
        if not find_default_dict and find_default_dict != {}:
            find_default_dict_ = {"is_deleted": lambda request: False}
        else:
            find_default_dict_ = find_default_dict
        if not find_return_key:
            find_return_key_ = action_ + "_list"
        else:
            find_return_key_ = find_return_key
        if not find_parent_field_dict_list and find_parent_field_dict_list != []:
            find_parent_field_dict_list_ = []
        else:
            find_parent_field_dict_list_ = find_parent_field_dict_list

        if not add_re_realte_dict_list and add_re_realte_dict_list != []:
            add_re_realte_dict_list_ = []
        else:
            add_re_realte_dict_list_ = add_re_realte_dict_list

        if not update_re_realte_dict_list and update_re_realte_dict_list != []:
            update_re_realte_dict_list_ = []
        else:
            update_re_realte_dict_list_ = update_re_realte_dict_list

        if not find_child_field_dict_list and find_child_field_dict_list != []:
            find_child_field_dict_list_ = []
        else:
            find_child_field_dict_list_ = find_child_field_dict_list
        if not find_for_write_default_dict and find_for_write_default_dict != {}:
            find_for_write_default_dict_ = {"id": lambda request: get_request_body_dict(request).get("id"),
                                            "is_deleted": lambda request: False}
        else:
            find_for_write_default_dict_ = find_for_write_default_dict
        if not find_for_delete_default_dict and find_for_delete_default_dict != {}:
            find_for_delete_default_dict_ = {"id": lambda request: get_request_body_dict(request).get("id")}
        else:
            find_for_delete_default_dict_ = find_for_delete_default_dict
        if not write_success_return_data_form and write_success_return_data_form != {}:
            write_success_return_data_form_ = {"write_data": {"id": "id"}}
        else:
            write_success_return_data_form_ = write_success_return_data_form
        if not if_find_dict_none and if_find_dict_none != {}:
            if_find_dict_none_ = {}
        else:
            if_find_dict_none_ = if_find_dict_none
        if not find_add_dict_list and find_add_dict_list != []:
            find_add_dict_list_ = []
        else:
            find_add_dict_list_ = find_add_dict_list
        if not find_id_key:
            find_id_key_ = "id"
        else:
            find_id_key_ = find_id_key

        model_dict[action_] = {
            "model": class_obj,
            "can_delete": can_delete,
            "can_add": can_add,
            "can_update": can_update,
            "can_find": can_find,
            "add_default_dict": add_default_dict_,
            "update_default_dict": update_default_dict_,
            "find_default_dict": find_default_dict_,
            "find_return_key": find_return_key_,
            "find_parent_field_dict_list": find_parent_field_dict_list_,
            "find_child_field_dict_list": find_child_field_dict_list_,
            "find_for_write_default_dict": find_for_write_default_dict_,
            "find_for_delete_default_dict": find_for_delete_default_dict_,
            "if_find_dict_none": if_find_dict_none_,
            "find_id_key": find_id_key_,
            "find_add_dict_list": find_add_dict_list_,
            "write_success_return_data_form": write_success_return_data_form_,
            "add_re_realte_dict_list": add_re_realte_dict_list_,
            "update_re_realte_dict_list": update_re_realte_dict_list_,
            "set_default_add_data_to_database": set_default_add_data_to_database,
            "set_default_update_data_to_database": set_default_update_data_to_database,
            "set_default_delete_data_to_database": set_default_delete_data_to_database,
            "set_default_find_data_to_database": set_default_find_data_to_database,
        }

        return class_obj

    return record_model
