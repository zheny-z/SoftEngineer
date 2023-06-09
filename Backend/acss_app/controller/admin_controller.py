"""管理员客户端控制器"""
from django.http import HttpRequest, JsonResponse

from acss_app.controller.util.validator import validate, ValidationError
from acss_app.controller.util.resp_tool import RetCode
from acss_app.service.auth import Role
from acss_app.service.exceptions import PileDoesNotExisted
from acss_app.service.schd import scheduler
from acss_app.service.simple_query import get_all_piles_status, get_pile_status, query_report, update_pile_status
from acss_app.service.util.jwt_tool import RequestContext, preprocess_token
from acss_app.models import PileStatus


__update_pile_status_schema = {
    'type': 'object',
    'required': ['chargingPileId', 'status'],
    'properties': {
        'chargingPileId': {
            'type': 'string',
            'errmsg': "pile_id 应为字符串"
        },
        'status': {
            'type': 'string',
            'enum': ['RUNNING', 'SHUTDOWN', 'UNAVAILABLE'],
            'errmsg': "status 应为可选值为'RUNNING', 'SHUTDOWN', 'UNAVAILABLE'的字符串"
        }
    }
}


@preprocess_token(limited_role=Role.ADMIN)
def query_all_piles_stat_api(_: RequestContext, req: HttpRequest) -> JsonResponse:
    try:
        validate(req, method='GET')
    except ValidationError as e:
        return JsonResponse({
            'code': RetCode.FAIL.value,
            'message': str(e)
        })

    status_list = get_all_piles_status()

    return JsonResponse({
        'code': RetCode.SUCCESS.value,
        'message': 'success',
        'data': status_list
    })


@preprocess_token(limited_role=Role.ADMIN)
def update_pile_status_api(_: RequestContext, req: HttpRequest) -> JsonResponse:
    try:
        kwargs = validate(req, method='POST',
                          schema=__update_pile_status_schema)
    except ValidationError as e:
        return JsonResponse({
            'code': RetCode.FAIL.value,
            'message': str(e)
        })

    pile_id_str: str = kwargs['chargingPileId']
    status_str: str = kwargs['status']
    pile_id = int(pile_id_str)
    status = PileStatus[status_str]

    try:
        status_before = get_pile_status(pile_id)
        update_pile_status(pile_id, status)
        match status_before:
            case PileStatus.RUNNING:
                match status:
                    case PileStatus.SHUTDOWN | PileStatus.UNAVAILABLE:
                        # 当充电桩故障时，进行的一系列操作
                        scheduler.brake(pile_id)
                    case _:
                        pass
            case PileStatus.SHUTDOWN | PileStatus.UNAVAILABLE:
                match status:
                    case PileStatus.RUNNING:
                        # 当充电桩从故障状态恢复后进行的一系列操作
                        scheduler.recover(pile_id)
                    case _:
                        pass

    except PileDoesNotExisted as e:
        return JsonResponse({
            'code': RetCode.SUCCESS.value,
            'message': str(e)
        })

    return JsonResponse({
        'code': RetCode.SUCCESS.value,
        'message': 'success'
    })


@preprocess_token(limited_role=Role.ADMIN)
def query_report_api(_: RequestContext, req: HttpRequest) -> JsonResponse:
    try:
        validate(req, method='GET')
    except ValidationError as e:
        return JsonResponse({
            'code': RetCode.FAIL.value,
            'message': str(e)
        })

    report = query_report()

    return JsonResponse({
        'code': RetCode.SUCCESS.value,
        'message': 'success',
        'data': report
    })


@preprocess_token(limited_role=Role.ADMIN)
def query_queue_api(_: RequestContext, req: HttpRequest) -> JsonResponse:
    try:
        validate(req, method='GET')
    except ValidationError as e:
        return JsonResponse({
            'code': RetCode.FAIL.value,
            'message': str(e)
        })

    snapshot = scheduler.snapshot()

    return JsonResponse({
        'code': RetCode.SUCCESS.value,
        'message': 'success',
        'data': snapshot
    })
