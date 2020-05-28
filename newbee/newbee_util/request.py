from django.http import QueryDict
import json


def get_request_body_dict(request):
    """
    获取字典格式的请求体(获取json字典)
    :param request: 前端传递的请求
    :return:
    """
    try:
        if isinstance(request.data, str):
            json_data = json.loads(request.data)
        else:
            json_data = request.data
    except AttributeError:
        try:
            json_data = json.loads(request.body.decode('utf-8'))
        except:
            json_data = QueryDict(request.body.decode('utf-8'))
    return json_data
