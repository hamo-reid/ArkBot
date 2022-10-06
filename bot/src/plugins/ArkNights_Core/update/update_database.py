from ..database import operator_conn, item_conn, skill_conn
from ..models import Operator, Item, Skill
from ..analysis import get_operators, get_items, get_skills
from ..requests.github_data import (
    down_character_table,
    down_item_table,
    down_skill_table,
)
from ..requests.github_monitor import check_execl_update, monitor_json, monitor_excel
from ..recorder import recorder


async def update_database():
    """
    更新所有数据库数据的函数
    """
    # 有更新且在列表内才进行更新
    is_update = await check_execl_update()
    json_dict = await monitor_json()
    if is_update and json_dict:
        if "character_table.json" in json_dict:
            await update_operator()
        if "item_table.json" in json_dict:
            await update_item()
        if "skill_table.json" in json_dict:
            await update_skill()
        recorder.excel_stamp = await monitor_excel()
        recorder.jsons_stamp.update(json_dict)
        recorder.save_record()
    else:
        pass


async def update_operator():
    """
    更新operator数据库的函数
    """
    operators = get_operators(await down_character_table())
    operator_ids = tuple(operators.keys())
    operator_objs = tuple(Operator(**operator) for operator in operators.values())
    operator_conn.insert_base(operator_ids, operator_objs)
    operator_conn.insert_phase(operator_objs)
    operator_conn.insert_mastery(operator_objs)
    operator_conn.insert_levelUp(operator_objs)


async def update_item():
    """
    更新item数据库的函数
    """
    item_table = await down_item_table()
    items = get_items(item_table)
    item_objs = tuple(Item(**item) for item in items.values())
    item_conn.insert_item(item_objs)


async def update_skill():
    """
    更新skill数据库的数据
    """
    skill_table = await down_skill_table()
    skills = get_skills(skill_table)
    skill_objs = tuple(Skill(**skill) for skill in skills.values())
    skill_conn.insert_skill(skill_objs)
