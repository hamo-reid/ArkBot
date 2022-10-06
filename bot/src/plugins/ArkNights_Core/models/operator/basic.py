from typing import Union, List

from pydantic import BaseModel

from .phase import Phase
from .skill_mastery import SkillMasteryFrame
from .skill_lvlup import LvlUpCostCond

class Operator(BaseModel):
    name: str  # 干员名称
    appellation: str  # 代号
    displayNumber: str  # 编号
    rarity: int  # 稀有度
    nationId: Union[str, None]
    groupId: Union[str, None]
    teamId: Union[str, None]
    tagList: List[str]
    profession: str  # 职业
    subProfessionId: str  # 子职业
    phases: List[Phase]  # 阶段数据
    skills: List[SkillMasteryFrame]  # 技能专精数据
    allSkillLvlup: List[LvlUpCostCond]  # 技能升级数据

