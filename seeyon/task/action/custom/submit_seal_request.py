"""
这个模块用于提交用章申请
发起用章申请，需要使用表单ID
"""
from seeyon.config.config import settings
from seeyon.domain.state import DialogueState
from seeyon.task.action.base import Action, ActionResult
from seeyon.utils import http_client


# 提交用章申请action
class SubmitSealRequest(Action):
    # name值和yaml文件用章申请流程action属性值相同
    name = "action_submit_seal_request"

    # 实现基类里面抽象方法，这个方法实现远程调用
    async def run(self, state: DialogueState) -> ActionResult:
        # 获取表单ID
        form_id = state.tasks.active.slots.get("form_id")

        # 拼接协同平台提交用章申请接口地址
        url = f"{settings.commerce_api_base_url}/seals/apply"

        # 远程调用
        response = await http_client.http_client.post(
            url,
            json={"form_id": form_id}
        )
        data = response.json().get("data", "未知")

        return ActionResult(
            slot_updates={
                "seal_result": data.get("message", "用章申请已提交，请等待审批。")
            }
        )
