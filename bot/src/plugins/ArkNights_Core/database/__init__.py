"""
本模块负责管理所有的数据库
"""

from .searcher import DataSearcher
from .connecter import operator_conn, item_conn, skill_conn, other_conn

searcher = DataSearcher()


__all__ = [searcher, operator_conn, item_conn, skill_conn, other_conn]
