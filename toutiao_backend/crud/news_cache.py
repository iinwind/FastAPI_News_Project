from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from cache.news_cache import get_cached_categories, set_cache_categories, get_cache_news_list, set_cache_news_list
from models.news import Category, News
from schemas.base import NewsItemBase


async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 100):
    # 先尝试从缓存中获取数据
    cached_categories = await get_cached_categories()
    if cached_categories:
        return cached_categories
    # 从数据库中查询新闻的所有分类
    stmt = select(Category).offset(skip).limit(limit)
    result = await db.execute(stmt)
    categories = result.scalars().all()
    # 写入缓存
    if categories:
        categories = jsonable_encoder(categories) # 将 SQLAlchemy 模型转换为 JSON 可序列化的格式
        await set_cache_categories(categories)
    # 返回数据
    return categories

async def get_news_list(db: AsyncSession, category_id: int, skip: int = 0, limit: int = 10):
    # 先尝试从缓存中获取数据
    cached_list = await get_cache_news_list(category_id, skip//limit+1, limit) # 缓存数据：json
    if cached_list:
        return [News(**item) for item in cached_list] # 需要的是 ORM
    # 从数据库中查询指定分类下的所有新闻
    stmt = select(News).where(News.category_id == category_id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    news_list = result.scalars().all()
    # 写入缓存
    if news_list:
        # ORM 转换为 Pydantic，再转为字典
        news_data = [NewsItemBase.model_validate(item).model_dump(mode="json",by_alias=False) for item in news_list]
        await set_cache_news_list(category_id, skip//limit+1, limit, news_data)
    # 返回数据
    return news_list