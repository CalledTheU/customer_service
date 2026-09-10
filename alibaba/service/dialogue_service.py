# -*- coding: utf-8 -*-
# ==============================================================================
# Package:
# File: dialogue_repository.py
# Description:1. 根据api层传递的session_id,调用数据库层(repository)查询当前用户的对话历史
#             2. 根据查询历史记录 +用户问题 调用engine层处理用户消息
#             3.把当前这一次对话，调用repository层保存数据库里面
#             4.返回engine层处理结果
# Date: 2026/9/8 20:26
#
# @author WangLei
# @version 1.0
# @email WangLei1578@outlook.com
# @since Python 3.14.5
# ==============================================================================
from alibaba.domain.message import ProcessResult, UserMessage, BotMessage
from alibaba.domain.state import DialogueState
from alibaba.engine.dialogue_engine import DialogueEngine
from alibaba.repository.dialogue_repository import DialogueRepository

class DialogueService:

    def __init__(self, engine: DialogueEngine, repository: DialogueRepository):
        self.engine = engine
        self.repository = repository

    """
        1.根据api层传递的session_id, 调用数据库层(repository)查询当前用户的对话历史
        2.根据查询历史记录 + 用户问题调用engine层处理用户消息
        3.把当前这一次对话，调用repository层保存数据库里面
        4.返回engine层处理结果
    """
    async def process_message(self, user_message:UserMessage) -> ProcessResult:
        # 1.根据api层传递的session_id, 调用数据库层(repository)查询当前用户的对话历史
        sender_id = user_message.sender_id
        state:DialogueState = await self.repository.load_state(sender_id)

        # todo 2.根据查询历史记录 + 用户问题调用engine层处理用户消息
        # result = self.engine.process_message(state, user_message)

        # 3.把当前这一次对话，调用repository层保存数据库里面
        await self.repository.save_state(state)

        # 4.返回engine层处理结果
        # todo
        return ProcessResult(
            sender_id=sender_id,
            message_id=user_message.message_id,
            messages=[BotMessage(
                text="你要揍嘛?",
                object=None
            )]
        )