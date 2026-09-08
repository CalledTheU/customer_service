# -*- coding: utf-8 -*-
# ==============================================================================
# Package:
# File: chat_router.py
# Description:
# Date: 2026/9/8 20:02
#
# @author WangLei
# @version 1.0
# @email WangLei1578@outlook.com
# @since Python 3.14.5
# ==============================================================================
import uuid
from uuid import UUID

from fastapi import APIRouter

from alibaba.api.schemas import ChatResponse, ChatRequest, ChatMessage

chat_router = APIRouter()

@chat_router.post("/api/chat")
async def chat(chat_request:ChatRequest) -> ChatResponse:
    # 1 获取前端传入数据，封装到ChatRequest
    # 2 把api层ChatRequest对象 转换 service层数据模型对象
    # 3 注入service对象，调用service方法
    # 4 获取service方法返回结果，把service返回类型转换api层ChatResponse
    # 5 返回转换之后api层ChatResponse对象
    return ChatResponse(
        sender_id = chat_request.sender_id,
        message_id = str(uuid.uuid4()),
        messages = [
            ChatMessage(
                text = "您好",
                object = None
        )]
    )
