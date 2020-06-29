from django.db import transaction
import json
from newbee import newbee_model, config
from newbee.models import NewBeeDeleteRecord
from newbee.newbee_util.model_to_json import models_to_json
from newbee.newbee_util.pro_log import logger
from newbee.newbee_util.request import get_request_body_dict
from newbee.tran import status_dict


def add_util(request, action, write_database_func=None):
    # 解析request数据  先转json
    json_data = get_request_body_dict(request)
    # 转json成功
    # 拿到model信息

    model = get_model_by_model_info(action)
    add_default_dict = get_add_default_dict(action)
    write_success_return_data_form = get_write_success_return_data_form(action)
    can_add = get_can_add(action)
    if not model:
        return {"msg": "找不到%s模型" % action,
                "status": "FAIL",
                "type": action,
                "code": 404}, 404
    if not can_add:
        return {"msg": "%s模型不允许进行增加操作" % action,
                "status": "FAIL",
                "type": action,
                "code": 500}, 500
    #  组合字典
    add_dict = get_add_dict(add_default_dict, request)
    many_to_many_dict = {}
    # 非空验证
    # 获取 该 model的所有字段  看哪个 新增  要求  必传
    normal_fields = get_normal_field_list_by_model(model)
    logger.debug("增加操作的普通字段为：%s " % normal_fields)
    for field in normal_fields:
        # 获取key
        request_key = newbee_model.get_attr_by_model_field_key(model, field, "request_key")
        if not request_key:
            request_key = field
        # 先看允许传递该字段吗
        allow_request_field = newbee_model.get_attr_by_model_field_key(model, field, "new_bee_can_add")
        if not allow_request_field:
            # 看看前端是否传递了
            re_value = json_data.get(request_key)
            if re_value:
                return_data_f = status_dict.get_FAIL_BY_PARA_TYPE_4001(msg="%s字段不能传递数据" % request_key)
                return_data_f.update({
                    "status": "FAIL",
                    "type": action,
                })
                return return_data_f, 400
            else:
                continue

        # 必传验证
        if newbee_model.get_attr_by_model_field_key(model, field, "is_add_tran"):
            # 必传  去验证
            require_field = json_data.get(request_key)
            if not require_field:
                # 必传验证失败
                return_data_f = status_dict.get_FAIL_BY_PARA_NOT_ALL_4000(msg="%s字段为必传字段" % request_key)
                return_data_f.update({
                    "status": "FAIL",
                    "type": action,
                })
                return return_data_f, 400

        # 普通字段
        try:
            normal_field_value = json_data[request_key]
        except:
            continue
        else:
            create_key = newbee_model.get_attr_by_model_field_key(model, field, "new_bee_add_key")
            if not create_key:
                create_key = request_key
            add_dict[create_key] = normal_field_value
    many_to_many_fields = get_many_to_many_field_list_by_model(model)
    children_field_list = get_children_field_list_by_model(model)
    many_to_many_fields += children_field_list
    # 多对多字段
    for many_to_many_field in many_to_many_fields:
        # 获取key
        request_key = newbee_model.get_attr_by_model_field_key(model, many_to_many_field, "request_key")
        if not request_key:
            request_key = many_to_many_field
        many_to_many_request_value = json_data.get(request_key)
        # 如果前端没有传递该多对多对象
        if not many_to_many_request_value:
            continue
        create_key = newbee_model.get_attr_by_model_field_key(model, many_to_many_field, "new_bee_add_key")
        if not create_key:
            create_key = request_key
        many_to_many_dict[create_key] = many_to_many_request_value
    add_re_realte_dict_list = get_add_re_realte_dict_list(action)
    if add_re_realte_dict_list:
        for add_re_realte_dict in add_re_realte_dict_list:
            if add_re_realte_dict:
                for rek, rev in add_re_realte_dict.items():
                    many_to_many_request_value = json_data.get(rek)
                    # 如果前端没有传递该多对多对象
                    if many_to_many_request_value != [] and not many_to_many_request_value:
                        continue
                    many_to_many_dict[rev] = many_to_many_request_value
    # 执行数据库操作  增加记录  生成多对多关系
    return_data_key = [k for k, v in write_success_return_data_form.items()][0]
    return_data_form = write_success_return_data_form.get(return_data_key)
    logger.debug("增加字典是：%s" % add_dict)
    default_add_data_to_database = get_default_add_data_to_database(action=action)
    if write_database_func:
        return write_database_func(model, add_dict, many_to_many_dict, return_data_key, return_data_form,
                                   default_add_data_to_database)
    else:
        return add_data_to_database(model, add_dict, many_to_many_dict, return_data_key, return_data_form,
                                    default_add_data_to_database)


def update_util(request, action, func=None):
    """

    :param request:
    :param action:
    :return:
    """
    # 解析request数据  先转json
    json_data = get_request_body_dict(request)
    # 转json成功
    # 拿到model信息

    model = get_model_by_model_info(action)
    update_default_dict = get_update_default_dict(action)
    write_success_return_data_form = get_write_success_return_data_form(action)
    find_for_write_default_dict = get_find_for_write_default_dict(request, action)
    can_update = get_can_update(action)
    if not model:
        return {"msg": "找不到%s模型" % action,
                "status": "FAIL",
                "type": action,
                "code": 404}, 404
    if not can_update:
        return {"msg": "%s模型不允许进行修改操作" % action,
                "status": "FAIL",
                "type": action,
                "code": 500}, 500
    #  组合字典
    update_dict = get_update_dict(update_default_dict, request)
    many_to_many_dict = {}
    # 非空验证
    # 获取 该 model的所有字段  看哪个 新增  要求  必传
    normal_fields = get_normal_field_list_by_model(model)
    for field in normal_fields:
        # 获取key
        request_key = newbee_model.get_attr_by_model_field_key(model, field, "request_key")
        if not request_key:
            request_key = field
        # 先看允许传递该字段吗
        allow_request_field = newbee_model.get_attr_by_model_field_key(model, field, "new_bee_can_update")
        if not allow_request_field:
            # 看看前端是否传递了
            re_value = json_data.get(request_key)
            if re_value:
                return_data_f = status_dict.get_FAIL_BY_PARA_TYPE_4001(msg="%s字段不能传递数据" % request_key)
                return_data_f.update({
                    "status": "FAIL",
                    "type": action,
                })
                return return_data_f, 400
            else:
                continue

        # 必传验证
        if newbee_model.get_attr_by_model_field_key(model, field, "new_bee_is_update_tran"):
            # 必传  去验证
            require_field = json_data.get(request_key)
            if not require_field:
                # 必传验证失败
                return_data_f = status_dict.get_FAIL_BY_PARA_NOT_ALL_4000(msg="%s字段为必传字段" % request_key)
                return_data_f.update({
                    "status": "FAIL",
                    "type": action, })
                return return_data_f, 400

                # 普通字段
        try:
            normal_field_value = json_data[request_key]
        except:
            continue
        else:
            # if not normal_field_value:
            #     continue
            # else:
            create_key = newbee_model.get_attr_by_model_field_key(model, field, "new_bee_update_key")
            if not create_key:
                create_key = request_key
            update_dict[create_key] = normal_field_value
    many_to_many_fields = get_many_to_many_field_list_by_model(model)
    children_field_list = get_children_field_list_by_model(model)
    many_to_many_fields += children_field_list
    # 多对多字段
    for many_to_many_field in many_to_many_fields:
        # 获取key
        request_key = newbee_model.get_attr_by_model_field_key(model, many_to_many_field, "request_key")
        if not request_key:
            request_key = many_to_many_field
        many_to_many_request_value = json_data.get(request_key)
        # 如果前端没有传递该多对多对象
        if many_to_many_request_value == []:
            create_key = newbee_model.get_attr_by_model_field_key(model, many_to_many_field, "new_bee_update_key")
            if not create_key:
                create_key = request_key
            many_to_many_dict[create_key] = []
        elif many_to_many_request_value == None:
            continue
        else:
            create_key = newbee_model.get_attr_by_model_field_key(model, many_to_many_field, "new_bee_update_key")
            if not create_key:
                create_key = request_key
            many_to_many_dict[create_key] = many_to_many_request_value

    update_re_realte_dict_list = get_update_re_realte_dict_list(action)
    logger.debug("update_re_realte_dict_list: % s" % update_re_realte_dict_list)
    if update_re_realte_dict_list:
        for update_re_realte_dict in update_re_realte_dict_list:
            if update_re_realte_dict:
                for rek, rev in update_re_realte_dict.items():
                    many_to_many_request_value = json_data.get(rek)
                    # 如果前端没有传递该多对多对象
                    if many_to_many_request_value != [] and not many_to_many_request_value:
                        continue
                    many_to_many_dict[rev] = many_to_many_request_value
    # 执行数据库操作  增加记录  生成多对多关系
    return_data_key = [k for k, v in write_success_return_data_form.items()][0]
    return_data_form = write_success_return_data_form.get(return_data_key)
    default_update_data_to_database = get_default_update_data_to_database(action)
    if func:
        return func(model, find_for_write_default_dict, update_dict, many_to_many_dict, return_data_key,
                    return_data_form, default_update_data_to_database)
    return update_data_to_database(model, find_for_write_default_dict, update_dict, many_to_many_dict, return_data_key,
                                   return_data_form, default_update_data_to_database)


def find_util(request, action, page=0, pageSize=config.FINDDEFUALTPAGESIZE, order_by="id"):
    """

    :param request:
    :param action:
    :return:
    """
    # 解析request数据  先转json
    json_data = get_request_body_dict(request)
    if not json_data:
        json_data = request.GET
    # 转json成功
    # 判断前端是否传递id
    request_id = json_data.get("id")
    page = json_data.get("page") or page
    pageSize = json_data.get("pageSize") or json_data.get("page_size") or pageSize
    order_by = json_data.get("order_by") or order_by
    # 拿到model信息
    model = get_model_by_model_info(action)  # 模型
    find_default_dict = get_find_default_dict(request, action)  # 查询附加{"is_deleted": False}
    find_parent_field_list = get_find_parent_field_dict_list(action)  # 返回的父亲字段
    find_child_field_list = get_find_child_field_dict_list(action)  # 返回的孩子字段
    find_return_key = get_find_return_key(action)  # 查询成功 组成json时 的key  默认为 action+"_list"
    find_response_normal_field_dict = get_find_response_normal_field_dict(model)
    can_find = get_can_find(action)
    find_add_dict_list = get_find_add_dict(action)
    id_key = get_find_id_key(action)  # 默认是id
    if not model:
        return {"msg": "找不到%s模型" % action,
                "status": "FAIL",
                "type": action,
                "code": 404}, 404
    if not can_find:
        return {"msg": "%s模型不允许进行查询操作" % action,
                "status": "FAIL",
                "type": action,
                "code": 500}, 500
    # 先组成查询字典
    find_request_allow_field_dict = get_find_request_allow_field_dict(model)
    find_dict__ = find_default_dict if find_default_dict else {}
    find_dict = find_dict__.copy()
    find_data_list = []
    for k, v in find_request_allow_field_dict.items():
        value = json_data.get(v.get("request_key"))
        if not value:
            continue
        # 组字典
        find_dict[v.get("find_by_self_key")] = value
    # 去查询
    if request_id:
        find_dict = {
            "id": request_id
        }
    if find_dict == find_dict__:
        find_dict.update(get_if_find_dict_none(request, action))
    logger.debug("查询字典是: %s" % find_dict)
    set_default_find_data_to_database = get_set_default_find_data_to_database(action=action)
    if set_default_find_data_to_database:
        find_dict = set_default_find_data_to_database(find_dict)
    if not find_dict:
        objs = model.objects.all().order_by(order_by)
    else:
        objs = model.objects.filter(**find_dict).order_by(order_by)
    # 拼装查询数据
    for obj in objs:
        obj_data = {}
        obj_data[id_key] = obj.id
        for find_add_dict in find_add_dict_list:
            for k, v in find_add_dict.items():
                obj_data[k] = obj.__dict__[v]
        for k, v in find_response_normal_field_dict.items():
            response_key = v.get("response_key")
            if not response_key.endswith("&json"):
                obj_data[v.get("response_key")] = obj.__dict__[k]
            else:
                value__ = obj.__dict__[k]
                obj_data[response_key[:-5]] = json.loads(value__) if value__ else None
        if find_parent_field_list:
            for find_parent_field in find_parent_field_list:
                key, this_field_name, new_model_fields = find_parent_field
                try:
                    new_models = getattr(obj, this_field_name).all()
                    new_model_values = []
                    for new_model in new_models:
                        new_model_value = {}
                        for nk, nv in new_model.__dict__.items():
                            for new_model_field in new_model_fields:
                                if isinstance(new_model_field, dict):
                                    for dk, dv in new_model_field.items():
                                        if nk == dv:
                                            if dk.endswith("&json"):
                                                new_model_value[dk[:-5]] = json.loads(nv) if nv else None
                                            else:
                                                new_model_value[dk] = nv
                            if nk in new_model_fields:
                                new_model_value[nk] = nv
                            elif nk+"&json" in new_model_fields:
                                new_model_value[nk] = json.loads(nv) if nv else None
                        if new_model_value:
                            new_model_values.append(new_model_value)
                    if new_model_values:
                        obj_data[key] = new_model_values
                except AttributeError:
                    new_model = getattr(obj, this_field_name)
                    new_model_value = {}
                    for nk, nv in new_model.__dict__.items():
                        if nk in new_model_fields:
                            new_model_value[nk] = nv
                        elif nk + "&json" in new_model_fields:
                            new_model_value[nk] = json.loads(nv) if nv else None
                    obj_data[key] = new_model_value
        if find_child_field_list:
            for find_parent_field in find_child_field_list:
                key, this_field_name, new_model_fields = find_parent_field
                try:
                    new_models = getattr(obj, this_field_name).all()
                    new_model_values = []
                    for new_model in new_models:
                        new_model_value = {}
                        for nk, nv in new_model.__dict__.items():
                            for new_model_field in new_model_fields:
                                if isinstance(new_model_field, dict):
                                    for dk, dv in new_model_field.items():
                                        if nk == dv:
                                            if dk.endswith("&json"):
                                                new_model_value[dk[:-5]] = json.loads(nv) if nv else None
                                            else:
                                                new_model_value[dk] = nv
                            if nk in new_model_fields:
                                new_model_value[nk] = nv
                            elif nk + "&json" in new_model_fields:
                                new_model_value[nk] = json.loads(nv) if nv else None
                        if new_model_value:
                            new_model_values.append(new_model_value)
                    if new_model_values:
                        obj_data[key] = new_model_values
                except AttributeError:
                    new_model = getattr(obj, this_field_name)
                    if new_model:
                        # print(new_model)
                        new_model_value = {}
                        for nk, nv in new_model.__dict__.items():
                            if nk in new_model_fields:
                                new_model_value[nk] = nv
                            elif nk + "&json" in new_model_fields:
                                new_model_value[nk] = json.loads(nv) if nv else None
                        obj_data[key] = new_model_value
        if obj_data:
            find_data_list.append(obj_data)
    if page == 0:
        return {
                   "msg": "查询成功",
                   "code": 200,
                   "status": "OK",
                   "type": action,
                   "data": {find_return_key: models_to_json(find_data_list)}
               }, 200
    else:
        # 分页
        page = int(page)
        pageSize = int(pageSize)
        range_start = (page - 1) * pageSize  # 开始下标
        range_end = page * pageSize  # 结束下标
        max_len = len(find_data_list)  # 数据总行数
        page_count = int(max_len / pageSize) + (1 if max_len % pageSize else 0)  # 总页数
        if page > page_count:  # page超出下标  下标越界
            return status_dict.get_FAIL_BY_NOT_FOUND_404(), 404
        if range_start <= range_end < 0:  # pageSize不正常
            range_start = range_end = 0
        model_data_page = find_data_list[range_start:min(range_end, page_count)]
        return {
                   "msg": "查询成功",
                   "code": 200,
                   "status": "OK",
                   "type": action,
                   "page": page,
                   "page_count": page_count,
                   "data": {find_return_key: models_to_json(model_data_page)}
               }, 200


def delete_util(request, action):
    """

    :param request:
    :param action:
    :return:
    """
    model = get_model_by_model_info(action)  # 模型
    can_delete = get_can_delete(action)
    if not can_delete:
        return {
                   "msg": "%s模型不允许删除" % action,
                   "code": 403,
                   "status": "FAIL",
                   "type": action,
               }, 403
    find_for_delete_default_dict = get_find_for_delete_default_dict(request, action)
    if not find_for_delete_default_dict:
        return {
                   "msg": "%s模型没有设置删除条件" % action,
                   "code": 500,
                   "status": "FAIL",
                   "type": action,
               }, 500
    default_delete_data_to_database = get_default_delete_data_to_database(action=action)
    return delete_data_to_database(model, find_dict=find_for_delete_default_dict,
                                   set_default_delete_data_to_database=default_delete_data_to_database)


def get_find_request_allow_field_dict(model):
    """

    :param model:
    :return:
    """
    normal_fields = get_normal_field_list_by_model(model)  # 普通字段
    many_to_many_fields = get_many_to_many_field_list_by_model(model)  # 多对多字段
    find_request_allow_field_dict = {}
    for normal_field in normal_fields:
        request_key = newbee_model.get_attr_by_model_field_key(model, normal_field, "request_key")
        can_find_by_self = newbee_model.get_attr_by_model_field_key(model, normal_field, "can_find_by_self")
        find_by_self_key = newbee_model.get_attr_by_model_field_key(model, normal_field, "find_by_self_key")
        is_found_as_foreign_return = newbee_model.get_attr_by_model_field_key(model, normal_field,
                                                                              "is_found_as_foreign_return")
        if can_find_by_self:
            find_request_allow_field_dict[normal_field] = {
                "request_key": request_key,
                "find_by_self_key": find_by_self_key or request_key or normal_field,
                "is_found_as_foreign_return": is_found_as_foreign_return,
            }
    for many_to_many_field in many_to_many_fields:
        request_key = newbee_model.get_attr_by_model_field_key(model, many_to_many_field, "request_key")
        can_find_by_self = newbee_model.get_attr_by_model_field_key(model, many_to_many_field, "can_find_by_self")
        find_by_self_key = many_to_many_field  # 可能要加上__id
        if can_find_by_self:
            find_request_allow_field_dict[many_to_many_field] = {
                "request_key": request_key,
                "find_by_self_key": find_by_self_key,
            }
    return find_request_allow_field_dict


def get_find_response_normal_field_dict(model):
    """

    :param model:
    :return:
    """
    normal_fields = get_normal_field_list_by_model(model)  # 普通字段

    find_response_allow_fields = {}
    for normal_field in normal_fields:
        response_key = newbee_model.get_attr_by_model_field_key(model, normal_field, "response_key")
        can_found = newbee_model.get_attr_by_model_field_key(model, normal_field, "can_found")
        is_found_as_foreign_return = newbee_model.get_attr_by_model_field_key(model, normal_field,
                                                                              "is_found_as_foreign_return")
        if can_found:
            find_response_allow_fields[normal_field] = {
                "response_key": response_key or normal_field,
                "is_found_as_foreign_return": is_found_as_foreign_return,
            }

    return find_response_allow_fields


def get_model_info(action):
    """
    通过action找到模型信息
    :param action:
    :return:
    """
    return newbee_model.model_dict.get(action)


def get_model_by_model_info(action=None, info_dict=None):
    """
    通过action或模型信息找到该模型
    :param action:
    :param info_dict:
    :return:
    """
    if not info_dict:
        return get_model_info(action).get("model")
    return info_dict.get("model")


def get_default_update_data_to_database(action=None, info_dict=None):
    """
    通过action或模型信息找到该模型
    :param action:
    :param info_dict:
    :return:
    """
    if not info_dict:
        return get_model_info(action).get("set_default_update_data_to_database")
    return info_dict.get("set_default_update_data_to_database")


def get_add_default_dict(action=None, info_dict=None):
    """
    通过action或模型信息找到新增默认字典
    :param action:
    :param info_dict:
    :return:
    """
    if not info_dict:
        return get_model_info(action).get("add_default_dict")
    return info_dict.get("add_default_dict")


def get_update_default_dict(action=None, info_dict=None):
    """
    通过action或模型信息找到新增默认字典
    :param action:
    :param info_dict:
    :return:
    """
    if not info_dict:
        return get_model_info(action).get("update_default_dict")
    return info_dict.get("update_default_dict")


def get_write_success_return_data_form(action=None, info_dict=None):
    """
    通过action或模型信息找到新增成功返回格式
    :param action:
    :param info_dict:
    :return:
    """
    if not info_dict:
        return get_model_info(action).get("write_success_return_data_form")
    return info_dict.get("write_success_return_data_form")


def get_add_re_realte_dict_list(action=None, info_dict=None):
    """
    通过action或模型信息找到新增成功返回格式
    :param action:
    :param info_dict:
    :return:
    """
    if not info_dict:
        return get_model_info(action).get("add_re_realte_dict_list")
    return info_dict.get("add_re_realte_dict_list")


def get_update_re_realte_dict_list(action=None, info_dict=None):
    """
    通过action或模型信息找到新增成功返回格式
    :param action:
    :param info_dict:
    :return:
    """
    if not info_dict:
        return get_model_info(action).get("update_re_realte_dict_list")
    return info_dict.get("update_re_realte_dict_list")


def get_can_add(action=None, info_dict=None):
    """
    通过action或模型信息找到新增成功返回格式
    :param action:
    :param info_dict:
    :return:
    """
    if not info_dict:
        return get_model_info(action).get("can_add")
    return info_dict.get("can_add")


def get_can_delete(action=None, info_dict=None):
    """
    通过action或模型信息找到新增成功返回格式
    :param action:
    :param info_dict:
    :return:
    """
    if not info_dict:
        return get_model_info(action).get("can_delete")
    return info_dict.get("can_delete")


def get_can_update(action=None, info_dict=None):
    """
    通过action或模型信息找到新增成功返回格式
    :param action:
    :param info_dict:
    :return:
    """
    if not info_dict:
        return get_model_info(action).get("can_update")
    return info_dict.get("can_update")


def get_can_find(action=None, info_dict=None):
    """
    通过action或模型信息找到新增成功返回格式
    :param action:
    :param info_dict:
    :return:
    """
    if not info_dict:
        return get_model_info(action).get("can_find")
    return info_dict.get("can_find")


def get_default_add_data_to_database(action=None, info_dict=None):
    """
    通过action或模型信息找到新增成功返回格式
    :param action:
    :param info_dict:
    :return:
    """
    if not info_dict:
        return get_model_info(action).get("set_default_add_data_to_database")
    return info_dict.get("set_default_add_data_to_database")


def get_find_parent_field_dict_list(action=None, info_dict=None):
    """
    通过action或模型信息找到新增成功返回格式
    :param action:
    :param info_dict:
    :return:
    """
    if not info_dict:
        return get_model_info(action).get("find_parent_field_dict_list")
    return info_dict.get("find_parent_field_dict_list")


def get_find_child_field_dict_list(action=None, info_dict=None):
    """
    通过action或模型信息找到新增成功返回格式
    :param action:
    :param info_dict:
    :return:
    """
    if not info_dict:
        return get_model_info(action).get("find_child_field_dict_list")
    return info_dict.get("find_child_field_dict_list")


def get_find_return_key(action=None, info_dict=None):
    """
    通过action或模型信息找到新增成功返回格式
    :param action:
    :param info_dict:
    :return:
    """
    if not info_dict:
        return get_model_info(action).get("find_return_key")
    return info_dict.get("find_return_key")


def get_find_id_key(action=None, info_dict=None):
    """
    通过action或模型信息找到新增成功返回格式
    :param action:
    :param info_dict:
    :return:
    """
    if not info_dict:
        return get_model_info(action).get("find_id_key")
    return info_dict.get("find_id_key")


def get_find_add_dict(action=None, info_dict=None):
    """
    通过action或模型信息找到新增成功返回格式
    :param action:
    :param info_dict:
    :return:
    """
    if not info_dict:
        return get_model_info(action).get("find_add_dict_list")
    return info_dict.get("find_add_dict_list")


def get_default_delete_data_to_database(action=None, info_dict=None):
    """
    通过action或模型信息找到新增成功返回格式
    :param action:
    :param info_dict:
    :return:
    """
    if not info_dict:
        return get_model_info(action).get("set_default_delete_data_to_database")
    return info_dict.get("set_default_delete_data_to_database")

def get_set_default_find_data_to_database(action=None, info_dict=None):
    """
    通过action或模型信息找到新增成功返回格式
    :param action:
    :param info_dict:
    :return:
    """
    if not info_dict:
        return get_model_info(action).get("set_default_find_data_to_database")
    return info_dict.get("set_default_find_data_to_database")


def get_find_default_dict(request, action=None, info_dict=None):
    """
    通过action或模型信息找到新增成功返回格式
    :param request:
    :param action:
    :param info_dict:
    :return:
    """
    if not info_dict:
        find_default_dict_ = get_model_info(action).get("find_default_dict")
    else:
        find_default_dict_ = info_dict.get("find_default_dict")
    find_default_dict = {}
    if find_default_dict_:
        for k, v in find_default_dict_.items():
            find_default_dict[k] = v(request)
    return find_default_dict


def get_if_find_dict_none(request, action=None, info_dict=None):
    """
    通过action或模型信息找到新增成功返回格式
    :param request:
    :param action:
    :param info_dict:
    :return:
    """
    if not info_dict:
        find_default_dict_ = get_model_info(action).get("if_find_dict_none")
    else:
        find_default_dict_ = info_dict.get("if_find_dict_none")
    find_default_dict = {}
    if find_default_dict_:
        for k, v in find_default_dict_.items():
            find_default_dict[k] = v(request)
    return find_default_dict


def get_delete_default_dict(request, action=None, info_dict=None):
    """

    :param request:
    :param action:
    :param info_dict:
    :return:
    """
    if not info_dict:
        find_default_dict_ = get_model_info(action).get("delete_default_dict")
    else:
        find_default_dict_ = info_dict.get("delete_default_dict")
    find_default_dict = {}
    if find_default_dict_:
        for k, v in find_default_dict_.items():
            find_default_dict[k] = v(request)
    return find_default_dict


def get_find_for_delete_default_dict(request, action=None, info_dict=None):
    """
    通过action或模型信息找到新增成功返回格式
    :param action:
    :param info_dict:
    :return:
    """
    if not info_dict:
        find_for_write_default_dict = {}
        find_for_write_default_dict_ = get_model_info(action).get("find_for_delete_default_dict")
        for k, v in find_for_write_default_dict_.items():
            find_for_write_default_dict[k] = v(request)
        return find_for_write_default_dict
    find_for_write_default_dict = {}
    find_for_write_default_dict_ = info_dict.get("find_for_delete_default_dict")
    for k, v in find_for_write_default_dict_.items():
        find_for_write_default_dict[k] = v(request)
    return find_for_write_default_dict


def get_find_for_write_default_dict(request, action=None, info_dict=None):
    """
    通过action或模型信息找到新增成功返回格式
    :param action:
    :param info_dict:
    :return:
    """
    if not info_dict:
        find_for_write_default_dict = {}
        find_for_write_default_dict_ = get_model_info(action).get("find_for_write_default_dict")
        for k, v in find_for_write_default_dict_.items():
            find_for_write_default_dict[k] = v(request)
        return find_for_write_default_dict
    find_for_write_default_dict = {}
    find_for_write_default_dict_ = info_dict.get("find_for_write_default_dict")
    for k, v in find_for_write_default_dict_.items():
        find_for_write_default_dict[k] = v(request)
    return find_for_write_default_dict


def get_add_dict(add_default_dict, request):
    """
    组合新增字典
    :param add_default_dict:
    :param request:
    :return:
    """
    add_dict = {}
    if add_default_dict:
        for k, v in add_default_dict.items():
            add_dict[k] = v(request)
    return add_dict


def get_update_dict(update_default_dict, request):
    """
    组合新增字典
    :param add_default_dict:
    :param request:
    :return:
    """
    update_dict = {}
    if update_default_dict:
        for k, v in update_default_dict.items():
            update_dict[k] = v(request)
    return update_dict


def get_normal_field_list_by_model(model):
    """
    通过model获取该model的所有普通字段
    :param model:
    :return:
    """
    return [field.name for field in model._meta.fields if
            (isinstance(field, newbee_model.NewBeeFieldBase) or isinstance(field, newbee_model.NewBeeRelatedBase))]


def get_many_to_many_field_list_by_model(model):
    """
    通过model获取该model的所有多对多字段
    :param model:
    :return:
    """
    return [field.name for field in model._meta.many_to_many if isinstance(field, newbee_model.NewBeeManyToManyField)]


def get_children_field_list_by_model(model, prefix="", suffix="_list"):
    children_field_list = []
    for name, v in model.__dict__.items():
        if name.startswith(prefix) and name.endswith(suffix):
            children_field_list.append(name)
    return children_field_list


def add_data_to_database(model, add_dict, many_to_many_dict, return_data_key, return_data_dict,
                         default_add_data_to_database=None):
    """
    增加一条记录到数据库
    :param model:
    :param add_dict:
    :param many_to_many_dict:
    :param return_data_dict:
    :return:
    """
    sid = transaction.savepoint()  # 开启事务设置事务保存点
    try:
        if default_add_data_to_database:
            model, add_dict, many_to_many_dict, return_data_key, return_data_dict = default_add_data_to_database(model,
                                                                                                                 add_dict,
                                                                                                                 many_to_many_dict,
                                                                                                                 return_data_key,
                                                                                                                 return_data_dict)
        obj = model.objects.create(**add_dict)
        for k, v in many_to_many_dict.items():
            attr = getattr(obj, k)
            if isinstance(v, list):
                v = [int(l) for l in v]
                attr.add(*v)
            else:
                attr.add(int(v))
    except Exception as e:
        transaction.savepoint_rollback(sid)  # 失败回滚事务(如果数据库操作发生异常，回滚到设置的事务保存点)
        return {
                   # "msg": "%s文件%s行发生%s错误" % (
                   #     e.__traceback__.tb_frame.f_globals["__file__"], e.__traceback__.tb_lineno, e),
                   "msg": "%s" % e,
                   "code": status_dict.SERVER_ERROR,
                   "status": "FAIL",
                   "type": model.__name__,
               }, 500
    else:
        transaction.savepoint_commit(sid)  # 如果没有异常，成功提交事物
        add_data = get_model_data_by_id(model=model, id=obj.id,
                                        return_data_dict=return_data_dict)
        logger.info("%s模型%s添加了一条数据%s成功" % (model.__str__, return_data_key, str(add_dict)))
        if not add_data:
            return_json = status_dict.get_ADD_SUCCESS_2000(msg="添加成功, 但查询新增数据时失败")
            return_json.update({

                "status": "OK",
                "type": model.__name__,
            })
        else:
            return_json = status_dict.get_ADD_SUCCESS_2000()
            return_json.update({

                "status": "OK",
                "type": model.__name__,
            })
        data = {}
        data[return_data_key] = models_to_json(data=add_data)
        return_json["data"] = data
        return return_json, 200


def update_data_to_database(model, find_for_write_default_dict, update_dict, many_to_many_dict, return_data_key,
                            return_data_dict, default_update_data_to_database=None):
    """
    增加一条记录到数据库
    :param model:
    :param add_dict:
    :param many_to_many_dict:
    :param return_data_dict:
    :return:
    """
    logger.debug("更新操作的多对多字典：%s " % many_to_many_dict)
    sid = transaction.savepoint()  # 开启事务设置事务保存点
    try:
        if default_update_data_to_database:
            logger.debug("执行default_update_data_to_database: %s" % default_update_data_to_database)
            model, find_for_write_default_dict, update_dict, many_to_many_dict, return_data_key, \
            return_data_dict = default_update_data_to_database(
                model, find_for_write_default_dict, update_dict, many_to_many_dict, return_data_key,
                return_data_dict)
        logger.debug("更新的查询字典是: %s" % find_for_write_default_dict)
        logger.debug("更新字典是: %s" % update_dict)
        objs = model.objects.filter(**find_for_write_default_dict)
        if not objs:
            return_data_f = status_dict.get_FAIL_BY_NOTHING_TO_DO_4040("没找到需要修改的对象")
            return_data_f.update({

                "status": "FAIL",
                "type": model.__name__,
            })
            return return_data_f, 400
        objs.update(**update_dict)
        for obj in objs:
            for k, v in many_to_many_dict.items():
                attr = getattr(obj, k)
                attr.clear()
                if isinstance(v, list):
                    v = [int(l) for l in v]
                    attr.add(*v)
                else:
                    attr.add(int(v))
    except Exception as e:
        transaction.savepoint_rollback(sid)  # 失败回滚事务(如果数据库操作发生异常，回滚到设置的事务保存点)
        return {
                   # "msg": "%s文件%s行发生%s错误" % (
                   #     e.__traceback__.tb_frame.f_globals["__file__"], e.__traceback__.tb_lineno, e),
                   "msg": "%s" % e,
                   "code": status_dict.SERVER_ERROR,
                   "status": "FAIL",
                   "type": model.__name__,
               }, 500
    else:
        transaction.savepoint_commit(sid)  # 如果没有异常，成功提交事物
        logger.info("%s模型修改了一条数据%s, %s成功" % (model.__str__, str(find_for_write_default_dict), str(update_dict)))
        if objs.count() > 1:
            update_data = get_model_data_by_ids(model=model, ids=[obj.id for obj in objs],
                                                return_data_dict=return_data_dict)
        else:
            update_data = get_model_data_by_id(model=model, id=objs[0].id,
                                               return_data_dict=return_data_dict)
        if not update_data:
            return_json = status_dict.get_UPDATE_SUCCESS_2002(msg="修改成功, 但查询新增数据时失败")
            return_json.update({
                "status": "OK",
                "type": model.__name__, })
        else:
            return_json = status_dict.get_UPDATE_SUCCESS_2002()
            return_json.update({

                "status": "OK",
                "type": model.__name__,
            })
        return_json["data"] = {
            return_data_key: models_to_json(data=update_data)
        }
        return return_json, 200


def delete_data_to_database(model, find_dict, set_default_delete_data_to_database=None):
    """

    :param model:
    :param find_dict:
    :return:
    """
    sid = transaction.savepoint()  # 开启事务设置事务保存点
    try:
        if set_default_delete_data_to_database:
            model, find_dict = set_default_delete_data_to_database(model, find_dict)
        objs = model.objects.filter(**find_dict)
        if not objs:
            return_json_j = status_dict.get_FAIL_BY_NOTHING_TO_DO_4040("没找到需要删除的对象")
            return_json_j.update({

                "status": "FAIL",
                "type": model.__name__,
            })
            return return_json_j, 400
            # 模型备份
        for obj in objs:
            NewBeeDeleteRecord.objects.create(model_name=model.__name__, record_json=json.dumps(models_to_json(obj)))
        objs.delete()

    except Exception as e:
        transaction.savepoint_rollback(sid)  # 失败回滚事务(如果数据库操作发生异常，回滚到设置的事务保存点)
        return {
                   # "msg": "%s文件%s行发生%s错误" % (
                   #     e.__traceback__.tb_frame.f_globals["__file__"], e.__traceback__.tb_lineno, e),
                   "msg": "%s" % e,
                   "code": status_dict.SERVER_ERROR,
                   "status": "FAIL",
                   "type": model.__name__,
               }, 500
    else:
        transaction.savepoint_commit(sid)  # 如果没有异常，成功提交事物
        logger.info("%s模型删除了一条数据%s成功" % (model.__str__, str(find_dict)))
        return_json = status_dict.get_DELETE_SUCCESS_2001()
        return_json.update({

            "status": "OK",
            "type": model.__name__,
        })
        return return_json, 200


def get_model_data_by_id(model, id, return_data_dict):
    """
    通过id获取一条数据
    :param model:
    :param id:
    :param return_data_dict: 返回的data字段列表
    :return:
    """
    records = model.objects.filter(id=id)
    if not records:
        return None
    # 查询成功
    record = records[0]
    return_data = {}
    if return_data_dict and isinstance(return_data_dict, dict):
        if return_data_dict.get("remove_return"):
            return_data_dict.pop("remove_return")
            return return_data_dict
        for k, v in return_data_dict.items():
            if isinstance(v, str):
                try:
                    obj_field = getattr(record, v)
                except:
                    return_data[k] = v
                else:
                    if obj_field != None:
                        return_data[k] = obj_field
                    else:
                        return_data[k] = v
            elif isinstance(v, dict):
                return_dict = {}
                return_list = []
                for kk, vv in v.items():
                    obj_field = getattr(record, kk)
                    if obj_field:
                        try:
                            obj_fields = obj_field.all()
                            for obj_field_a in obj_fields:
                                dict_a = {}
                                for kkk, vvv in vv.items():
                                    value = getattr(obj_field_a, vvv)
                                    if kkk.endswith("&json"):
                                        dict_a[kkk[:-5]] = json.loads(value) if value else None
                                    else:
                                        dict_a[kkk] = value
                                return_list.append(dict_a)
                            if return_list:
                                return_data[k] = return_list
                        except:
                            for kkk, vvv in vv.items():
                                if kkk.endswith("&json"):
                                    value = getattr(obj_field, vvv)
                                    return_dict[kkk[:-5]] = json.loads(value) if value else None
                                else:
                                    return_dict[kkk] = getattr(obj_field, vvv)
                            if return_dict:
                                return_data[k] = return_dict

        return return_data
    return records


def get_model_data_by_ids(model, ids, return_data_dict):
    """
    通过id获取一条数据
    :param model:
    :param ids:
    :param return_data_dict: 返回的data字段列表
    :return:
    """
    records = model.objects.filter(id__in=ids)
    if not records:
        return None
    # 查询成功
    if records.count == 1:
        record = records[0]
        return_data = {}
        if return_data_dict and isinstance(return_data_dict, dict):
            for k, v in return_data_dict.items():
                obj_field = getattr(record, v)
                return_data[k] = obj_field
            return return_data
        return records
    else:
        return_data_list = []
        for record in records:
            return_data = {}
            if return_data_dict and isinstance(return_data_dict, dict):
                for k, v in return_data_dict.items():
                    obj_field = getattr(record, v)
                    return_data[k] = obj_field
                return_data_list.append(return_data)
            else:
                return_data_list.append(record)
        return return_data_list
