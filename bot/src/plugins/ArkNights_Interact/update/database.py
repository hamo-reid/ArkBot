from nonebot.plugin import on_fullmatch
from nonebot.permission import SUPERUSER

from nonebot import require

require("ArkNights_Core")
from src.plugins.ArkNights_Core.update import update_database

update_db = on_fullmatch("update", priority=4, permission=SUPERUSER)

@update_db.handle()
async def _():
    await update_database()
    await update_db.finish("更新完毕")