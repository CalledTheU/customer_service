# -*- coding: utf-8 -*-
# ==============================================================================
# Package:
# File: app.py
# Description:
# Date: 2026/9/8 20:02
#
# @author WangLei
# @version 1.0
# @email WangLei1578@outlook.com
# @since Python 3.14.5
# ==============================================================================
from contextlib import asynccontextmanager

from fastapi import FastAPI

from alibaba.api.chat_router import chat_router
from alibaba.utils.database import init_db_engine
from alibaba.utils.http_client import init_http_client

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db_engine()
    init_http_client()
    yield
    await init_db_engine()
    await init_http_client()

app = FastAPI(lifespan=lifespan)

app.include_router(chat_router)