ADD_SUCCESS_2000 = {
    "code": 2000,
    "msg": "增加成功"
}


def get_ADD_SUCCESS_2000(msg=None, format=None):
    if msg:
        ADD_SUCCESS_2000["msg"] = msg
        return ADD_SUCCESS_2000
    if format:
        ADD_SUCCESS_2000["msg"] += msg
        return ADD_SUCCESS_2000
    return ADD_SUCCESS_2000


DELETE_SUCCESS_2001 = {
    "code": 2001,
    "msg": "删除成功"
}


def get_DELETE_SUCCESS_2001(msg=None, format=None):
    if msg:
        DELETE_SUCCESS_2001["msg"] = msg
        return DELETE_SUCCESS_2001
    if format:
        DELETE_SUCCESS_2001["msg"] += msg
        return DELETE_SUCCESS_2001
    return DELETE_SUCCESS_2001

UPDATE_SUCCESS_2002 = {
    "code": 2002,
    "msg": "修改成功"
}


def get_UPDATE_SUCCESS_2002(msg=None, format=None):
    if msg:
        UPDATE_SUCCESS_2002["msg"] = msg
        return UPDATE_SUCCESS_2002
    if format:
        UPDATE_SUCCESS_2002["msg"] += msg
        return UPDATE_SUCCESS_2002
    return UPDATE_SUCCESS_2002


FIND_SUCCESS_2003 = {
    "code": 2003,
    "msg": "查询成功"
}


def get_FIND_SUCCESS_2003(msg=None, format=None):
    if msg:
        FIND_SUCCESS_2003["msg"] = msg
        return FIND_SUCCESS_2003
    if format:
        FIND_SUCCESS_2003["msg"] += msg
        return FIND_SUCCESS_2003
    return FIND_SUCCESS_2003


SUCCESS_200 = {
    "code": 200,
    "msg": "成功"
}


def get_SUCCESS_200(msg=None, format=None):
    if msg:
        SUCCESS_200["msg"] = msg
        return SUCCESS_200
    if format:
        SUCCESS_200["msg"] += msg
        return SUCCESS_200
    return SUCCESS_200


FAIL_BY_PARA_NOT_ALL_4000 = {
    "code": 4000,
    "msg": "因为传递参数不全导致的失败"
}


def get_FAIL_BY_PARA_NOT_ALL_4000(msg=None, format=None):
    if msg:
        FAIL_BY_PARA_NOT_ALL_4000["msg"] = msg
        return FAIL_BY_PARA_NOT_ALL_4000
    if format:
        FAIL_BY_PARA_NOT_ALL_4000["msg"] += msg
        return FAIL_BY_PARA_NOT_ALL_4000
    return FAIL_BY_PARA_NOT_ALL_4000


FAIL_BY_PARA_TYPE_4001 = {
    "code": 4001,
    "msg": "因为传递参数类型不正确导致的失败"
}


def get_FAIL_BY_PARA_TYPE_4001(msg=None, format=None):
    if msg:
        FAIL_BY_PARA_TYPE_4001["msg"] = msg
        return FAIL_BY_PARA_TYPE_4001
    if format:
        FAIL_BY_PARA_TYPE_4001["msg"] += msg
        return FAIL_BY_PARA_TYPE_4001
    return FAIL_BY_PARA_TYPE_4001


FAIL_BY_PARA_NOT_UNIQUE_4002 = {
    "code": 4002,
    "msg": "因为传递参数不是唯一值导致的失败"
}


def get_FAIL_BY_PARA_NOT_UNIQUE_4002(msg=None, format=None):
    if msg:
        FAIL_BY_PARA_NOT_UNIQUE_4002["msg"] = msg
        return FAIL_BY_PARA_NOT_UNIQUE_4002
    if format:
        FAIL_BY_PARA_NOT_UNIQUE_4002["msg"] += msg
        return FAIL_BY_PARA_NOT_UNIQUE_4002
    return FAIL_BY_PARA_NOT_UNIQUE_4002


FAIL_BY_PARA_400 = {
    "code": 400,
    "msg": "因为传递参数原因导致失败,具体原因未知"
}


def get_FAIL_BY_PARA_400(msg=None, format=None):
    if msg:
        FAIL_BY_PARA_400["msg"] = msg
        return FAIL_BY_PARA_400
    if format:
        FAIL_BY_PARA_400["msg"] += msg
        return FAIL_BY_PARA_400
    return FAIL_BY_PARA_400


FAIL_BY_LOGIN_NO_INFO_4030 = {
    "code": 4030,
    "msg": "因为没有登录或者登录信息已失效导致的失败"
}


def get_FAIL_BY_LOGIN_NO_INFO_4030(msg=None, format=None):
    if msg:
        FAIL_BY_LOGIN_NO_INFO_4030["msg"] = msg
        return FAIL_BY_LOGIN_NO_INFO_4030
    if format:
        FAIL_BY_LOGIN_NO_INFO_4030["msg"] += msg
        return FAIL_BY_LOGIN_NO_INFO_4030
    return FAIL_BY_LOGIN_NO_INFO_4030


FAIL_BY_LEVEL_NOT_ENOUGH_4031 = {
    "code": 4031,
    "msg": "因为当前登录用户没有使用该接口权限导致的失败"
}


def get_FAIL_BY_LEVEL_NOT_ENOUGH_4031(msg=None, format=None):
    if msg:
        FAIL_BY_LEVEL_NOT_ENOUGH_4031["msg"] = msg
        return FAIL_BY_LEVEL_NOT_ENOUGH_4031
    if format:
        FAIL_BY_LEVEL_NOT_ENOUGH_4031["msg"] += msg
        return FAIL_BY_LEVEL_NOT_ENOUGH_4031
    return FAIL_BY_LEVEL_NOT_ENOUGH_4031


FAIL_BY_FORBIDDEN_2003 = {
    "code": 403,
    "msg": "因为登录或权限问题导致的失败,具体原因未知"
}


def get_FAIL_BY_FORBIDDEN_2003(msg=None, format=None):
    if msg:
        FAIL_BY_FORBIDDEN_2003["msg"] = msg
        return FAIL_BY_FORBIDDEN_2003
    if format:
        FAIL_BY_FORBIDDEN_2003["msg"] += msg
        return FAIL_BY_FORBIDDEN_2003
    return FAIL_BY_FORBIDDEN_2003


FAIL_BY_NOTHING_TO_DO_4040 = {
    "code": 4040,
    "msg": "因为传递参数查询不到结果导致的失败"
}


def get_FAIL_BY_NOTHING_TO_DO_4040(msg=None, format=None):
    if msg:
        FAIL_BY_NOTHING_TO_DO_4040["msg"] = msg
        return FAIL_BY_NOTHING_TO_DO_4040
    if format:
        FAIL_BY_NOTHING_TO_DO_4040["msg"] += msg
        return FAIL_BY_NOTHING_TO_DO_4040
    return FAIL_BY_NOTHING_TO_DO_4040


FAIL_BY_NOT_FOUND_404 = {
    "code": 404,
    "msg": "因为查询不到导致的失败,具体原因未知"
}


def get_FAIL_BY_NOT_FOUND_404(msg=None, format=None):
    if msg:
        FAIL_BY_NOT_FOUND_404["msg"] = msg
        return FAIL_BY_NOT_FOUND_404
    if format:
        FAIL_BY_NOT_FOUND_404["msg"] += msg
        return FAIL_BY_NOT_FOUND_404
    return FAIL_BY_NOT_FOUND_404


FAIL_BY_REQUEST_TYPE_NOT_ALLOW_4050 = {
    "code": 4050,
    "msg": "请求方式不被允许导致的失败"
}


def get_FAIL_BY_REQUEST_TYPE_NOT_ALLOW_4050(msg=None, format=None):
    if msg:
        FAIL_BY_REQUEST_TYPE_NOT_ALLOW_4050["msg"] = msg
        return FAIL_BY_REQUEST_TYPE_NOT_ALLOW_4050
    if format:
        FAIL_BY_REQUEST_TYPE_NOT_ALLOW_4050["msg"] += msg
        return FAIL_BY_REQUEST_TYPE_NOT_ALLOW_4050
    return FAIL_BY_REQUEST_TYPE_NOT_ALLOW_4050


FAIL_BY_REQUEST_TYPE_405 = {
    "code": 405,
    "msg": "请求方式导致的失败,具体原因未知"
}


def get_FAIL_BY_REQUEST_TYPE_405(msg=None, format=None):
    if msg:
        FAIL_BY_REQUEST_TYPE_405["msg"] = msg
        return FAIL_BY_REQUEST_TYPE_405
    if format:
        FAIL_BY_REQUEST_TYPE_405["msg"] += msg
        return FAIL_BY_REQUEST_TYPE_405
    return FAIL_BY_REQUEST_TYPE_405

SERVER_ERROR = 500