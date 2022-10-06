from pydantic import BaseModel

class Profession(BaseModel):
    professionId: str
    professionName: str

class SubProfession(BaseModel):
    subProfessionId: str
    subProfessionName: str