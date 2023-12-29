from nonebot import on_notice
from protocol_adapter.protocol_adapter import ProtocolAdapter
from protocol_adapter.adapter_type import AdapterGroupIncreaseNoticeEvent
from ..database.captions_groups import DBPluginsCaptionsGroupsInfo
from utils.rule import group_only
from utils.permission import white_list_handle

group_increase_handler = on_notice(priority=5, rule=group_only)
group_increase_handler.handle(white_list_handle("captions_groups"))


@group_increase_handler.handle()
async def _(event: AdapterGroupIncreaseNoticeEvent):
    """进群欢迎Handler"""
    msg_type = ProtocolAdapter.get_msg_type(event)
    msg_type_id = ProtocolAdapter.get_msg_type_id(event)
    user_id = ProtocolAdapter.get_user_id(event)
    welcome_content = DBPluginsCaptionsGroupsInfo.get_group_welcome_content_by_msg_type_id(msg_type, msg_type_id)
    if not welcome_content:
        await group_increase_handler.finish()
    else:
        msg = ProtocolAdapter.MS.at(user_id) + ProtocolAdapter.MS.text("\n" + welcome_content)
        await group_increase_handler.finish(msg)
