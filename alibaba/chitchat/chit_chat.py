# -*- coding: utf-8 -*-
# ==============================================================================
# Package:
# File: chit_chat.py
# Description:
# Date: 2026/9/16 19:35
#
# @author WangLei
# @version 1.0
# @email WangLei1578@outlook.com
# @since Python 3.14.5
# ==============================================================================
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from alibaba.domain.message import UserMessage, BotMessage
from alibaba.domain.state import DialogueState
from alibaba.prompts.history_builder import HistoryBuilder
from alibaba.prompts.loader import load_prompt
from alibaba.utils.llm_client import chat_model


class ChitChat:
    async def handle(self,user_message:UserMessage,
                     state:DialogueState)->list[BotMessage]:
        prompt_text = load_prompt("chitchat_respond")
        prompt = PromptTemplate.from_template(prompt_text, template_format="jinja2")

        # 创建调用链(调用大模型)
        chain = prompt | chat_model | StrOutputParser()

        response = await chain.ainvoke({"history": HistoryBuilder.build(state.shared.sessions[-1].turns),
                                       "user_message": HistoryBuilder.render_user_message(user_message)})
        return [BotMessage(text=response)]