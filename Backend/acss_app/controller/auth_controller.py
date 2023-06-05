"""身份验证控制器"""
from django.http import HttpRequest, JsonResponse

from acss_app.service.auth import login, register

from acss_app.service.timemock import get_timestamp_now, get_datetime_now
from acss_app.controller.util.validator import validate, ValidationError
from acss_app.controller.util.resp_tool import RetCode
from acss_app.service.exceptions import UserAlreadyExisted, UserDoesNotExisted, WrongPassword
from acss_app.service.util.jwt_tool import Role


__login_schema = {
    'type': 'object',
    'required': ['username', 'password'],
    'properties': {
        'username': {
            'type': 'string',
            'errmsg': "username 应为字符串"
        },
        'password': {
            'type': 'string',
            'errmsg': "password 应为字符串"
        }
    }
}


__register_schema = {
    'type': 'object',
    'required': ['username', 'password', 'key'],
    'properties': {
        'username': {
            'type': 'string',
            'minLength': 4,
            'errmsg': "username 应为4位以上字符串"
        },
        'password': {
            'type': 'string',
            'minLength': 8,
            'errmsg': "password 应为8位以上字符串"
        },
        'key': {
            'type': 'string',
            'minLength': 0
        }
    }
}


def login_api(req: HttpRequest) -> JsonResponse:
    try:
        kwargs = validate(req, schema=__login_schema)
    except ValidationError as e:
        return JsonResponse({
            'code': RetCode.FAIL.value,
            'message': str(e)
        })
    username = kwargs['username']
    password = kwargs['password']
    try:
        token, role = login(username, password)
    except UserDoesNotExisted as e:
        return JsonResponse({
            'code': RetCode.FAIL.value,
            'message': str(e)
        })
    except WrongPassword as e:
        return JsonResponse({
            'code': RetCode.FAIL.value,
            'message': str(e)
        })

    is_admin = False
    if role == Role.ADMIN:
        is_admin = True

    return JsonResponse({
        'code': RetCode.SUCCESS.value,
        'message': 'success',
        'data': {
            'token': token,
            "is_admin": is_admin
        }
    })

# 注册时前端传来的req里面包含三个字段；
# 其中key字段是管理员注册秘钥，用于后端检验秘钥有效性
def register_api(req: HttpRequest) -> JsonResponse:
    try:
        kwargs = validate(req, schema=__register_schema)
    except ValidationError as e:
        return JsonResponse({
            'code': RetCode.FAIL.value,
            'message': str(e)
        })
    username = kwargs['username']
    password = kwargs['password']
    key = kwargs['key'] 
    try:
        register(username, password, key) 
    except UserAlreadyExisted as e:
        return JsonResponse({
            'code': RetCode.FAIL.value,
            'message': str(e)
        })
    except WrongPassword as e:
        return JsonResponse({
            'code': RetCode.FAIL.value,
            'message': str(e)
        })

    return JsonResponse({
        'code': RetCode.SUCCESS.value,
        'message': 'success'
    })


def query_time(req: HttpRequest) -> JsonResponse:
    try:
        validate(req, method='GET')
    except ValidationError as e:
        return JsonResponse({
            'code': RetCode.FAIL.value,
            'message': str(e)
        })

    return JsonResponse({
        'code': RetCode.SUCCESS.value,
        'message': 'success',
        'data': {
            'datetime': get_datetime_now(),
            'timestamp': get_timestamp_now()
        }
    })
