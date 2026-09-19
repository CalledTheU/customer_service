# -*- coding: utf-8 -*-
# ==============================================================================
# Package:
# File: turn_plan.py
# Description:
# Date: 2026/9/11 21:05
#
# @author WangLei
# @version 1.0
# @email WangLei1578@outlook.com
# @since Python 3.14.5
# ==============================================================================
import json
from dataclasses import asdict

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate

from seeyon.domain.message import UserMessage
from seeyon.domain.state import DialogueState
from seeyon.knowledge.intents import KNOWLEDGE_INTENTS
from seeyon.plan.models import TurnPlan
from seeyon.prompts.history_builder import HistoryBuilder
from seeyon.prompts.loader import load_prompt
from seeyon.task.flow.models import FlowCatalog
from seeyon.utils.llm_client import chat_model
"""
    用于进行用户意图识别
    # RAFT
    ## Role：明确告诉LLM当前身份角色是什么
    ## Action：明确告诉LLM当前做事情是什么
    ## Format：明确告诉LLM以什么格式输出，输出示例
    ## Tone：语气，以专家口吻...
"""
class TurnPlanner:
    async def plan(self,
                   user_message: UserMessage,
                   state: DialogueState,
                   flow_catalog: FlowCatalog):
        # 加载提示词模版
        prompt_text = load_prompt('turn_plan')
        prompt = PromptTemplate.from_template(
            prompt_text, template_format='jinja2'
        )

        # 创建调用链
        chain = prompt | chat_model | JsonOutputParser()

        # 获取提示词需要数据
        # 用户消息
        user_message_str = HistoryBuilder.render_user_message(user_message)

        # 历史记录
        conversation_history = HistoryBuilder.build(state.shared.sessions[-1].turns)

        # 对象类型消息
        focused_object_json = json.dumps(asdict(state.shared.focused_object)
                                         if state.shared.focused_object else None)

        # 任务流程特有数据
        task_state_json = json.dumps(asdict(state.tasks)
                                     if state.tasks else None)

        # flows_json yml文件中的流程数据(不包含steps数据,避免出现幻觉)
        flows = [
            {key: value for key, value in asdict(flow).items()
             if key != 'steps'}
            for flow in flow_catalog.flows.values()
        ] if flow_catalog else None
        flows_json = json.dumps(flows, ensure_ascii=False)

        # 知识检索范围数据
        knowledge_intents_json = json.dumps(
            [
                {
                    "id": intent.id,
                    "description": intent.description
                }
                for intent in KNOWLEDGE_INTENTS.values()
            ]
        )

        # 执行invoke，得到结果
        res = await chain.ainvoke({
            "user_message": user_message_str,
            "flows_json": flows_json,
            "knowledge_intents_json": knowledge_intents_json,
            "task_state_json": task_state_json,
            "focused_object_json": focused_object_json,
            "conversation_history": conversation_history
        })

        # LLM返回json转换TurnPlan
        return TurnPlan.from_dict(res)
