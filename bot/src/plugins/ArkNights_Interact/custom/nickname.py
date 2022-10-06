from nonebot.plugin import on_regex
from nonebot.typing import T_State
from nonebot.params import State
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.adapters.onebot.v11.message import MessageSegment

from nonebot import require
require("ArkNights_Core")
from src.plugins.ArkNights_Core.database import searcher
require("ArkNights_Custom")
from src.plugins.ArkNights_Custom.database import nickname_conn

add_nickname = on_regex(r"^为(.*)添加别名(.*)$", priority=5)

@add_nickname.handle()
async def _(state: T_State = State()):
    _match_result = list(state["_matched_groups"])
    name = _match_result[0]
    if name in searcher.operator.get_all_name():
        nickname = _match_result[1]
        if nickname not in nickname_conn.existed_nickname:
            nickname_conn.insert_nickname(nickname, name)
            await add_nickname.finish(MessageSegment.text(f"已为{name}新增别名{nickname}"))
        else:
            owner = nickname_conn.search_operater(nickname)
            await add_nickname.finish(MessageSegment.text(f"干员别名已存在，所属于{owner}"))
    else:
        await add_nickname.finish(MessageSegment.text("干员不存在"))

del_nickname = on_regex(r"^删除(.*)别名(.*)$", priority=5)

@del_nickname.handle()
async def _(state: T_State = State()):
    _match_result = list(state["_matched_groups"])
    name = _match_result[0]
    if name in searcher.operator.get_all_name():
        nickname = _match_result[1]
        if nickname in nickname_conn.existed_nickname:
            nickname_conn.delete_nickname(nickname)
            await del_nickname.finish(MessageSegment.text(f"已删除{name}别名{nickname}"))
        else:
            await del_nickname.finish(MessageSegment.text("干员别名不存在"))
    else:
        await del_nickname.finish(MessageSegment.text("干员不存在"))