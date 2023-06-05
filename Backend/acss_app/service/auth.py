"""authentication service
"""
import hashlib
from typing import Tuple

from django.core.exceptions import ObjectDoesNotExist

from acss_app.models import User
from acss_app.service.exceptions import UserAlreadyExisted, UserDoesNotExisted, WrongPassword
from acss_app.service.util.jwt_tool import Role, gen_token


def register(username: str, password: str, key: str) -> None:
    registered: User = User.objects.filter(username=username).exists()
    if registered:
        raise UserAlreadyExisted("用户名已被注册")
    hashed_password = hashlib.md5(password.encode('utf-8')).hexdigest()
    if (len(key) == 0) :
        print("key为空，注册为用户")
        user = User(username=username, password=hashed_password)
        user.save()
    else :
        if (key == "abcdefgh"):
            print("满足条件，key有效，注册为管理员")
            user = User(username=username, password=hashed_password, is_admin=True)
            user.save()
    


def login(username: str, password: str) -> Tuple[str, Role]:
    """登陆

    Args:
        username (str): 用户名
        password (str): 密码

    Raises:
        UserDoesNotExisted: 用户名不存在
        WrongPassword: 密码错误

    Returns:
        Tuple[str, Role]: JWT令牌, 角色
    """
    try:
        user: User = User.objects.get(username=username)
    except ObjectDoesNotExist as e:
        raise UserDoesNotExisted("用户名不存在") from e
    hashed_password = hashlib.md5(password.encode('utf-8')).hexdigest()
    if user.password != hashed_password:
        raise WrongPassword("密码错误")
    role = Role.USER
    if user.is_admin:
        role = Role.ADMIN
    return gen_token(username, role.name), role
