"""
在settings中设置该中间件
MIDDLEWARE = [
    # ... 你的其他中间件
    'utils.DataTransMiware.DTMiddleware'
]
"""
import json
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin

from newbee.newbee_util.AESPy import decrypt_oralce, encrypt_oracle
from newbee.newbee_util.AESPy import sign_key
from newbee.config import is_recv_json, is_send_text, exclude_path
# 前端请求json  是否进行业务处理
from newbee.newbee_util.pro_log import logger


class DTMiddleware(MiddlewareMixin):
    def process_request(self, request):
        path = str(request.path)
        if path not in exclude_path and [path, str(request.method).upper()] not in exclude_path and str(
                request.method).upper() != "GET":
            try:
                if is_recv_json:
                    if request.META["CONTENT_TYPE"] not in ("application/json",):
                        try:
                            request.META["CONTENT_TYPE"] = "application/json"
                            logger.debug("收到text：%s" % request.body.decode('utf-8'))
                            json_data = decrypt_oralce(sign_key, request.body.decode('utf-8'))
                            logger.debug("收到json：%s" % json_data)
                            if isinstance(json_data, str):
                                setattr(request, "_body", json_data.encode('utf-8'))
                            setattr(request, "_body", json.dumps(json_data).encode('utf-8'))
                        except Exception as e:
                            str_data = encrypt_oracle(sign_key, {
                                "msg": "解密失败: " + str(e),
                                "code": 400
                            })
                            http_response = HttpResponse(str_data.encode('utf-8'),
                                                         content_type="text/plain,charset=utf-8")
                            http_response.status_code = 400
                            return http_response
                    else:
                        logger.debug("前端发送了json")
                else:
                    if request.META["CONTENT_TYPE"] not in ("application/json",):
                        try:
                            request.META["CONTENT_TYPE"] = "application/json"
                            json_data = decrypt_oralce(sign_key, request.body.decode('utf-8'))
                            if isinstance(json_data, str):
                                setattr(request, "_body", json_data.encode('utf-8'))
                            setattr(request, "_body", json.dumps(json_data).encode('utf-8'))
                        except Exception as e:
                            str_data = encrypt_oracle(sign_key, {
                                "msg": "解密失败: " + str(e),
                                "code": 400
                            })
                            http_response = HttpResponse(str_data.encode('utf-8'),
                                                         content_type="text/plain,charset=utf-8")
                            http_response.status_code = 400
                            return http_response
                    else:
                        str_data = encrypt_oracle(sign_key, {
                            "msg": "后端不接受json数据",
                            "code": 400
                        })
                        http_response = HttpResponse(str_data.encode('utf-8'), content_type="text/plain,charset=utf-8")
                        http_response.status_code = 400
                        return http_response
            except Exception as e:
                logger.error("解密时发生错误")

    def process_response(self, request, response):
        path = str(request.path)
        if path not in exclude_path and [path, str(request.method).upper()] not in exclude_path:
            if response:
                if is_send_text:
                    try:
                        if response["Content-Type"] in ("application/json",):
                            str_data = encrypt_oracle(sign_key, response.data)
                            http_response = HttpResponse(str_data.encode("utf-8"),
                                                         content_type="text/plain,charset=utf-8")
                            http_response.status_code = response.status_code
                            return http_response
                        else:
                            logger.debug("不是返回的json, 返回的：%s" % response["Content-Type"])
                            return response
                    except Exception as e:
                        logger.error("加密时发生错误:%s" % e)
                        return response
        else:
            return response
