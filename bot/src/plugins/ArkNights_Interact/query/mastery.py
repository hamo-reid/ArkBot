from nonebot.plugin import on_regex
from nonebot.typing import T_State
from nonebot.params import State
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.adapters.onebot.v11.message import MessageSegment

from nonebot import require

require("ArkNights_Core")
from src.plugins.ArkNights_Core.database import searcher
from src.plugins.ArkNights_Core.image import image_manager
require("ArkNights_Custom")
from src.plugins.ArkNights_Custom.utils import obtain_operator_name

mastery = on_regex(r"^(查询)?(.*)专精材料$", priority=5)

@mastery.handle()
async def _(bot: Bot, event: Event, state: T_State = State()):
    mark = list(state["_matched_groups"])[1]
    name = obtain_operator_name(mark)
    print(name)
    if name is not None:
        if searcher.operator.get_operator_rarity(name) > 2:
            await mastery.finish(
                MessageSegment.image(await image_manager.get_mastery_image(name))
            )
        else:
            await mastery.finish(MessageSegment.text("该干员无法专精"))
    else:
        await mastery.finish(MessageSegment.text("干员不存在"))