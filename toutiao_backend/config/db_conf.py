from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine

from config.settings import get_settings

settings = get_settings()

ASYNC_DATABASE_URL = settings.async_database_url

async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True,        # 打印SQL日志（调试用）
    pool_size=10,     # 连接池保持10个连接
    max_overflow=20   # 最多额外创建20个连接
)

# 创建异步会话工厂
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,  # 将该会话工厂绑定到某数据库引擎上
    class_=AsyncSession,  # 异步会话
    expire_on_commit=False  # 提交事务后数据不过期
)

# 获取数据库会话，提取为依赖项
async def get_db():
    async with AsyncSessionLocal() as session:  # 生产会话
        try:
            yield session  # 返回数据库给接口使用
            await session.commit()  # 无报错就提交
        except Exception:
            await session.rollback()  # 有报错就回滚
            raise  # 抛出错误
        finally:
            await session.close()  # 关闭会话