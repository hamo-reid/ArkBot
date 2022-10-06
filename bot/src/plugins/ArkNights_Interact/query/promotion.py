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

promotion = on_regex(r"^(查询)?(.*)精英材料$", priority=5)

@promotion.handle()
async def _(bot: Bot, event: Event, state: T_State = State()):
    mark = list(state["_matched_groups"])[1]
    name = obtain_operator_name(mark)
    if name is not None:
        if searcher.operator.get_operator_rarity(name) > 1:
            await promotion.finish(
                MessageSegment.image(await image_manager.get_promotion_image(name))
            )
        else:
            await promotion.finish(MessageSegment.text("该干员无法精英化"))
    else:
        await promotion.finish(MessageSegment.text("干员不存在"))