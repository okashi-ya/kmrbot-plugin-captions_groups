from nonebot import on_notice
from protocol_adapter.protocol_adapter import ProtocolAdapter
from protocol_adapter.adapter_type import AdapterBot, AdapterGroupBanNoticeEvent
from utils.rule import group_only
from utils.permission import white_list_handle

group_ban_handler = on_notice(priority=5, rule=group_only)
group_ban_handler.handle(white_list_handle("captions_groups"))


@group_ban_handler.handle()
async def _(bot: AdapterBot, event: AdapterGroupBanNoticeEvent):
    """群禁言/解禁Handler"""
    ban_info = await ProtocolAdapter.Ban.get_ban_info(bot, event)
    if ban_info["is_ban"]:
        ret_str = f"{ban_info['ban_user_name']}（{ban_info['ban_user_id']}）被" \
                  f"{ban_info['operator_user_name']}（{ban_info['operator_user_id']}）" \
                  f"塞了{ban_info['duration']}秒的口球"
    else:
        ret_str = f"{ban_info['operator_user_name']}（{ban_info['operator_user_id']}）取出了" \
                  f"{ban_info['ban_user_name']}（{ban_info['ban_user_id']}）" \
                  f"的口球"
    await group_ban_handler.finish(ret_str)
