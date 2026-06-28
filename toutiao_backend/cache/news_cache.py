# 新闻相关的缓存方法：新闻分类的读取和写入
from typing import List, Dict, Any, Optional

from config.cache_conf import get_json_cache, set_cache

CATEFORIES_KEY = "news:categories"
NEWS_LIST_PREFIX = "news_list:"

# 获取新闻分类缓存
async def get_cached_categories():
    return await get_json_cache(CATEFORIES_KEY)

# 写入新闻分类缓存：缓存数据、过期时间
async def set_cache_categories(data: List[Dict[str, Any]], expire: int = 7200):
    return await set_cache(CATEFORIES_KEY, data, expire)

# 获取新闻列表缓存
async def get_cache_news_list(category_id: Optional[int], page: int, size: int):
    category_part = category_id if category_id is not None else "all"
    key = f"{NEWS_LIST_PREFIX}{category_part}:{page}:{size}"
    return await get_json_cache(key)

# 写入新闻列表缓存
async def set_cache_news_list(category_id: Optional[int], page: int, size: int, news_list: List[Dict[str, Any]], expire: int = 1800):
    # 调用 redis 封装的设置方法，存新闻列表到缓存
    category_part = category_id if category_id is not None else "all"
    key = f"{NEWS_LIST_PREFIX}{category_part}:{page}:{size}"
    return await set_cache(key, news_list, expire)