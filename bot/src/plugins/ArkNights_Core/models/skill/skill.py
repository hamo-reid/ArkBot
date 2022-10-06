from typing import Dict, List, Union

from pydantic import BaseModel

class InsertData(BaseModel):
    key: str
    value: float

class SpData(BaseModel):
    spType: int
    levelUpCost: None
    maxChargeTime: int
    spCost: int
    initSp: int
    increment: float

class SkillLevel(BaseModel):
    name: str
    rangeId: Union[str, None]
    description: Union[str, None]
    skillType: int
    durationType: int
    spData: SpData
    duration: float
    blackboard: List[InsertData]

class Skill(BaseModel):
    skillId: str
    levels: List[SkillLevel]

