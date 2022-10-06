from pathlib import Path

from nonebot import require

require("ArkNights_Core")
from src.plugins.ArkNights_Core.database.connecter import DBConnecter

from ..paths import custom_db_collection

class NicknameConn(DBConnecter):
    def __init__(self, db_path: Path) -> None:
        super().__init__(db_path)

    def init_tables(self):
        if self.is_empty:
            sql = "CREATE TABLE IF NOT EXISTS nickname(nickname VARCHAR PRIMARY KEY, name VARCHAR)"
            self.cur.execute(sql)


    @property
    def existed_nickname(self):
        sql = "SELECT nickname FROM nickname"
        return tuple(_[0] for _ in self.cur.execute(sql).fetchall())
    
    def insert_nickname(self, nickname: str, operator_name: str):
        sql = "INSERT INTO nickname (nickname, name) VALUES (?, ?)"
        self.cur.execute(sql, (nickname, operator_name))
        self.commit()
    
    def delete_nickname(self, nickname: str):
        sql = "DELETE FROM nickname WHERE nickname = ?"
        self.cur.execute(sql, (nickname, ))
        self.commit()
    
    def search_operater(self, nickname: str) -> str:
        sql = "SELECT name FROM nickname WHERE nickname = ?"
        self.cur.execute(sql, (nickname, ))
        return self.cur.fetchone()[0]

nickname_conn = NicknameConn(custom_db_collection["nickname"])