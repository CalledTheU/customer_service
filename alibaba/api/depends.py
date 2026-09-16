from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from alibaba.chitchat.chit_chat import ChitChat
from alibaba.clarify.clarify_response import ClarifyResponse
from alibaba.engine.dialogue_engine import DialogueEngine
from alibaba.plan.turn_plan import TurnPlanner
from alibaba.plan.turn_plan_validation import TurnPlannValidator
from alibaba.repository.dialogue_repository import DialogueRepository
from alibaba.service.dialogue_service import DialogueService
from alibaba.task.action.registry import ActionRegistry
from alibaba.task.action.runner import ActionRunner
from alibaba.task.command.process import CommandProcessor
from alibaba.task.flow.executor import FlowExecutor
from alibaba.task.lifecycle.responder import TaskLifecycleResponder
from alibaba.task.handler import TaskHandler
from alibaba.task.response.renderer import ResponseTemplateRender
from alibaba.utils import database
from alibaba.task.action.builder import registry_action

"""
   api  --  service  --  repository -- session
               |
            engine -- ？
"""

# 数据库操作session对象
async def get_session():
    async with database.async_session() as session:
        # 暂停
        yield session

# 创建repository
async def get_repository(
        session:AsyncSession=Depends(get_session)):

    return DialogueRepository(session=session)

#创建engine对象
async def get_engine():
    turn_planner = TurnPlanner()
    turn_plann_validator = TurnPlannValidator()

    registry = ActionRegistry()
    registry_action(registry)
    action_runner = ActionRunner(registry=registry)
    response_render = ResponseTemplateRender()
    task_handler = TaskHandler(
        command_processor=CommandProcessor(),
        task_lifecycle=TaskLifecycleResponder(),
        flow_executor=FlowExecutor(response_render=response_render,
                                   action_runner=action_runner)
    )
    chit_chat = ChitChat()
    clarify_response = ClarifyResponse()
    return DialogueEngine(
        turn_planner=turn_planner,
        turn_plann_validator=turn_plann_validator,
        task_handler=task_handler,
        clarif_response=clarify_response,
        chit_chat=chit_chat
    )

async def get_dialogue_service(
        dialogue_repository:DialogueRepository=Depends(get_repository),
        dialogue_engine:DialogueEngine=Depends(get_engine)):
    return DialogueService(
        engine=dialogue_engine,
       repository=dialogue_repository
    )