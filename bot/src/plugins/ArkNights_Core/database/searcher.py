from typing import List, Union

import ujson

from .connecter import operator_conn, item_conn, skill_conn, other_conn
from ..paths import *
from ..models.operator.skill_mastery import SkillMasteryFrame
from ..models.operator.skill_lvlup import LvlUpCostCond
from ..models.operator.phase import Phase, CostItem


class ItemSearcher:
    def get_item_data(self, id: str):
        """
        获取物品所有的数据
        """
        pass

    def get_item_name(self, id: str) -> str:
        """
        通过物品id获取物品名称

        :param id: <str> 物品id
        :return: <str> 物品名称
        """
        item_conn.cur.execute("SELECT name FROM item WHERE id = ?", (id,))
        return item_conn.cur.fetchone()[0]


class SkillSeacher:
    def get_skill_data(self, id: str):
        """
        获取技能所有的数据

        :param id: <str> 技能id
        """
        pass

    def get_skill_name(self, id: str) -> str:
        """
        通过技能id获取技能名称

        :param id: <str> 技能id
        :return: <str> 技能名称
        """
        skill_conn.cur.execute("SELECT name FROM skill WHERE id = ?", (id,))
        return skill_conn.cur.fetchone()[0]


class OperatorSearcher:
    def get_operator_name(self, id: str) -> str:
        """
        通过干员id获取干员名称

        :param id: <str> 干员id
        :return: <str> 干员名称
        """
        pass
    
    def get_operator_subProfession(self, name: str) -> str:
        operator_conn.cur.execute("SELECT subProfessionId FROM base WHERE name = ?", (name, ))
        return operator_conn.cur.fetchone()[0]

    def get_all_name(self):
        operator_conn.cur.execute("SELECT name FROM base")
        return tuple(data[0] for data in operator_conn.cur.fetchall())

    def get_operator_id(self, name: str) -> str:
        """
        通过干员名称获取干员id

        :param name: <str> 干员名称
        :return: <str> 干员id
        """
        pass

    def get_operator_rarity(self, name: str) -> int:
        """
        通过干员名称获得干员稀有度

        :param name: <str> 干员名称
        :return: <int> 干员稀有度
        """
        operator_conn.cur.execute("SELECT rarity FROM base WHERE name= ?", (name,))
        return operator_conn.cur.fetchone()[0]

    def get_mastery_data(self, name: str) -> Union[List[SkillMasteryFrame], None]:
        """
        获取干员的专精数据

        :param name: 干员名称
        """
        operator_conn.cur.execute(
            "SELECT skill_1, skill_2, skill_3 FROM mastery WHERE name =  ?", (name,)
        )
        str_data = operator_conn.cur.fetchone()
        if tuple(set(str_data)) != (None,):
            data = map(
                lambda x: SkillMasteryFrame(**ujson.loads(x)) if x is not None else x,
                str_data,
            )
            return list(data)
        else:
            return None

    def get_skill_lvlup_data(self, name: str) -> List[LvlUpCostCond]:
        """
        获取干员技能升级数据

        :param name: <str> 干员名称
        """
        operator_conn.cur.execute(
            f"SELECT level_2, level_3, level_4, level_5,level_6, level_7 FROM levelUp WHERE name = ?",
            (name,),
        )
        data = map(
            lambda x: LvlUpCostCond(**ujson.loads(x)), operator_conn.cur.fetchone()
        )
        return list(data)

    def get_promotion_costs(self, name: str) -> List[List[CostItem]]:
        """
        获取干员晋升数据（材料）
        """
        operator_conn.cur.execute(
            f"SELECT phase_1, phase_2, phase_3 FROM phase WHERE name = ?", (name,)
        )
        data = map(
            lambda x: Phase(**ujson.loads(x)).evolveCost,
            filter(lambda x: x is not None, operator_conn.cur.fetchone()),
        )
        return list(data)[1:]

class OtherSearcher():
    def get_profession_name(self, profession_id: str) -> str:
        pass

    def get_subProfession_name(self, subProfession_id: str) -> str:
        other_conn.cur.execute("SELECT name FROM subProfession WHERE id = ?", (subProfession_id, ))
        return other_conn.cur.fetchone()[0]

class DataSearcher:
    def __init__(self) -> None:
        self.item = ItemSearcher()
        self.skill = SkillSeacher()
        self.operator = OperatorSearcher()
        self.other = OtherSearcher()
