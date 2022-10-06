from typing import Union

from pydantic import BaseModel

class Item(BaseModel):
    itemId: str
    name: str
    description: Union[str, None]
    rarity: int
    sortId: int
    usage: Union[str, None]
    obtainApproach: Union[str, None]
    classifyType: str