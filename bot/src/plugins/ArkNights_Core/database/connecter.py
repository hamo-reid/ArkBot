import sqlite3
from pathlib import Path
from typing import Iterable, List, Tuple, Generator

import ujson
from ..models import Operator, Item, Skill
from ..models.other import Team, Profession, SubProfession
from ..paths import OPERATOR_DB_PATH, ITEM_DB_PATH, SKILL_DB_PATH, OTHER_DB_PATH


class DBConnecter:
    def __init__(self, db_path: Path) -> None:
        self._con = sqlite3.connect(db_path)
        self._cur = self._con.cursor()

    def __del__(self):
        self._con.commit()
        self._con.close()

    @property
    def cur(self):
        return self._cur

    @property
    def is_empty(self):
        if self.cur.execute(
            "SELECT name FROM sqlite_master WHERE TYPE = 'table'"
        ).fetchall():
            return False
        else:
            return True
    
    def commit(self):
        self._con.commit()

    def select_many(self, sql: str, datas: Iterable) -> Generator:
        for data in datas:
            self._cur.execute(sql, data)
            yield self._cur.fetchone()


class OperatorConn(DBConnecter):
    def __init__(self, db_path: Path) -> None:
        super().__init__(db_path)

    def init_tables(self):
        if self.is_empty:
            sql = (
                "CREATE TABLE IF NOT EXISTS base("
                "id VARCHAR PRIMARY KEY,"
                "name VARCHAR,"
                "appellation VARCHAR,"
                "displayNumber VARCHAR(4),"
                "rarity INTEGER,"
                "nationId VARCHAR,"
                "groupId VARCHAR,"
                "teamId VARCHAR,"
                "tagList TEXT,"
                "profession VARCHAR,"
                "subProfessionId VARCHAR"
                ")"
            )
            self.cur.execute(sql)
            # 创建精英阶段表
            sql = (
                "CREATE TABLE IF NOT EXISTS phase("
                "name VARCHAR,"
                "phase_1 TEXT,"
                "phase_2 TEXT,"
                "phase_3 TEXT"
                ")"
            )
            self.cur.execute(sql)
            # 创建技能专精表
            sql = (
                "CREATE TABLE IF NOT EXISTS mastery("
                "name VARCHAR,"
                "skill_1 TEXT,"
                "skill_2 TEXT,"
                "skill_3 TEXT"
                ")"
            )
            self.cur.execute(sql)
            # 创建技能升级数据表
            sql = (
                "CREATE TABLE IF NOT EXISTS levelUp("
                "name VARCHAR,"
                "level_2 TEXT,"
                "level_3 TEXT,"
                "level_4 TEXT,"
                "level_5 TEXT,"
                "level_6 TEXT,"
                "level_7 TEXT"
                ")"
            )
            self.cur.execute(sql)
            self.commit()
        else:
            pass
    
    @property
    def existed_id(self):
        sql = "SELECT id FROM base"
        return tuple(id[0] for id in self.cur.execute(sql).fetchall())

    def get_existed_name(self, table_name: str) -> Tuple[str]:
        sql = f"SELECT name FROM {table_name}"
        return tuple(name[0] for name in self.cur.execute(sql).fetchall())

    def insert_base(self, ids: List[str], operators: List[Operator]):
        sql = "INSERT INTO base (id,name,appellation,displayNumber,rarity,nationId,groupId,teamId,tagList,profession,subProfessionId) VALUES (?,?,?,?,?,?,?,?,?,?,?)"
        existed_ids = self.existed_id
        datas = (
            (
                id,
                operator.name,
                operator.appellation,
                operator.displayNumber,
                operator.rarity,
                operator.nationId,
                operator.groupId,
                operator.teamId,
                str(operator.tagList),
                operator.profession,
                operator.subProfessionId,
            )
            for id, operator in zip(ids, operators)
            if id not in existed_ids
        )
        self.cur.executemany(sql, datas)

    def insert_phase(self, operators: List[Operator]):
        sql = "INSERT INTO phase (name,phase_1,phase_2,phase_3) VALUES (?,?,?,?)"
        names = self.get_existed_name("phase")
        # 没有精英阶段的用None占位
        datas = (
            (operator.name,)
            + tuple(
                ujson.dumps(operator.phases[_].dict())
                if _ < len(operator.phases)
                else None
                for _ in range(3)
            )
            for operator in operators
            if operator.name not in names
        )
        self.cur.executemany(sql, datas)

    def insert_levelUp(self, operators: List[Operator]):
        sql = "INSERT INTO levelUp (name,level_2,level_3,level_4,level_5,level_6,level_7) VALUES (?,?,?,?,?,?,?)"
        names = self.get_existed_name("levelUp")
        # 没有技能升级的用None占位
        datas = (
            (operator.name,)
            + tuple(
                ujson.dumps(operator.allSkillLvlup[_].dict())
                if _ < len(operator.allSkillLvlup)
                else None
                for _ in range(6)
            )
            for operator in operators
            if operator.name not in names
        )
        self.cur.executemany(sql, datas)

    def insert_mastery(self, operators: List[Operator]):
        sql = "INSERT INTO mastery (name,skill_1,skill_2,skill_3) VALUES (?,?,?,?)"
        names = self.get_existed_name("mastery")
        # 没有技能专精的用None占位
        datas = (
            (operator.name,)
            + tuple(
                ujson.dumps(operator.skills[_].dict())
                if _ < len(operator.skills)
                else None
                for _ in range(3)
            )
            for operator in operators
            if operator.name not in names
        )
        self.cur.executemany(sql, datas)


class ItemConn(DBConnecter):
    def __init__(self, db_path: Path) -> None:
        super().__init__(db_path)

    def init_tables(self):
        if self.is_empty:
            sql = (
                "CREATE TABLE IF NOT EXISTS item("
                "id VARCHAR PRIMARY KEY,"
                "name VARCHAR,"
                "description TEXT,"
                "rarity INTEGER,"
                "sortId INTEGER,"
                "usage TEXT,"
                "obtainApproach TEXT,"
                "classifyType VERCHAR"
                ")"
            )
            self.cur.execute(sql)
            self.commit()

    @property
    def existed_id(self):
        sql = "SELECT id FROM item"
        return tuple(id[0] for id in self.cur.execute(sql).fetchall())

    def insert_item(self, items: List[Item]):
        sql = "INSERT INTO item (id,name,description,rarity,sortId,usage,obtainApproach,classifyType) VALUES (?,?,?,?,?,?,?,?)"
        ids = self.existed_id
        datas = (
            (
                item.itemId,
                item.name,
                item.description,
                item.rarity,
                item.sortId,
                item.usage,
                item.obtainApproach,
                item.classifyType,
            )
            for item in items
            if item.itemId not in ids
        )
        self.cur.executemany(sql, datas)
        self.commit()


class SkillConn(DBConnecter):
    def __init__(self, db_path: Path) -> None:
        super().__init__(db_path)

    def init_tables(self):
        if self.is_empty:
            sql = (
                "CREATE TABLE IF NOT EXISTS skill("
                "id VARCHAR PRIMARY KEY,"
                "name VARCHAR,"
                "level_1 TEXT,"
                "level_2 TEXT,"
                "level_3 TEXT,"
                "level_4 TEXT,"
                "level_5 TEXT,"
                "level_6 TEXT,"
                "level_7 TEXT,"
                "mastery_1 TEXT,"
                "mastery_2 TEXT,"
                "mastery_3 TEXT"
                ")"
            )
            self.cur.execute(sql)
            self.commit()

    @property
    def existed_id(self):
        sql = "SELECT id FROM skill"
        return tuple(id[0] for id in self.cur.execute(sql).fetchall())

    def insert_skill(self, skills: List[Skill]):
        sql = (
            "INSERT INTO skill ("
            "id,"
            "name,"
            "level_1,"
            "level_2,"
            "level_3,"
            "level_4,"
            "level_5,"
            "level_6,"
            "level_7,"
            "mastery_1,"
            "mastery_2,"
            "mastery_3"
            ") VALUES (?,?,?,?,?,?,?,?,?,?,?,?)"
        )
        ids = self.existed_id
        # 不能升级/专精的用None占位
        datas = (
            (skill.skillId, skill.levels[0].name)
            + tuple(
                ujson.dumps(skill.levels[_].dict(), ensure_ascii=False)
                if _ < len(skill.levels)
                else None
                for _ in range(10)
            )
            for skill in skills
            if skill.skillId not in ids
        )
        self.cur.executemany(sql, datas)
        self.commit()

class OtherDB(DBConnecter):
    def __init__(self, db_path: Path) -> None:
        super().__init__(db_path)
    
    def init_tables(self):
        # 创建势力表
        sql = 'CREATE TABLE IF NOT EXISTS team(' \
            'id VERCHAR PRIMARY KEY,' \
            'orderNum INTEGER,' \
            'powerLevel INTEGER,' \
            'powerName VERCHAR,' \
            'powerCode VERCHAR' \
            ')'
        self.cur.execute(sql)
        # 创建职业表
        sql = 'CREATE TABLE IF NOT EXISTS profession(' \
            'id VERCHAR PRIMARY KEY,' \
            'name VERCHAR' \
            ')'
        self.cur.execute(sql)
        # 创建子职业表
        sql = 'CREATE TABLE IF NOT EXISTS subProfession(' \
            'id VERCHAR PRIMARY KEY,' \
            'name VERCHAR' \
            ')'
        self.cur.execute(sql)
        self.commit()
    
    def get_existed_id(self, table_name: str) -> Tuple[str]:
        sql = f"SELECT id FROM {table_name}"
        return tuple(name[0] for name in self.cur.execute(sql).fetchall())

    def insert_team(self, teams: List[Team]):
        sql = 'INSERT INTO team (id,orderNum,powerLevel,powerName,powerCode) VALUES (?,?,?,?,?)'
        ids = self.get_existed_id("team")
        datas = (
            (
                team.powerId,
                team.orderNum,
                team.powerLevel,
                team.powerName,
                team.powerCode
            )
            for team in teams
            if id not in ids
        )
        self.cur.executemany(sql, datas)
        self.commit()

    def insert_profession(self, professions: List[Profession]):
        sql = 'INSERT INTO profession (id,name) VALUES (?,?)'
        ids = self.get_existed_id("profession")
        datas = (
            (
                profession.professionId,
                profession.professionName
            )
            for profession in professions
            if id not in ids
        )
        self.cur.executemany(sql, datas)
        self.commit()

    def insert_subProfession(self, subProfessions: List[SubProfession]):
        sql = 'INSERT INTO subProfession (id,name) VALUES (?,?)'
        ids = self.get_existed_id("profession")
        datas = (
            (
                subProfession.subProfessionId,
                subProfession.subProfessionName,
            )
            for subProfession in subProfessions
            if id not in ids
        )
        self.cur.executemany(sql, datas)
        self.commit()

operator_conn = OperatorConn(OPERATOR_DB_PATH)
item_conn = ItemConn(ITEM_DB_PATH)
skill_conn = SkillConn(SKILL_DB_PATH)
other_conn = OtherDB(OTHER_DB_PATH)