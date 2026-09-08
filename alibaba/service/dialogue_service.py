# -*- coding: utf-8 -*-
# ==============================================================================
# Package:
# File: dialogue_repository.py
# Description:1. 根据api层传递的session_id,调用数据库层(repository)查询当前用户的对话历史
#             2. 根据查询历史记录 +用户问题 调用engine层处理用户消息
#             3.把当前这一次对话，调用repository层保存数据库里面
#             4.返回engine层处理结果
# Date: 2026/9/8 20:26
#
# @author WangLei
# @version 1.0
# @email WangLei1578@outlook.com
# @since Python 3.14.5
# ==============================================================================

class DialogueService:
    pass