"""
负责晋升图片的生成
"""

from io import BytesIO
from typing import List

from ..database import searcher
from ..models.operator.phase import CostItem
from ..requests.prts_url import get_item_icon_url, get_half_body_0_url, get_subProfession_icon_url
from ..html_render import RenderBrowser
from ..paths import TEMPLATE_PATH

class PromotionData():
    def __init__(self, operator_name: str) -> None:
        self.operator_name = operator_name
        subProfessionId = searcher.operator.get_operator_subProfession(operator_name)
        self.subProfession =  searcher.other.get_subProfession_name(subProfessionId)
        self.rarity = searcher.operator.get_operator_rarity(operator_name)
        self.promotion_costs = self.get_costs()
    
    @property
    def item_set(self) -> List[str]:
        item_set = set()
        item_set.add("龙门币")
        for evolve in self.promotion_costs:
            for item in evolve:
                item_set.add(item)
        return item_set
    
    def get_costs(self) -> List[dict]:
        """
        对数据进行解析
        """
        promotion_costs = searcher.operator.get_promotion_costs(self.operator_name)
        costs_list = []
        for index, evolve in enumerate(promotion_costs):
            costs_dict = {}
            # 向材料里添加龙门币
            if index == 0:
                if self.rarity == 2:
                    costs_dict.update({"龙门币": "1W"})
                elif self.rarity == 3:
                    costs_dict.update({"龙门币": "1.5W"})
                elif self.rarity == 4:
                    costs_dict.update({"龙门币": "2W"})
                elif self.rarity == 5:
                    costs_dict.update({"龙门币": "3W"})
            elif index == 1:
                if self.rarity == 3:
                    costs_dict.update({"龙门币": "6W"})
                elif self.rarity == 4:
                    costs_dict.update({"龙门币": "12W"})
                elif self.rarity == 5:
                    costs_dict.update({"龙门币": "18W"})
            costs_list.append(costs_dict)
            for item in evolve:
                item_name = searcher.item.get_item_name(item.id)
                costs_dict.update(
                    {item_name: item.count}
                )
        return costs_list

async def promotion_generate(operator: str = None) -> BytesIO:
    promotion_data = PromotionData(operator)
    item_list = list(promotion_data.item_set)
    item_urls = await get_item_icon_url(item_list, is_border=True)
    item_url_dict = {item: url for item, url in zip(item_list, item_urls)}
    promotion_costs = promotion_data.promotion_costs
    half_body_url = await get_half_body_0_url(promotion_data.operator_name)
    subProfession_url = await get_subProfession_icon_url(promotion_data.subProfession)
    params = {
        "half_body_url": half_body_url,
        "subProfession_url": subProfession_url,
        "item_url_dict": item_url_dict,
        "operater": promotion_data.operator_name,
        "subProfession": promotion_data.subProfession,
        "promotion_costs": promotion_costs,
    }
    browser = RenderBrowser(TEMPLATE_PATH)
    await browser.init()
    bufffer = BytesIO(
        await browser.screenshot_template(
            "promotion/index.html",
            params=params,
            viewport={"width": 1500, "height": 700},
        )
    )
    await browser.shutdown()
    return bufffer
