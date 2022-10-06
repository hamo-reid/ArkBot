"""
本模块负责对某些节点进行记录
"""

from typing import Dict

from pydantic import BaseModel
import ujson

from .paths import TOTAL_PATH

class Record(BaseModel):
    excel_stamp: float = 0
    jsons_stamp: dict = {
        "character_table.json": 0,
        "item_table.json": 0,
        "skill_table.json": 0,
    }

class Recorder:
    def __init__(self) -> None:
        self.__record_path = (TOTAL_PATH / "record.json")
        self.__record: Record = self.read_record()
    
    @property
    def excel_stamp(self):
        return self.__record.excel_stamp
    
    @excel_stamp.setter
    def excel_stamp(self, value: float):
        self.__record.excel_stamp = value

    @property
    def jsons_stamp(self):
        return self.__record.jsons_stamp
    
    @jsons_stamp.setter
    def jsons_stamp(self, value: Dict[str, float]):
        self.__record.jsons_stamp = value
        
    def read_record(self):
        if self.__record_path.exists():
            record_str = self.__record_path.read_text(encoding="utf-8")
            return Record(**ujson.loads(record_str))
        else:
            return Record()
    
    def save_record(self):
        with self.__record_path.open("w", encoding="utf-8") as fp:
            fp.write(ujson.dumps(self.__record.dict()))

recorder = Recorder()