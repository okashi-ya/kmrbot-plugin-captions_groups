from protocol_adapter.protocol_adapter import ProtocolAdapter
from protocol_adapter.adapter_type import AdapterMessage, AdapterGroupMessageEvent
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.params import CommandArg, ArgPlainText
from nonebot import on_command
from ..database.captions_groups import DBPluginsCaptionsGroupsInfo
from utils.rule import group_only
from utils.permission import white_list_handle

set_welcome_content = on_command(
    "设置群欢迎内容",
    priority=5,
    rule=to_me() & group_only()
)
set_welcome_content.__doc__ = """设置群欢迎内容"""
set_welcome_content.__help_type__ = None
set_welcome_content.handle(white_list_handle("captions_groups"))


async def handle_content(
    matcher: Matcher,
    command_arg: AdapterMessage = CommandArg(),
):
    matcher.set_arg("content", command_arg)
set_welcome_content.handle()(handle_content)


@set_welcome_content.handle()
async def _(
        event: AdapterGroupMessageEvent,
        content: str = ArgPlainText("content")
):
    msg_type = ProtocolAdapter.get_msg_type(event)
    msg_type_id = ProtocolAdapter.get_msg_type_id(event)
    ret_msg = ""
    welcome_content = DBPluginsCaptionsGroupsInfo.get_group_welcome_content_by_msg_type_id(msg_type, msg_type_id)
    if welcome_content:
        ret_msg = "【原群欢迎内容已被覆盖】\n"
    DBPluginsCaptionsGroupsInfo.set_group_welcome_content(msg_type, msg_type_id, content)
    ret_msg += "已写入群欢迎内容"
    await set_welcome_content.finish(ret_msg)
