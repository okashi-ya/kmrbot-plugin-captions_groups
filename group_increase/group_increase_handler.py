from typing import Union

from nonebot import on_notice
from nonebot.adapters.onebot.v11 import GroupIncreaseNoticeEvent
from nonebot.adapters.onebot.v11 import MessageSegment, Message
from plugins.common_plugins_function import while_list_handle
from haruka_bot.utils import group_only
from ..db.captions_groups_db_utils import CaptionsGroupsDBUtils

group_increase_handler = on_notice(priority=5)
group_increase_handler.handle()(while_list_handle("captions_groups"))
group_increase_handler.handle()(group_only)


@group_increase_handler.handle()
async def _(event: Union[GroupIncreaseNoticeEvent]):
    """进群欢迎Handler"""
    print("group_increase_handler start")
    welcome_content = await CaptionsGroupsDBUtils.get_welcome_content(
        type="group",
        type_id=event.group_id)
    if not welcome_content:
        print("no welcome_content")
        await group_increase_handler.finish()
    else:
        print("welcome_content ok")
        msg = MessageSegment.at(event.user_id) + Message("\n" + welcome_content)
        await group_increase_handler.finish(msg)
