from typing import Union
from nonebot import on_notice
from nonebot.adapters.onebot.v11 import Bot, Message
from nonebot.adapters.onebot.v11 import GroupBanNoticeEvent
from plugins.common_plugins_function import white_list_handle
from haruka_bot.utils import group_only

group_ban_handler = on_notice(priority=5)
group_ban_handler.handle()(white_list_handle("captions_groups"))
group_ban_handler.handle()(group_only)


@group_ban_handler.handle()
async def _(bot: Bot, event: Union[GroupBanNoticeEvent]):
    """群禁言/解禁Handler"""

    ban_operator_info = \
        await bot.get_group_member_info(group_id=event.group_id, user_id=event.operator_id, no_cache=True)
    ban_user_info = \
        await bot.get_group_member_info(group_id=event.group_id, user_id=event.user_id, no_cache=True)

    if event.sub_type == "ban":
        ret_str = f"{ban_user_info.get('card', '')}（{event.user_id}）被" \
                  f"{ban_operator_info.get('card', '')}（{event.operator_id}）" \
                  f"塞了{event.duration}秒的口球"
    else:
        ret_str = f"{ban_operator_info.get('card', '')}（{event.operator_id}）取出了" \
                  f"{ban_user_info.get('card', '')}（{event.user_id}）" \
                  f"的口球"
    await group_ban_handler.finish(ret_str)
