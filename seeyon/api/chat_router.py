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
from dataclasses import asdict
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends

from seeyon.api.depends import get_dialogue_service
from seeyon.api.schemas import ChatResponse, ChatRequest, ChatMessage, ChatObject, HistoryResponse, HistoryMessage
from seeyon.domain.message import UserMessage, ProcessResult, MessageType, MessageObject
from seeyon.domain.state import DialogueState
from seeyon.service.dialogue_service import DialogueService

chat_router = APIRouter()


@chat_router.post("/api/chat")
async def chat(chat_request: ChatRequest,
               service: DialogueService = Depends(get_dialogue_service)) -> ChatResponse:
    # 1 获取前端传入数据，封装到ChatRequest
    # 2 把api层ChatRequest对象 转换 service层数据模型对象
    user_message: UserMessage = _build_user_message(chat_request)

    # 3 注入service对象，调用service方法
    process_result: ProcessResult = await service.process_message(user_message)

    # 4 获取service方法返回结果，把service返回类型转换api层ChatResponse
    chat_response: ChatResponse = _build_chat_response(process_result)

    # 5 返回转换之后api层ChatResponse对象
    return chat_response

    # 把api层ChatRequest对象 转换 service层数据模型对象UserMessage
    #  ChatRequest ==> UserMessage


def _build_user_message(chatRequest: ChatRequest) -> UserMessage:
    return UserMessage(
        sender_id=chatRequest.sender_id,
        message_id=chatRequest.message_id
        if chatRequest.message_id else str(uuid.uuid4()),
        type=MessageType.TEXT
        if chatRequest.text else MessageType.OBJECT,
        text=chatRequest.text,
        # ChatObject ==> MessageObject
        object=MessageObject(
            id=chatRequest.object.id,
            type=chatRequest.object.type,
            title=chatRequest.object.title,
            attributes=chatRequest.object.attributes,
        ) if chatRequest.object else None,
    )


# 4 获取service方法返回结果 ProcessResult，把service返回类型转换api层ChatResponse
# ProcessResult -- ChatResponse
def _build_chat_response(process_result: ProcessResult) -> ChatResponse:
    return ChatResponse(
        sender_id=process_result.sender_id,
        message_id=process_result.message_id,
        # process_result里面messages列表遍历得到每个BotMessage对象
        # 把每个BotMessage对象转换 ChatMessage
        messages=[
            ChatMessage(
                text=bot_message.text,
                object=ChatObject(
                    **asdict(bot_message.object)
                ) if bot_message.object else None,
            )
            for bot_message in process_result.messages
        ]
    )


# 根据用户ID查询历史记录接口
@chat_router.get("/api/chat/history")
async def chat(sender_id:str,
        service:DialogueService=Depends(get_dialogue_service)) -> HistoryResponse:
    state: DialogueState = await service.get_history_info(sender_id)
    # 封装成历史记录响应对象HistoryResponse
    messages: list[HistoryMessage] = []

    # 获取对话历史记录
    for session in state.shared.sessions:
        for turn in session.turns:
            messages.append(
                HistoryMessage(
                    role="user",
                    text=turn.user_message.text,
                    object=ChatObject(
                        **asdict(turn.user_message.object)
                    ) if turn.user_message.object else None
                )
            )
            messages.extend(
                [
                    HistoryMessage(
                        role="bot",
                        text=message.text,
                        object=None
                    ) for message in turn.bot_message
                ]
            )

        return HistoryResponse(
            sender_id=sender_id,
            messages=messages
        )
