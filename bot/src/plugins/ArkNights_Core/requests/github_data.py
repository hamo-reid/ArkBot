from fake_useragent import UserAgent
from .core import GetRequest, async_get


ua = UserAgent()

async def down_json(url: str) -> dict:
    headers = {
        'user-agent': ua.random
    }
    response = (await async_get([GetRequest(url=url, headers=headers), ]))[0]
    return response.json()

async def down_character_table() -> dict:
    return await down_json('https://raw.githubusercontents.com/Kengxxiao/ArknightsGameData/master/zh_CN/gamedata/excel/character_table.json')

async def down_char_patch_table() -> dict:
    return await down_json('https://raw.githubusercontents.com/Kengxxiao/ArknightsGameData/master/zh_CN/gamedata/excel/char_patch_table.json')

async def down_item_table() -> dict:
    return await down_json('https://raw.githubusercontents.com/Kengxxiao/ArknightsGameData/master/zh_CN/gamedata/excel/item_table.json')

async def down_handbook_team_table() -> dict:
    return await down_json('https://raw.githubusercontents.com/Kengxxiao/ArknightsGameData/master/zh_CN/gamedata/excel/handbook_team_table.json')

async def down_uniequip_table() -> dict:
    return await down_json('https://raw.githubusercontents.com/Kengxxiao/ArknightsGameData/master/zh_CN/gamedata/excel/uniequip_table.json')

async def down_skill_table() -> dict:
    return await down_json('https://raw.githubusercontents.com/Kengxxiao/ArknightsGameData/master/zh_CN/gamedata/excel/skill_table.json')