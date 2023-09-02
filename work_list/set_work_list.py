import re
from nonebot.adapters.onebot.v11.event import GroupMessageEvent
from nonebot.adapters.onebot.v11.message import Message
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.params import CommandArg, ArgPlainText
from nonebot import on_command
from haruka_bot.utils import (
    group_only,
)
from plugins.common_plugins_function, while_list_handle
from ..db.captions_groups_db_utils import CaptionsGroupsDBUtils

set_work_list = on_command(
    "设置工作表",
    rule=to_me(),
    priority=5
)
set_work_list.__doc__ = """设置工作表"""
set_work_list.__help_type__ = None

set_work_list.handle()(while_list_handle("captions_groups"))
set_work_list.handle()(group_only)


async def handle_url(
    matcher: Matcher,
    command_arg: Message = CommandArg(),
):
    url = command_arg.extract_plain_text().strip()
    # 不是url就报错
    if re.match(".*(http|www)[^ ]* *", url) is not None:
        matcher.set_arg("url", command_arg)
    else:
        await matcher.finish("工作表链接无效！")
set_work_list.handle()(handle_url)


@set_work_list.handle()
async def _(
        event: GroupMessageEvent, 
        url: str = ArgPlainText("url")
):
    ret_msg = ""
    work_list = await CaptionsGroupsDBUtils.get_work_list(
        type="group",
        type_id=event.group_id)
    if work_list:
        ret_msg = "【原工作表已被覆盖】\n"
    await CaptionsGroupsDBUtils.set_work_list(
        type="group",
        type_id=event.group_id,
        work_list=url)
    ret_msg += "已写入工作表"
    await set_work_list.finish(ret_msg)
