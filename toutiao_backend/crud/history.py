from datetime import datetime

from sqlalchemy import select, func, delete
from sqlalchemy.ext.asyncio import AsyncSession

from models.history import History
from models.news import News


async def add_news_history(db: AsyncSession, user_id: int, news_id: int):
    # 查询是否存在浏览历史记录
    stmt = select(History).where(History.user_id == user_id, History.news_id == news_id)
    result = await db.execute(stmt)
    existing_history = result.scalar_one_or_none()
    # 存在则更新浏览时间，不存在则添加新记录
    if existing_history:
        existing_history.view_time = datetime.now()
        await db.commit()
        await db.refresh(existing_history)
        return existing_history
    else:
        history = History(user_id=user_id, news_id=news_id)
        db.add(history)
        await db.commit()
        await db.refresh(history)
        return history

async def get_news_history(db: AsyncSession, user_id: int, page: int, page_size: int):
    # 统计总量
    stmt = select(func.count()).where(History.user_id == user_id)
    count_result = await db.execute(stmt)
    total = count_result.scalar_one()
    # 联表查询，浏览时间排序，分页
    query = (select(News, History.view_time)
             .join(History, History.news_id == News.id)
             .where(History.user_id == user_id)
             .order_by(History.view_time.desc())
             .offset((page-1)*page_size).limit(page_size))
    result = await db.execute(query)
    rows = result.all()
    return rows, total

async def remove_news_history(db: AsyncSession, user_id: int, news_id: int):
    stmt = delete(History).where(History.user_id == user_id, History.news_id == news_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount > 0

async def clear_news_history(db: AsyncSession, user_id: int):
    stmt = delete(History).where(History.user_id == user_id)
    await db.execute(stmt)
    await db.commit()
