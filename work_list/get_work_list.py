from protocol_adapter.protocol_adapter import ProtocolAdapter
from protocol_adapter.adapter_type import AdapterGroupMessageEvent
from nonebot import on_regex
from plugins.common_plugins_function import white_list_handle
from ..database.captions_groups import DBPluginsCaptionsGroupsInfo
from utils import group_only

get_work_list = on_regex(
    pattern=r"^(工作|工资|giaogiao|gaugau)表$",
    priority=5,
    block=True
)
get_work_list.__doc__ = """工作表"""
get_work_list.__help_type__ = None

get_work_list.handle()(white_list_handle("captions_groups"))
get_work_list.handle()(group_only)


@get_work_list.handle()
async def _(
    event: AdapterGroupMessageEvent
):
    msg_type = ProtocolAdapter.get_msg_type(event)
    msg_type_id = ProtocolAdapter.get_msg_type_id(event)
    work_list = DBPluginsCaptionsGroupsInfo.get_work_list_by_msg_type_id(msg_type, msg_type_id)
    if not work_list:
        await get_work_list.finish("尚未设置工作表！")
    else:
        event_msg_extra_str = {
            "工资表": "不好好切片翻译打轴校对还想要工资？？？\n\n",
            "giaogiao表": "no giao!\n\n",
            "gaugau表": "gau~\n\n"
        }
        # 一个彩蛋
        pre_str = event_msg_extra_str.get(str(event.message), "")
        await get_work_list.finish(pre_str + work_list)
