# -*- coding: utf-8 -*-
# ==============================================================================
# Package:
# File: provider.py
# Description:
# Date: 2026/9/16 09:29
#
# @author WangLei
# @version 1.0
# @email WangLei1578@outlook.com
# @since Python 3.14.5
# ==============================================================================
"""
    用于创建provider,返回问题答案
"""
import asyncio
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass

from seeyon.config.config import settings
from seeyon.domain.message import UserMessage
from seeyon.domain.state import DialogueState
from seeyon.utils.http_client import http_client


# 1 封装最终结果的类
@dataclass
class KnowledgeChunk:
    content: str = ""

# 创建provider基类,公共属性和抽象方法
class KnowledgeProvider(ABC):
    provider_id = ""

    @abstractmethod
    async def provide(self,state:DialogueState,user_message:UserMessage)->list[KnowledgeChunk]:
        pass

# 每个答案位置创建provider，继承基类，实现抽象方法
# api.form
class FormProvider(KnowledgeProvider):
    provider_id = "api.form"
    # 实现抽象方法
    async def provide(self,state: DialogueState,
                      user_message: UserMessage) -> list[KnowledgeChunk]:
        focused_object = state.shared.focused_object
        if focused_object is None:
            return [KnowledgeChunk(content="请提供表单信息")]

        # 获取表单ID
        form_id = focused_object.id
        # 调用协同平台接口,获取表单信息
        url = f"{settings.commerce_api_base_url}/forms/{form_id}"
        form_info_json = await http_client.get(url)
        if not form_info_json:
            return [KnowledgeChunk(content="未能查询到该表单的信息")]

        form_info = form_info_json.json().get("data", "未能查询到该表单的信息")
        data_json = json.dumps(form_info,ensure_ascii=False)
        return [KnowledgeChunk(content=data_json)]

# api.flow
# 约定需求：查询流程信息 要调用两个协同平台接口，一个查询流程详情信息 ，一个查询流程审批信息
# 调用两个接口，使用并行方式实现，不是串行，提高速度
class ApiFlowProvider(KnowledgeProvider):
    provider_id = "api.flow"

    async def provide(self, state: DialogueState,
                      user_message: UserMessage) -> list[KnowledgeChunk]:
        # 从对象类型消息获取流程id
        focused_object = state.shared.focused_object
        if focused_object is None:
            return [KnowledgeChunk(content="请提供流程信息")]

        flow_id = focused_object.id

        # 拼接调用接口地址
        flow_info_url = f"{settings.commerce_api_base_url}/flows/{flow_id}"
        approval_info_url = f"{settings.commerce_api_base_url}/flows/{flow_id}/approval"

        # 并行方式
        # gather并行调用
        # 返回结果和gather传入顺序相关的
        flow_info,approval_info = await asyncio.gather(
            http_client.get(flow_info_url),
            http_client.get(approval_info_url),
        )

        result = json.dumps({
            "flow_info":flow_info.json().get("data","未知"),
            "approval_info":approval_info,
            },ensure_ascii=False
         )
        return [KnowledgeChunk(content=result)]

# faq.default
"""
    faq 代表常见问题
    设计： 
    1 在mysql创建数据库和表
    2 在表存储问题 和 对应答案
    3 根据用户输入问题 到 mysql表找到对应问题
      返回问题答案
"""
class FAQProvider(KnowledgeProvider):
    provider_id = 'faq.default'

    async def provide(self,
                       user_message: UserMessage,
                       state: DialogueState, ) -> list[KnowledgeChunk]:
        # TODO
        return [KnowledgeChunk(content="未检索到相关问题")]

# rag.default
"""
    rag 一般用于查询协同办公制度、操作步骤
    设计：
      之前智库项目
      远程调用，调用智库项目接口
"""
class RAGProvider(KnowledgeProvider):
    provider_id = 'rag.default'

    async def provide(self,
                       user_message: UserMessage,
                       state: DialogueState, ) -> list[KnowledgeChunk]:
        # RAG知识库查询知识接口（TODO）
        return [KnowledgeChunk(content="未检索到相关信息")]

