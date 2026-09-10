# -*- coding: utf-8 -*-
# ==============================================================================
# Package:
# File: dialogue_repository.py
# Description:
# Date: 2026/9/8 20:26
#
# @author WangLei
# @version 1.0
# @email WangLei1578@outlook.com
# @since Python 3.14.5
# ==============================================================================
from pydantic import TypeAdapter
from sqlalchemy import select
from sqlalchemy.dialects.mysql import insert

from alibaba.domain.state import DialogueState
from sqlalchemy.ext.asyncio import AsyncSession

from alibaba.repository.orm.dialogue_state import DialogueStateRecord

# 序列化和反序列化 -> 使用类型适配器实现
# 对象 -> JSON字符串 -> dump_json
# JSON字符串 -> 对象 -> validate_json
DIALOGUE_STATE_ADAPTER = TypeAdapter(DialogueState)

class DialogueRepository:
    def __init__(self, session:AsyncSession):
        self.session = session

    # 根据用户ID查找对话
    # 查询数据库 -> 返回JSON字符串(需要把JSON字符串转换为对象 -> validate_json)
    async def load_state(self, sender_id:str) -> DialogueState:
        # 两种实现方式:
        # 1.使用SQL语句
        # sql = "SELECT * FROM dialogue_states WHERE sender_id = :sender_id"
        # result = await self.session.execute(sql, {"sender_id": sender_id})

        # 2.使用ORM(不需要编写SQL语句,使用sqlalchemy中封装的各种方法实现)
        # 注意: 该方法不适用于复杂SQL,如 group by/inner join等
        sql = select(DialogueStateRecord).where(DialogueStateRecord.sender_id == sender_id)
        result = await self.session.execute(sql)
        record = result.scalar_one_or_none()
        if record:
            # 由于record.state_json是JSON字符串,需要转换为对象
            return DIALOGUE_STATE_ADAPTER.validate_json(record.state_json)
        else:
            return DialogueState(sender_id=sender_id)

    # 保存对话
    # 保存数据库 -> 返回对象(需要把对象转换为JSON字符串 -> dump_json)
    async def save_state(self, state:DialogueState):
        state_json = DIALOGUE_STATE_ADAPTER.dump_json(state).decode(encoding="utf-8")
        sql = insert(DialogueStateRecord).values(sender_id=state.sender_id, state_json=state_json)

        # 判断表中是否存在sender_id,在就更新,不在则插入
        key_update = sql.on_duplicate_key_update(state_json=state_json)

        await self.session.execute(key_update) 
        await self.session.commit()