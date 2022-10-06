from nonebot import require

require("ArkNights_Core")
from src.plugins.ArkNights_Core.paths import DB_PATH

CUSTOM_DB_PATH = DB_PATH / "custom"

custom_db_collection = {"nickname": CUSTOM_DB_PATH / "nickname.db"}
