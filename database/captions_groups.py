import copy
import re
from database.interface.db_impl_interface import DBCacheImplInterface
from database.db_manager import DBManager


# B站翻译信息
class DBPluginsCaptionsGroupsInfo(DBCacheImplInterface):

    """
    key: {msg_type}_{msg_type_id}
    """
    _default_value = {
        "work_list": "",
        "group_welcome_content": ""
    }

    @classmethod
    def is_work_list_exist(cls, msg_type, msg_type_id):
        """ 是否已经添加过工作表 """
        key = cls.generate_key(msg_type, msg_type_id)
        data = cls.get_data_by_key(key)
        return data["work_list"] is not None if (data is not None and data.get("work_list") is not None) else False

    @classmethod
    def set_work_list(cls, msg_type, msg_type_id, work_list):
        """ 设置工作表 """
        key = cls.generate_key(msg_type, msg_type_id)
        data = cls.get_data_by_key(key)
        if data is None:
            data = copy.deepcopy(cls._default_value)
        data["work_list"] = work_list
        cls.set_data_by_key(key, data)

    @classmethod
    def del_work_list(cls, msg_type, msg_type_id):
        """ 删除工作表 """
        key = cls.generate_key(msg_type, msg_type_id)
        data = cls.get_data_by_key(key)
        if data is not None:
            data["work_list"] = ""
        cls.set_data_by_key(key, data)

    @classmethod
    def get_work_list_by_msg_type_id(cls, msg_type, msg_type_id):
        """ 根据msg_type和msg_type_id 获取群欢迎内容 """
        key = cls.generate_key(msg_type, msg_type_id)
        data = cls.get_data_by_key(key)
        if data is not None:
            return data["work_list"]

    @classmethod
    def is_group_welcome_content_exist(cls, msg_type, msg_type_id):
        """ 是否已经添加过群欢迎内容 """
        key = cls.generate_key(msg_type, msg_type_id)
        data = cls.get_data_by_key(key)
        return data["group_welcome_content"] is not None \
            if (data is not None and data.get("work_list") is not None) \
            else False

    @classmethod
    def set_group_welcome_content(cls, msg_type, msg_type_id, group_welcome_content):
        """ 设置群欢迎内容 """
        key = cls.generate_key(msg_type, msg_type_id)
        data = cls.get_data_by_key(key)
        if data is None:
            data = copy.deepcopy(cls._default_value)
        data["group_welcome_content"] = group_welcome_content
        cls.set_data_by_key(key, data)

    @classmethod
    def del_group_welcome_content(cls, msg_type, msg_type_id):
        """ 删除群欢迎内容 """
        key = cls.generate_key(msg_type, msg_type_id)
        data = cls.get_data_by_key(key)
        if data is not None:
            data["group_welcome_content"] = ""
        cls.set_data_by_key(key, data)

    @classmethod
    def get_group_welcome_content_by_msg_type_id(cls, msg_type, msg_type_id):
        """ 根据msg_type和msg_type_id 获取群欢迎内容 """
        key = cls.generate_key(msg_type, msg_type_id)
        data = cls.get_data_by_key(key)
        if data is not None:
            return data["group_welcome_content"]

    @classmethod
    def db_key_name(cls, bot_id):
        # 公共的
        return f"{cls.__name__}"

    @classmethod
    async def init(cls):
        """ 初始化 """
        pass

    @classmethod
    def generate_key(cls, msg_type, msg_type_id):
        """ 生成__data内存放的key """
        return f"{msg_type}_{msg_type_id}"

    @classmethod
    def analysis_key(cls, key):
        """ 解析generate_key生成的key """
        regex_groups = re.match("([a-zA-Z]*)_([0-9]*)", key).groups()
        if regex_groups is not None:
            return {
                "msg_type": regex_groups[0],
                "msg_type_id": int(regex_groups[1]),
            }


DBManager.add_db(DBPluginsCaptionsGroupsInfo)
