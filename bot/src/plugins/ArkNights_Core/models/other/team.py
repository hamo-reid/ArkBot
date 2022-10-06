from typing import Union, List
from unicodedata import name

from pydantic import BaseModel

class Team(BaseModel):
    powerId: str
    orderNum: int
    powerLevel: int
    powerName: str
    powerCode: str