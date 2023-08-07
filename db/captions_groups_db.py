from tortoise.fields.data import CharField, IntField
from plugins.db_base_model import PluginsDBBaseModel


# 字幕组数据
class CaptionsGroupsData(PluginsDBBaseModel):
    type = CharField(max_length=16)                 # 类型 群,私聊...
    type_id = IntField()                            # 类型对应的ID
    work_list = CharField(max_length=64)            # 工作表链接
    welcome_content = CharField(max_length=255)     # 欢迎文字
