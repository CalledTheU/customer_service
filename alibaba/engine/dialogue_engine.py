# -*- coding: utf-8 -*-
# ==============================================================================
# Package:
# File: dialogue_engine.py
# Description:
# Date: 2026/9/9 10:36
#
# @author WangLei
# @version 1.0
# @email WangLei1578@outlook.com
# @since Python 3.14.5
# ==============================================================================
from alibaba.domain.message import UserMessage
from alibaba.domain.state import DialogueState

class DialogueEngine:
    def process_message(self, state:DialogueState, user_message:UserMessage):
        pass