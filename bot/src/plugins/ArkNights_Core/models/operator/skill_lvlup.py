from typing import List

from pydantic import BaseModel


class CostItem(BaseModel):
    id: str
    count: int
    type: str


class LvlUpCostCond(BaseModel):
    lvlUpCost: List[CostItem]

