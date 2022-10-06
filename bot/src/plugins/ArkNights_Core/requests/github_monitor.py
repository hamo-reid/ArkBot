from datetime import datetime
import time
from typing import List, Dict

from fake_useragent import UserAgent
from lxml import etree

from .core import async_get, GetRequest
from ..recorder import recorder

ua = UserAgent()

excel_url = (
    "https://github.com/Kengxxiao/ArknightsGameData/commits/master/zh_CN/gamedata/excel"
)

monitor_list = [
    "character_table.json",
    "item_table.json",
    "skill_table.json",
]


async def monitor_github(urls: List[str]) -> List[float]:
    """
    获取github文件/文件夹最新的commit时间
    """
    reqs = tuple(GetRequest(url=url) for url in urls)
    responses = await async_get(req_list=reqs)
    least_stamp_list = []
    for response in responses:
        tree = etree.HTML(response.text)
        container = tree.xpath(
            "//div[@class='js-navigation-container js-active-navigation-container mt-3']"
        )[0]
        least_commit = container.xpath(".//h2[@class='f5 text-normal']/text()")[0]
        day = datetime.strptime(least_commit, "Commits on %b %d, %Y")
        least_stamp_list.append(time.mktime(day.timetuple()))
    return least_stamp_list


async def monitor_excel() -> float:
    least_stamp = (
        await monitor_github(
            [
                excel_url,
            ]
        )
    )[0]
    return least_stamp


async def check_execl_update() -> bool:
    """
    检查excel文件夹commit时间
    若获取时间比记录时间更新返回True
    """
    least_stamp = (
        await monitor_github(
            [
                excel_url,
            ]
        )
    )[0]
    if least_stamp > recorder.excel_stamp:
        return True
    else:
        return False


async def monitor_json() -> Dict[str, float]:
    """
    检查监视列表中的json文件是否有更新
    """
    old_jsons_stamp = recorder.jsons_stamp.copy()
    new_jsons_stamp = await monitor_github(
        [excel_url + "/" + json_name for json_name in monitor_list]
    )
    return {
        name: stamp
        for name, stamp in zip(monitor_list, new_jsons_stamp)
        if stamp > old_jsons_stamp[name]
    }
