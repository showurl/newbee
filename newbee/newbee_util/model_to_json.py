import datetime
import json
from django.db import models
import decimal
from django.db.models.query import QuerySet


class MDump:
    def __init__(self):
        self.model_type = []

    def do_dumps(self, data):
        """
        模型或列表转json
        :return:
        """
        if is_model(data):
            # if str(type(data)) in self.model_type:
            #     return None
            self.model_type.append(str(type(data)))
            data_dict = {}
            for k, v in data.__dict__.items():
                if not k.startswith("_"):
                    if not is_model(v) and not is_query_set(v) and not is_dict(v) and not is_list(v) and not isinstance(
                            v, decimal.Decimal) and not isinstance(v, Exception):
                        data_dict[k] = v.strftime("%Y-%m-%d %H:%M:%S") if isinstance(v, datetime.datetime) else v
                    else:
                        data__, flag = self.do_dumps(v)
                        data_dict[k] = data__
            return data_dict, 1
        elif is_query_set(data):
            data_list = []
            for model in data:
                data__, flag = self.do_dumps(model)
                data_list.append(data__)
            return data_list, 1
        elif is_dict(data):
            data_dict = {}
            for k, v in data.items():
                if not k.startswith("_"):
                    if not is_model(v) and not is_query_set(v) and not is_dict(v) and not is_list(v) and not isinstance(
                            v, decimal.Decimal) and not isinstance(v, Exception):
                        data_dict[k] = v.strftime("%Y-%m-%d %H:%M:%S") if isinstance(v, datetime.datetime) else v
                    else:
                        data__, flag = self.do_dumps(v)
                        data_dict[k] = data__
            return data_dict, 1
        elif is_list(data):
            data_list = []
            for model in data:
                data__, flag = self.do_dumps(model)
                data_list.append(data__)
                # print("model_data: %s "%model_data)
                # print("data_list: %s "%data_list)
            return data_list, 1
        elif isinstance(data, decimal.Decimal):
            return float(data), 1
        elif isinstance(data, Exception):
            return "服务器异常: "+str(data), -1
        else:
            return data, 1


# 判断是模型或者查询集
def is_model(data):
    if isinstance(data, models.Model):
        return True
    return False


def is_query_set(data):
    if isinstance(data, QuerySet):
        return True
    return False


def is_dict(data):
    if isinstance(data, dict):
        return True
    return False


def is_list(data):
    if isinstance(data, list):
        return True
    return False


def models_to_json(data):
    data, flag = MDump().do_dumps(data)
    if isinstance(data, str):
        data = eval(repr(data).replace('\\\\', ''))
        return data
    return data

if __name__ == '__main__':
    data = {'name': '测试4个组织机构', 'charge_person': '马守越', 'address': '不告诉你', 'email': 'yuey@163.com', 'remark': '测试4个组织机构'}
    print(models_to_json(data))