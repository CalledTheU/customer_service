# -*- coding: utf-8 -*-
# ==============================================================================
# Package:
# File: depends.py
# Description:
# Date: 2026/9/9 10:35
#
# @author WangLei
# @version 1.0
# @email WangLei1578@outlook.com
# @since Python 3.14.5
# ==============================================================================
from sqlalchemy.ext.asyncio.session import AsyncSession

from alibaba.engine.dialogue_engine import DialogueEngine
from alibaba.repository.dialogue_repository import DialogueRepository
from alibaba.service.dialogue_service import DialogueService
from alibaba.utils import database
from fastapi import Depends

"""
用于创建模型对象
"""


# 数据库session对象
async def get_session():
    async with database.async_session() as session:
        yield session


# 数据库仓库对象
async def get_repository(session: AsyncSession = Depends(get_session)):
    return DialogueRepository(session=session)


# 对话引擎对象
async def get_engine():
    return DialogueEngine()


# 对话服务对象
async def get_dialogue_service(
        dialogue_repository: DialogueRepository = Depends(get_repository),
        dialogue_engine: DialogueEngine = Depends(get_engine)):
    return DialogueService(engine=dialogue_engine, repository=dialogue_repository)
