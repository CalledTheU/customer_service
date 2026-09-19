# -*- coding: utf-8 -*-
# ==============================================================================
# Package:
# File: responder.py.py
# Description:用provider返回结果构建提示词，提交给LLM由LLM修改结果返回用户
# Date: 2026/9/17 11:21
#
# @author WangLei
# @version 1.0
# @email WangLei1578@outlook.com
# @since Python 3.14.5
# ==============================================================================
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from seeyon.prompts.loader import load_prompt

from seeyon.domain.message import UserMessage, BotMessage
from seeyon.domain.state import DialogueState
from seeyon.knowledge.provider import KnowledgeChunk
from seeyon.prompts.history_builder import HistoryBuilder
from seeyon.utils.llm_client import chat_model


class KnowledgeResponseder:
    async def responsed(self,state:DialogueState,
                        user_message:UserMessage,
                        chunks:list[KnowledgeChunk]):
        # 加载提示词模版
        prompt_text = load_prompt("knowledge_respond")
        prompt = PromptTemplate.from_template(
            prompt_text,
            template_format="jinja2")

        # 创建调用链
        chain = prompt | chat_model | StrOutputParser()

        # 调用
        res = await chain.ainvoke(
            {
                "knowledge_content": "\n".join(
                    [chunk.content
                     for chunk in chunks]
                ),
                "history": HistoryBuilder.build(state.shared.sessions[-1].turns),
                "user_message": HistoryBuilder.render_user_message(user_message)
            }
        )
        return BotMessage(text=res)