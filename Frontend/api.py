"""API封装"""
from datetime import datetime
from typing import Any, Dict, List, Tuple

import requests


# BASE_URL = 'https://acss.jnn.icu/api'  # 基础 API URL (停止维护)
BASE_URL = 'http://127.0.0.1:8000'  # 本地测试 URL
TOKEN = ''


class ApiError(BaseException):
    """API返回值为-1时抛出该异常

    服务端抛出错误信息时，raise本异常，
    外侧调用者捕获该异常并决定是否打印异常信息。

    抛出方法：
    ```
    if resp['code'] == -1:
        raise ApiError(resp['message'])
    ```

    处理方法：
    ```
    try:
        some_api()
    except ApiError as e:
        some_toast(str(e)).show()
    ```
    """


def api_post(path: str, json: Dict) -> Dict[str, Any] | None:
    """POST 请求封装

    Args:
        path (str): BASE_URL 后的相对路径
        json (Dict): 字典，会被转换为JSON字符串置于请求体中

    Raises:
        ApiError: 响应码为-1的异常，包含错误信息

    Returns:
        Dict[str, Any] | None: 响应中的 data 字段，可能为 None
    """
    url = BASE_URL + path
    try:
        if len(TOKEN) > 0:
            header = {'Authorization': f'Bearer {TOKEN}'}
            resp: dict = requests.post(url=url, json=json, headers=header).json()
        else:
            resp: dict = requests.post(url=url, json=json).json()
    except requests.exceptions.ConnectTimeout as e:
        raise ApiError('连接超时') from e
    except requests.exceptions.ConnectionError as e:
        raise ApiError('连接错误') from e
    except requests.exceptions.ReadTimeout as e:
        raise ApiError('数据读取超时') from e
    except requests.exceptions.HTTPError as e:
        raise ApiError('Http错误') from e
    except BaseException as e:
        raise ApiError('网络错误') from e
    if resp['code'] == -1:
        raise ApiError(resp['message'])
    return resp.get('data')


def api_get(path: str) -> Dict[str, Any] | None:
    """GET 请求封装

    Args:
        path (str): BASE_URL 后的相对路径

    Raises:
        ApiError: 响应码为-1的异常，包含错误信息

    Returns:
        Dict[str, Any] | None: 响应中的 data 字段，可能为 None
    """
    url = BASE_URL + path
    try:
        if len(TOKEN) > 0:
            header = {'Authorization': f'Bearer {TOKEN}'}
            resp: dict = requests.get(url=url, headers=header).json()
        else:
            resp: dict = requests.get(url=url).json()
    except requests.exceptions.ConnectTimeout as e:
        raise ApiError('连接超时') from e
    except requests.exceptions.ConnectionError as e:
        raise ApiError('连接错误') from e
    except requests.exceptions.ReadTimeout as e:
        raise ApiError('数据读取超时') from e
    except requests.exceptions.HTTPError as e:
        raise ApiError('Http错误') from e
    except BaseException as e:
        raise ApiError('网络错误') from e
    if resp['code'] == -1:
        raise ApiError(resp['message'])
    return resp.get('data')


def login(username: str, password: str) -> Dict[str, Any]:
    data = api_post('/login', json={'username': username, 'password': password})
    return data['token'], data['is_admin']


def time() -> Tuple[datetime, int]:
    data = api_get('/time')
    return data['datetime'], data['timestamp']


def register(username: str, password: str) -> None:
    api_post('/user/register', json={
        'username': username,
        'password': password,
        're_password': password
    })


def submit_charging_request(charge_mode: str, require_amount: str, battery_size: str) -> None:
    api_post('/user/submit_charging_request', json={
        'charge_mode': charge_mode,
        'require_amount': require_amount,
        'battery_size': battery_size
    })


def edit_charging_request(charge_mode: str, require_amount: str) -> None:
    api_post('/user/edit_charging_request', json={
        'charge_mode': charge_mode,
        'require_amount': require_amount
    })


def end_charging_request() -> None:
    api_get('/user/end_charging_request')


def query_order_detail() -> List[Dict[str, Any]]:
    data = api_get('/user/query_order_detail')
    return data


def preview_queue() -> Dict[str, Any]:
    data = api_get('/user/preview_queue')
    return data


def query_all_piles_stat() -> Dict[str, Any]:
    data = api_get('/admin/query_all_piles_stat')
    return data


def admin_status_report() -> List[Dict[str, Any]]:
    data = api_get('/admin/query_report')
    return data


def admin_query_queue() -> List[Dict[str, Any]]:
    data = api_get('/admin/query_queue')
    return data


def update_pile_stat(pile_id: str, status: str) -> None:
    data = api_post('/admin/update_pile', json={
        'pile_id': pile_id,
        'status': status
    })
    return data
