from typing import List

from pydantic import BaseModel

class CostItem(BaseModel):
    id: str
    count: int
    type: str

class MasteryCostCond(BaseModel):
    lvlUpTime: int
    levelUpCost: List[CostItem]

class SkillMasteryFrame(BaseModel):
    skillId: str
    levelUpCostCond: List[MasteryCostCond]
