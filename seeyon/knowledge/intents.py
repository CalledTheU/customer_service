# -*- coding: utf-8 -*-
# ==============================================================================
# Package:
# File: intent.py
# Description:
# Date: 2026/9/16 09:21
#
# @author WangLei
# @version 1.0
# @email WangLei1578@outlook.com
# @since Python 3.14.5
# ==============================================================================
from dataclasses import dataclass, field


@dataclass
class KnowledgeIntent:
    id: str  # 范围值
    description: str  # 范围值对应中文描述
    # 当前范围问题 答案位置
    provider_ids: list[str] = field(default_factory=list)
    # 查询表单信息 form  流程信息  flow 传入对应类型对象
    requires_object: str | None = None

# 创建字典
KNOWLEDGE_INTENTS: dict[str, KnowledgeIntent] = {
    "form_info": KnowledgeIntent(
        id="form_info", description="表单信息咨询",
        provider_ids=["api.form"], requires_object="form",
    ),
    "flow_info": KnowledgeIntent(
        id="flow_info", description="流程信息咨询",
        provider_ids=["api.flow"], requires_object="flow",
    ),

    "leave_policy": KnowledgeIntent(
        id="leave_policy", description="请假制度咨询",
        provider_ids=["faq.default", "rag.default"],
    ),
    "expense_policy": KnowledgeIntent(
        id="expense_policy", description="报销制度咨询",
        provider_ids=["faq.default", "rag.default"],
    ),
    "seal_policy": KnowledgeIntent(
        id="seal_policy", description="用章制度咨询",
        provider_ids=["faq.default", "rag.default"],
    ),
    "oa_policy": KnowledgeIntent(
        id="oa_policy", description="协同平台使用规范咨询",
        provider_ids=["rag.default"],
    ),
    "general_office_info": KnowledgeIntent(
        id="general_office_info", description="协同办公通用信息咨询",
        provider_ids=["faq.default", "rag.default"],
    ),
}

