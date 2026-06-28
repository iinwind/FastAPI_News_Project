from sqlalchemy import select, delete, func
from sqlalchemy.ext.asyncio import AsyncSession

from models.favorite import Favorite
from models.news import News


async def is_news_favorite(db: AsyncSession, user_id: int, news_id: int):
    stmt = select(Favorite).where(Favorite.user_id == user_id, Favorite.news_id == news_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none() is not None

async def add_news_favorite(db: AsyncSession, user_id: int, news_id: int):
    favorite = Favorite(user_id = user_id, news_id=news_id)
    db.add(favorite)
    await db.commit()
    await db.refresh(favorite)
    return favorite

async def remove_news_favorite(db: AsyncSession, user_id: int, news_id: int):
    stmt = delete(Favorite).where(Favorite.user_id == user_id,Favorite.news_id == news_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount > 0

async def get_favorite_list(db: AsyncSession, user_id: int, page: int = 1, page_size: int = 10):
    # 统计总量
    stmt = select(func.count()).where(Favorite.user_id == user_id)
    count_result = await db.execute(stmt)
    total = count_result.scalar_one()
    # 联表查询，收藏时间排序，分页
    query = (select(News, Favorite.created_at.label("favorite_time"), Favorite.id.label("favorite_id")) # 第一个参数决定了from哪个表
             .join(Favorite, Favorite.news_id == News.id)
             .where(Favorite.user_id == user_id)
             .order_by(Favorite.created_at.desc())
             .offset((page-1)*page_size).limit(page_size))
    result = await db.execute(query)
    rows = result.all()
    return rows,total

async def remove_all_favorite(db: AsyncSession, user_id: int):
    stmt = delete(Favorite).where(Favorite.user_id == user_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount or 0