# -*- coding: utf-8 -*-
# ==============================================================================
# Package:
# File: proc.py
# Description:
# Date: 2026/9/12 14:18
#
# @author WangLei
# @version 1.0
# @email WangLei1578@outlook.com
# @since Python 3.14.5
# ==============================================================================

""""
    根据意图识别结果,更新state里面的数据
    返回任务状态变化对象 TaskEvent,用于后面组件生成中文提示
"""
from alibaba.domain.state import DialogueState, TaskInstance
from alibaba.task.command.models import Command, StartFlowCommand, SetSlotsCommand, ResumeTaskCommand, CancelTaskCommand
from alibaba.task.flow.models import FlowCatalog, Flow
from alibaba.task.lifecycle.models import TaskEvent


class CommandProcessor:
    async def run(self,commands:list[Command],
                  state: DialogueState,
                  flows: FlowCatalog) -> list[TaskEvent]:
        events:list[TaskEvent] = []
        # 遍历意图识别结果列表，得到每个command，根据不同类型command不同处理
        for command in commands:
            event:TaskEvent = self._execute_command(command,state,flows)
            if event:
                events.append(event)
        return events

    def _execute_command(self, command:Command,
                         state:DialogueState,
                         flow_catalog:FlowCatalog) -> TaskEvent:
        # 判断command类型
        # `{"command": "start_flow", "flow": "<flow_id>"}`
        if isinstance(command, StartFlowCommand):
            # 获取流程id
            flow_id = command.flow
            # 根据流程id获取flow对象
            flow: Flow = flow_catalog.get_flow_by_id(flow_id)
            # 获取开始类型步骤
            step = flow.get_start_step()
            # 创建当前任务对象
            task = TaskInstance(
                flow_id=flow_id,
                step_id=step.id
            )
            # 更新state对象里面 TaskState 里面 属性值 active 和 paused
            event: TaskEvent = state.tasks.start(task)
            return event

        # {"command": "set_slots", "slots": {"<slot_name>": "<value>"}}
        # 设置槽位数据前提条件：当前有活跃任务
        if isinstance(command, SetSlotsCommand):
            state.tasks.active.slots.update(command.slots)
            return None

        # `{"command": "cancel_task", "task_id": "<task_id>"}`
        if isinstance(command, ResumeTaskCommand):
            event: TaskEvent = state.tasks.resume(command.task_id)
            return event

        # `{"command": "resume_task", "task_id": "<task_id>"}`
        if isinstance(command, CancelTaskCommand):
            event: TaskEvent = state.tasks.cancel(command.task_id)
            return event
