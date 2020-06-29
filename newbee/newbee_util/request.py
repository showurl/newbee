from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.http import QueryDict
import json

from rest_framework_jwt.utils import jwt_decode_handler


def get_request_body_dict(request):
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


def get_character_id_by_request(request):
    token = request.META.get('HTTP_TOKEN')
    if not token:
        return -1
    try:
        jwt_user = jwt_decode_handler(token)
    except:
        # token过期
        return -1
    if not jwt_user:
        return -1
    user_id = jwt_user.get('user_id')
    jwt_model = get_user_model()
    try:
        user = jwt_model.objects.get(id=user_id)
    except ObjectDoesNotExist:
        return -1
    else:
        chara = user.character
        if not chara:
            return -1
        else: return chara.id

def get_user_by_request(request):
    token = request.META.get('HTTP_TOKEN')
    if not token:
        return
    try:
        jwt_user = jwt_decode_handler(token)
    except:
        # token过期
        return
    if not jwt_user:
        return
    user_id = jwt_user.get('user_id')
    jwt_model = get_user_model()
    try:
        user = jwt_model.objects.get(id=user_id)
    except ObjectDoesNotExist:
        return
    return user

def get_username_by_request(request):
    user = get_user_by_request(request)
    if not user:
        return None
    else:
        return user.username
