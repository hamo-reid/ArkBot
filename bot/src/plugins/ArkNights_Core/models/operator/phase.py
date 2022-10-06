from typing import List, Union

from pydantic import BaseModel

class AttributesData(BaseModel):
    maxHp: int
    atk: int
    magicResistance: float
    cost: int
    blockCnt: int
    moveSpeed: float
    attackSpeed: float
    baseAttackTime: float
    respawnTime: int
    hpRecoveryPerSec: float
    spRecoveryPerSec: float
    maxDeployCount: int
    maxDeckStackCnt: int
    tauntLevel: int
    massLevel: int
    baseForceLevel: int
    stunImmune: bool
    silenceImmune: bool
    sleepImmune: bool
    frozenImmune: bool
    levitateImmune: bool

class AttributesFrame(BaseModel):
    level: int
    data: AttributesData


class CostItem(BaseModel):
    id: str
    count: int
    type: str

class Phase(BaseModel):
    rangeId: str
    maxLevel: int
    attributesKeyFrames: List[AttributesFrame]
    evolveCost: Union[List[CostItem], None]

