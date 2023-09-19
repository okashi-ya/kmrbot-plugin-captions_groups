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
from plugins.common_plugins_function import white_list_handle
from ..db.captions_groups_db_utils import CaptionsGroupsDBUtils

set_welcome_content = on_command(
    "设置群欢迎内容",
    priority=5,
    rule=to_me()
)
set_welcome_content.__doc__ = """设置群欢迎内容"""
set_welcome_content.__help_type__ = None

set_welcome_content.handle()(white_list_handle("captions_groups"))
set_welcome_content.handle()(group_only)


async def handle_content(
    matcher: Matcher,
    command_arg: Message = CommandArg(),
):
    matcher.set_arg("content", command_arg)
set_welcome_content.handle()(handle_content)


@set_welcome_content.handle()
async def _(
        event: GroupMessageEvent, 
        content: str = ArgPlainText("content")
):
    ret_msg = ""
    welcome_content = await CaptionsGroupsDBUtils.get_welcome_content(
        type="group",
        type_id=event.group_id)
    if welcome_content:
        ret_msg = "【原群欢迎内容已被覆盖】\n"
    await CaptionsGroupsDBUtils.set_welcome_content(
        type="group",
        type_id=event.group_id,
        welcome_content=content)
    ret_msg += "已写入群欢迎内容"
    await set_welcome_content.finish(ret_msg)
