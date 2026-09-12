# -*- coding: utf-8 -*-
# ==============================================================================
# Package:
# File: database.py.py
# Description:工具模块,用于异步操作MySQL
# Date: 2026/9/8 18:52
#
# @author WangLei
# @version 1.0
# @email WangLei1578@outlook.com
# @since Python 3.14.5
# ==============================================================================

import asyncio

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, AsyncSession, create_async_engine

from alibaba.config.config import settings

# 引擎:用于和数据库做连接
engine: AsyncEngine | None = None
# session 会话:通过async_sessionmaker 工厂创建AsyncSession
async_session: async_sessionmaker[AsyncSession] | None = None

def init_db_engine():
    global engine, async_session
    # 这个方法内部有数据库连接池
    if engine is None:
        engine = create_async_engine(
            url=settings.database_url,
            # 是否打印SQL语句，方便调试,默认是False
            echo=True
        )
    # 会话:通过async_sessionmaker 工厂创建AsyncSession
    if async_session is None:
        async_session = async_sessionmaker(
            # 绑定引擎
            bind=engine,
            # 是否在提交后过期，如果设置为True，则提交后会话中的对象会立即变为过期，需要重新查询
            expire_on_commit=False
        )


async def close_engine():
    await engine.dispose()  # 关闭引擎

async def test():
    """
    测试数据库连接
    :return:
    """
    init_db_engine()
    async with async_session() as session:
        result = await session.execute(text("select 1"))
        print(result.fetchone())
    await close_engine()

if __name__ == '__main__':
    asyncio.run(test())