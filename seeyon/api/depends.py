from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from seeyon.chitchat.chit_chat import ChitChat
from seeyon.clarify.clarify_response import ClarifyResponse
from seeyon.engine.dialogue_engine import DialogueEngine
from seeyon.knowledge.hanlder import KnowledgeHanlder
from seeyon.knowledge.provider import FormProvider, ApiFlowProvider, FAQProvider, RAGProvider
from seeyon.knowledge.registry import KnowledgeProviderRegistry
from seeyon.knowledge.responder import KnowledgeResponseder
from seeyon.plan.turn_plan import TurnPlanner
from seeyon.plan.turn_plan_validation import TurnPlannValidator
from seeyon.repository.dialogue_repository import DialogueRepository
from seeyon.service.dialogue_service import DialogueService
from seeyon.task.action.registry import ActionRegistry
from seeyon.task.action.runner import ActionRunner
from seeyon.task.command.process import CommandProcessor
from seeyon.task.flow.executor import FlowExecutor
from seeyon.task.lifecycle.responder import TaskLifecycleResponder
from seeyon.task.handler import TaskHandler
from seeyon.task.response.renderer import ResponseTemplateRender
from seeyon.utils import database
from seeyon.task.action.builder import registry_action

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

    knowledge_registry = KnowledgeProviderRegistry(
        provider_objs=[
            FormProvider(),
            ApiFlowProvider(),
            FAQProvider(),
            RAGProvider()
        ]
    )

    knowledge_hanlder = KnowledgeHanlder(knowledge_responder=KnowledgeResponseder(),
                                         knowledge_registry=knowledge_registry)

    return DialogueEngine(
        turn_planner=turn_planner,
        turn_plann_validator=turn_plann_validator,
        task_handler=task_handler,
        clarif_response=clarify_response,
        chit_chat=chit_chat,
        knowledge_hanlder=knowledge_hanlder
    )

async def get_dialogue_service(
        dialogue_repository:DialogueRepository=Depends(get_repository),
        dialogue_engine:DialogueEngine=Depends(get_engine)):
    return DialogueService(
        engine=dialogue_engine,
       repository=dialogue_repository
    )