"""
weiboanalysis.dao.userDao 的 Docstring
用户数据访问层
"""

from flask import jsonify
from sqlalchemy import select
from sqlalchemy.orm import Session

from weiboanalysis.extensions import engine
from weiboanalysis.models.userModel import User

def get_user_by_username(username: str) -> User | None:
    """
    get_user_by_username 的 Docstring
    根据用户名获取用户
    """
    with Session(engine) as session:
        user = session.execute(select(User).where(User.username == username)).scalar_one_or_none()
    
    return user

def add_user(username: str, password: str) -> bool:
    """
    add_user 的 Docstring
    添加用户
    """
    with Session(engine) as session:
        user = User(username=username, password=password)
        session.add(user)
        session.commit()
    
    return True

def get_user_by_name(username: str) -> User | None:
    """
    get_user_by_name 的 Docstring
    根据用户名获取用户
    """
    with Session(engine) as session:
        user = session.execute(select(User).where(User.username == username)).scalar_one_or_none()
    
    return user