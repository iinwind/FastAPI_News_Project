from fastapi import Header, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from config.db_conf import get_db
from crud import users

# 验证令牌，并返回用户
async def get_current_user(
        authorization: str = Header(...,alias="Authorization"), # 从请求头中读取 Authorization 字段
        db: AsyncSession = Depends(get_db)
):
    # token = authorization.split(" ")[1]
    token = authorization.replace("Bearer ", "")  # 移除 "Bearer " 前缀，获取纯令牌
    user = await users.get_user_by_token(db, token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="无效的令牌或已经过期的令牌")
    return user