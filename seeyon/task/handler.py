# -*- coding: utf-8 -*-
# ==============================================================================
# Package:
# File: handler.py
# Description:
# Date: 2026/9/14 21:12
#
# @author WangLei
# @version 1.0
# @email WangLei1578@outlook.com
# @since Python 3.14.5
# ==============================================================================
from seeyon.domain.message import UserMessage, BotMessage
from seeyon.domain.state import DialogueState
from seeyon.task.command.models import Command
from seeyon.task.command.process import CommandProcessor
from seeyon.task.flow.models import FlowCatalog
from seeyon.task.lifecycle.models import TaskEvent
from seeyon.task.lifecycle.responder import TaskLifecycleResponder
from seeyon.task.flow.executor import FlowExecutor


class TaskHandler:
    # 注入
    def __init__(self,command_processor:CommandProcessor,
                 task_lifecycle:TaskLifecycleResponder,
                 flow_executor:FlowExecutor):
        self.command_processor = command_processor
        self.task_lifecycle = task_lifecycle
        self.flow_executor = flow_executor

    # 调用的方法
    # commands: 意图识别结果列表
    # flows:所有流程数据
    async def handle(self,commands: list[Command],
            state: DialogueState,
            flows: FlowCatalog,
            user_message:UserMessage)->list[BotMessage]:
        # 1 根据意图识别结果，调用CommandProcessor更新state状态数据
        events:list[TaskEvent] = await self.command_processor.run(
            commands=commands,
            state=state,
            flows=flows,
        )

        # 2 根据CommandProcessor返回结果,调TaskLifecycleResponder生成不同中文提示
        messages:list[BotMessage] = await self.task_lifecycle.responder(
            events=events,
            flow_catalog=flows,
        )

        # 3 调用FlowEXecutor推进步骤实现
        bot_messages:list[BotMessage] = await self.flow_executor.run_step(
            state=state,
            flows=flows,
        )
        messages.extend(bot_messages)

        return messages