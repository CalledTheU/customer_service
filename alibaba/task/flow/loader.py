"""
    用于加载yml文件,封装到FlowCatalog
"""
from pathlib import Path

import yaml

from alibaba.task.flow.models import FlowCatalog, FlowSlot, Flow
from alibaba.task.flow.steps import FlowStep


class FlowLoader:
    # 根据yml文件路径加载yml文件数据,封装到FlowCatalog对象
    def load(self, path: Path) -> FlowCatalog:
        # 读取文件中的内容,返回字符串
        flow_text = path.read_text(encoding='utf-8')
        # 把字符串内容转换为dict格式
        flow_dict = yaml.safe_load(flow_text)
        # 加载槽位数据
        slots: dict[str, FlowSlot] = self._load_slots(flow_dict["slots"])
        # 加载流程数据
        flows: dict[str, Flow] = self._load_flows(flow_dict["flows"], slots)
        return FlowCatalog(slots=slots, flows=flows)

    def _load_slots(self, slots_dict: dict[str, dict]) -> dict[str, FlowSlot]:
        slots: dict[str, FlowSlot] = {}
        for slot_name, slot_data in slots_dict.items():
            slot = FlowSlot(name=slot_name, **slot_data)
            slots[slot_name] = slot
        return slots

    def _load_flows(self, flow_data:dict[str, dict],
                         slots:dict[str,FlowSlot]) -> dict[str,Flow]:
        flows: dict[str, Flow] = {}
        for flows_name,flows_data in flow_data.items():
            # 处理槽位数据
            flows_slots: list[FlowSlot] = []
            for collect_step in flows_data["steps"]:
                if collect_step["type"] == "collect":
                    slot = slots[collect_step["slot_name"]]
                    flows_slots.append(slot)
            # 处理步骤数据
            flows_steps: list[FlowStep] = []
            for step_data in flows_data["steps"]:
                step = FlowStep.from_dict(step_data)
                flows_steps.append(step)

            flow: Flow = Flow(
                id=flows_name,
                description=flows_data["description"],
                steps=flows_steps,
                slots=flows_slots,
                name=flows_data["name"]
            )
            flows[flows_name] = flow
        return flows



if __name__ == '__main__':
    loader = FlowLoader()
    path = Path(__file__).parents[3] / 'flow_config' / 'user_flows.yml'
    res = loader.load(path)
    print(res)
