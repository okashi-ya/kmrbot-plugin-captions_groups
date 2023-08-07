import os
from pathlib import Path
from nonebot import get_driver
from tortoise import Tortoise
from tortoise.connection import connections
from plugins.common_plugins_function import get_plugin_db_path
from .captions_groups_db import CaptionsGroupsData


class CaptionsGroupsDBUtils:

    @classmethod
    async def init(cls):
        plugin_name = os.path.split(Path(os.path.dirname(os.path.dirname(__file__))))[1]
        config = {
            "connections": {
                "captions_groups_data_conn": f"sqlite://{get_plugin_db_path('captions_groups_data.sqlite3')}"
            },
            "apps": {
                "kmr_bot_app": {
                    "models": [f"plugins.{plugin_name}.db.captions_groups_db"],
                    "default_connection": "captions_groups_data_conn",
                }
            }
        }

        await Tortoise.init(config)
        await Tortoise.generate_schemas()

    @classmethod
    async def get_work_list(cls, **kwargs):
        """ 获取工作表 """
        data = await CaptionsGroupsData.get(**kwargs).first()
        return data.work_list if data is not None else None

    @classmethod
    async def set_work_list(cls, **kwargs):
        """ 设置工作表 """
        if not await CaptionsGroupsData.get(type=kwargs["type"], type_id=kwargs["type_id"]):
            await CaptionsGroupsData.add(
                type=kwargs["type"],
                type_id=kwargs["type_id"],
                work_list=kwargs["work_list"],
                welcome_content="")
        else:
            await CaptionsGroupsData.update({
                "type": kwargs["type"],
                "type_id": kwargs["type_id"]},
                work_list=kwargs["work_list"])

    @classmethod
    async def get_welcome_content(cls, **kwargs):
        """ 获取欢迎文字 """
        data = await CaptionsGroupsData.get(**kwargs).first()
        return data.welcome_content if data is not None else None

    @classmethod
    async def set_welcome_content(cls, **kwargs):
        """ 设置欢迎文字 """
        if not await CaptionsGroupsData.get(type=kwargs["type"], type_id=kwargs["type_id"]):
            await CaptionsGroupsData.add(
                type=kwargs["type"],
                type_id=kwargs["type_id"],
                work_list="",
                welcome_content=kwargs["welcome_content"])
        else:
            await CaptionsGroupsData.update({
                "type": kwargs["type"],
                "type_id": kwargs["type_id"]},
                welcome_content=kwargs["welcome_content"])


get_driver().on_startup(CaptionsGroupsDBUtils.init)
# get_driver().on_shutdown(connections.close_all)
