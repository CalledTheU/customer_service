# -*- coding: utf-8 -*-
# ==============================================================================
# Package:
# File: llm_client.py
# Description:工具模块,用于创建大语言模型
# Date: 2026/9/8 14:06
#
# @author WangLei
# @version 1.0
# @email WangLei1578@outlook.com
# @since Python 3.14.5
# ==============================================================================
from langchain.chat_models import init_chat_model
from langchain_core.language_models import BaseChatModel

from alibaba.config.config import settings

chat_model: BaseChatModel = init_chat_model(
    model=settings.LLM_MODEL,
    model_provider="openai",
    api_key=settings.llm_api_key,
    base_url = settings.llm_base_url,
    temperature="0",
)

if __name__ == '__main__':
    model_invoke = chat_model.invoke("Hello, how are you?")
    print(model_invoke.content)
