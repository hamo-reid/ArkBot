from typing import List, Union

from fuzzywuzzy import process, fuzz

def fuzzy_match_and_check(item: str, match_list: List[str], confidence: int) -> Union[None, str]:
    """
    模糊匹配函数
    :param item: 待匹配数据
    :param match_list: 全部数据的列表
    :param confidence: 置信度（取值范围为0）
    :return: 最合适匹配结果
    """
    if confidence not in range(101):
        raise(ValueError, 'Param confidence should in range of 0 to 100.')
    else:
        pass
    if item in match_list:  # 在列表中直接返回结果
        return item
    else:
        vague_result = [x[0] for x in process.extract(item, match_list, scorer=fuzz.partial_ratio, limit=10)]
        vague_result = [x[0] for x in process.extract(item, vague_result, scorer=fuzz.WRatio, limit=10)]
        result = list(process.extract(item, vague_result, scorer=fuzz.ratio, limit=1))[0]