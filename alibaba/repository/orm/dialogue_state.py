# -*- coding: utf-8 -*-
# ==============================================================================
# Package:
# File: dialogue_state.py
# Description:
# Date: 2026/9/9 19:50
#
# @author WangLei
# @version 1.0
# @email WangLei1578@outlook.com
# @since Python 3.14.5
# ==============================================================================
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from alibaba.repository.orm.base import Base


class DialogueStateRecord(Base):
    __tablename__ = "dialogue_states"
    # sender_id = Column(String(255), primary_key=True)
    # state_json = Column(Text, nullable=False)
    # 或者
    sender_id: Mapped[str] = mapped_column(String(255), primary_key=True)
    state_json: Mapped[str] = mapped_column(Text, nullable=False)
