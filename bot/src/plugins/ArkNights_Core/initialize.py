"""
本模块负责初始化操作
"""

from .paths import *
from .requests.github_data import (
    down_character_table,
    down_char_patch_table,
    down_item_table, 
    down_skill_table, 
    down_handbook_team_table,
    down_uniequip_table,
)
from .analysis import *
from .models import *


async def total_init():
    if not TOTAL_PATH.exists():
        init_folder()
        init_database()
        await init_insert_database()

def init_folder():
    '''
    初始化生成文件夹
    '''
    if not TOTAL_PATH.exists():  # 创建总资源文件夹
        TOTAL_PATH.mkdir()
    if not ASSETS_PATH.exists():  # 创建资源文件夹
        ASSETS_PATH.mkdir()
    if not RESOURCE_PATH.exists():  # 创建素材文件夹
        RESOURCE_PATH.mkdir()
    for path in resource_collection.values(): # 创建素材文件夹的子文件夹
        if not path.exists():
            path.mkdir()
    if not PRODUCT_PATH.exists():  # 创建已生成图片文件夹
        PRODUCT_PATH.mkdir()
    for path in product_collection.values(): # 创建已生成图片的子文件夹
        if not path.exists():
            path.mkdir()
    if not DB_PATH.exists():  # 创建数据库文件夹
        DB_PATH.mkdir()

def init_database():
    '''
    初始化生成数据库
    '''
    from .database import operator_conn, item_conn, skill_conn, other_conn
    operator_conn.init_tables()
    item_conn.init_tables()
    skill_conn.init_tables()
    other_conn.init_tables()

async def init_insert_database():
    '''
    初次插入数据库
    '''
    from .database import operator_conn, item_conn, skill_conn, other_conn
    # 插入operater
    character_table = await down_character_table()
    char_patch_table = await down_char_patch_table()
    operators = get_operators(character_table, char_patch_table)
    operator_ids = tuple(operators.keys())
    operator_objs = tuple(Operator(**operator) for operator in operators.values())
    operator_conn.insert_base(operator_ids, operator_objs)
    operator_conn.insert_phase(operator_objs)
    operator_conn.insert_mastery(operator_objs)
    operator_conn.insert_levelUp(operator_objs)
    operator_conn.commit()

    item_table = await down_item_table()
    items = get_items(item_table)
    item_objs = tuple(Item(**item) for item in items.values())
    item_conn.insert_item(item_objs)

    skill_table = await down_skill_table()
    skills = get_skills(skill_table)
    skill_objs = tuple(Skill(**skill) for skill in skills.values())
    skill_conn.insert_skill(skill_objs)

    team_table = await down_handbook_team_table()
    teams = get_teams(team_table)
    team_objs = tuple(Team(**team) for team in teams.values())
    other_conn.insert_team(team_objs)
    professions = get_professions()
    professions_objs = tuple(Profession(**profession) for profession in professions.values())
    other_conn.insert_profession(professions_objs)
    uniequip_table = await down_uniequip_table()
    subProfessions = get_subprofessions(uniequip_table)
    subProfessions_objs = tuple(SubProfession(**subProfession) for subProfession in subProfessions.values())
    other_conn.insert_subProfession(subProfessions_objs)
