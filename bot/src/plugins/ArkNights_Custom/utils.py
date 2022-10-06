from typing import Union

from nonebot import require

require("ArkNights_Core")
from src.plugins.ArkNights_Core.database import searcher

from .database import nickname_conn

def obtain_operator_name(mark: str) -> Union[str, None]:
    """
    获取干员名称，可为干员名，或别名
    """
    if mark in nickname_conn.existed_nickname:
        return nickname_conn.search_operater(mark)
    else:
        if mark in searcher.operator.get_all_name():
            return mark
        else:
            return None
