import re
from protocol_adapter.protocol_adapter import ProtocolAdapter
from protocol_adapter.adapter_type import AdapterGroupMessageEvent, AdapterMessage
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.params import CommandArg, ArgPlainText
from nonebot import on_command
from utils import group_only
from plugins.common_plugins_function import white_list_handle
from ..database.captions_groups import DBPluginsCaptionsGroupsInfo

set_work_list = on_command(
    "设置工作表",
    rule=to_me(),
    priority=5
)
set_work_list.__doc__ = """设置工作表"""
set_work_list.__help_type__ = None

set_work_list.handle()(white_list_handle("captions_groups"))
set_work_list.handle()(group_only)


async def handle_url(
    matcher: Matcher,
    command_arg: AdapterMessage = CommandArg(),
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
        event: AdapterGroupMessageEvent,
        url: str = ArgPlainText("url")
):
    msg_type = ProtocolAdapter.get_msg_type(event)
    msg_type_id = ProtocolAdapter.get_msg_type_id(event)
    ret_msg = ""
    work_list = DBPluginsCaptionsGroupsInfo.get_work_list_by_msg_type_id(msg_type, msg_type_id)
    if work_list:
        ret_msg = "【原工作表已被覆盖】\n"
    DBPluginsCaptionsGroupsInfo.set_work_list(msg_type, msg_type_id, url)
    ret_msg += "已写入工作表"
    await set_work_list.finish(ret_msg)
