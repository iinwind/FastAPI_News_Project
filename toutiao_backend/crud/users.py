import uuid
from datetime import datetime, timedelta

from fastapi import HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import user

from models.users import User, UserToken
from schemas.users import UserRequest, UserUpdateRequest
from utils import security
from utils.security import get_hash_password

# 根据用户名查询用户
async def get_user_by_username(db: AsyncSession, username: str):
    stmt = select(User).where(User.username == username)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

# 创建用户
async def create_user(db: AsyncSession, user_data: UserRequest):
    user = User(
        username=user_data.username,
        password=get_hash_password(user_data.password),
    )
    db.add(user)
    await db.commit()
    await db.refresh(user) # 从数据库重新读取这条记录，对于一些自动生成的字段（如自增id），需要刷新对象才能获取最新值
    return user

# 生成 Token
async def create_token(db: AsyncSession, user_id: int):
    token = str(uuid.uuid4())
    expires_at = datetime.now() + timedelta(days=7)
    query = select(UserToken).where(UserToken.user_id == user_id)
    result = await db.execute(query)
    user_token = result.scalar_one_or_none()
    if user_token:
        user_token.token = token
        user_token.expires_at = expires_at
    else:
        user_token = UserToken(user_id=user_id, token=token, expires_at=expires_at)
        db.add(user_token)
    await db.commit()
    return token

# 认证用户
async def authenticate_user(db: AsyncSession, username: str, password: str):
    user = await get_user_by_username(db, username)
    if not user:
        return None
    if not security.verify_password(password, user.password):
        return None
    return user

# 根据 token 查询当前可用用户
async def get_user_by_token(db: AsyncSession, token: str):
    stmt = select(UserToken).where(UserToken.token == token)
    result = await db.execute(stmt)
    db_token = result.scalar_one_or_none()

    if not db_token or db_token.expires_at < datetime.now():
        return None

    stmt = select(User).where(User.id == db_token.user_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

# 更新用户信息
async def update_user(db: AsyncSession, user_data: UserUpdateRequest, username: str):
    stmt = update(User).where(User.username == username).values(**user_data.model_dump(exclude_unset=True, exclude_none=True)) # model_dump() = 把 Pydantic 对象转成 普通字典
    result = await db.execute(stmt)
    await db.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="用户不存在")

    updated_user = await get_user_by_username(db, username)
    return updated_user

# 修改密码
async def change_password(db: AsyncSession, user: User, old_password: str, new_password: str):
    if not security.verify_password(old_password, user.password):
        return False
    hashed_new_pwd = security.get_hash_password(new_password)
    user.password = hashed_new_pwd
    db.add(user) # 规避session过期或关闭导致的不能提交的问题
    await db.commit()
    await db.refresh(user)
    return True