"""
这个模块用于远程调用，调用协同平台接口查询审批进度
查询审批进度，需要使用流程单号
"""
from seeyon.config.config import settings
from seeyon.domain.state import DialogueState
from seeyon.task.action.base import Action, ActionResult
from seeyon.utils import http_client


# 查询审批进度action
class QueryApprovalProgress(Action):
    # name值和yaml文件查询审批进度流程action属性值相同
    name = "action_query_approval_progress"

    # 实现基类里面抽象方法，这个方法实现远程调用
    async def run(self, state: DialogueState) -> ActionResult:
        # 获取流程单号
        flow_number = state.tasks.active.slots.get("flow_number")

        # 拼接协同平台查询审批进度接口地址
        url = (f"{settings.commerce_api_base_url}"
               f"/flows/{flow_number}/approval")

        # 远程调用
        response = await http_client.http_client.get(url)
        data = response.json().get("data", "未知")

        return ActionResult(
            slot_updates={
                "node_name": data.get("node_name", "未知节点"),
                "approver": data.get("approver", "未知"),
                "approval_progress": data.get("status", "未知")
            }
        )
