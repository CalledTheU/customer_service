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
from fastapi import FastAPI

from alibaba.api.chat_router import chat_router

app = FastAPI()

app.include_router(chat_router)