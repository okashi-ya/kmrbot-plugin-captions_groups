from nonebot.adapters.onebot.v11.event import GroupMessageEvent
from nonebot.adapters.onebot.v11.message import Message
from nonebot import on_command
from haruka_bot.utils import (
    group_only,
)
from plugins.common_plugins_function import while_list_handle
from ..db.captions_groups_db_utils import CaptionsGroupsDBUtils


get_work_list = on_command(
    "工作表", aliases={
        "工资表",
        "giaogiao表",
        "gaugau表"},
    priority=5,
)
get_work_list.__doc__ = """工作表"""
get_work_list.__help_type__ = None

get_work_list.handle()(while_list_handle("captions_groups"))
get_work_list.handle()(group_only)


@get_work_list.handle()
async def _(
    event: GroupMessageEvent
):
    work_list = await CaptionsGroupsDBUtils.get_work_list(
        type="group",
        type_id=event.group_id)
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
        msg = Message(pre_str + work_list)
        await get_work_list.finish(msg)
