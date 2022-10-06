"""
负责技能专精图片的生成
"""
from io import BytesIO
from typing import List, Union
from ..paths import TEMPLATE_PATH
from ..database import searcher
from ..models.operator.skill_mastery import SkillMasteryFrame
from ..requests.prts_url import (
    get_stand_phase_0_url,
    get_stand_phase_2_url,
    get_item_icon_url,
    get_skill_icon_url,
    get_mastery_icon_url,
)
from ..html_render import RenderBrowser


class MasteryData:
    def __init__(self, operator_name: str) -> None:
        self.operator_name: str = operator_name
        self.rarity = searcher.operator.get_operator_rarity(operator_name)
        self.mastery_skill_data = self.get_mastery_skill_data()
        self.skill_lvlup_data = self.get_skill_lvlup_data()

    @property
    def skills(self) -> List[str]:
        """
        干员拥有的技能名
        """
        return [data["name"] for data in self.mastery_skill_data if data is not None]

    @property
    def item_set(self) -> List[str]:
        """
        干员专精所需材料的集合
        """
        item_set = set()
        for m in self.mastery_skill_data:
            if m is None:
                continue
            for level in m["costs"]:
                for item in level:
                    item_set.add(item)
        for level in self.skill_lvlup_data:
            for item in level:
                item_set.add(item)
        return item_set

    def get_mastery_skill_data(self) -> List[dict]:
        """
        获取技能专精信息
        """
        frames: list[SkillMasteryFrame, None] = searcher.operator.get_mastery_data(
            self.operator_name
        )
        data = []
        for frame in frames:
            if frame is None:
                data.append(None)
                continue
            skill_name = searcher.skill.get_skill_name(frame.skillId)
            mastery_consuption = []
            for cost_cond in frame.levelUpCostCond:
                level_cost = {}
                for item in cost_cond.levelUpCost:
                    item_name = searcher.item.get_item_name(item.id)
                    level_cost.update({item_name: item.count})
                mastery_consuption.append(level_cost)
            data.append({"name": skill_name, "costs": mastery_consuption})
        return data

    def get_skill_lvlup_data(self) -> Union[List[dict], None]:
        """
        获取技能升级数据

        :return:
        """
        if self.rarity < 2:
            return None
        cost_conds = searcher.operator.get_skill_lvlup_data(self.operator_name)
        lvlup_list = []
        for cost_cond in cost_conds:
            cost = {}
            for item in cost_cond.lvlUpCost:
                item_name = searcher.item.get_item_name(item.id)
                cost.update({item_name: item.count})
            lvlup_list.append(cost)
        return lvlup_list


async def mastery_generate(operator: str = None) -> BytesIO:
    """
    生成干员专精需求图片
    """
    operator_mastery_data = MasteryData(operator)
    item_list = list(operator_mastery_data.item_set)
    skill_list = operator_mastery_data.skills
    item_urls = await get_item_icon_url(item_list, is_border=True)
    skill_urls = await get_skill_icon_url(skill_list)
    item_url_dict = {item: url for item, url in zip(item_list, item_urls)}
    skill_url_dict = {skill: url for skill, url in zip(skill_list, skill_urls)}
    lvlup_data = operator_mastery_data.skill_lvlup_data
    mastery_skill_data = operator_mastery_data.get_mastery_skill_data()
    params = {
        "stand_0_url": await get_stand_phase_0_url(operator),
        "stand_2_url": await get_stand_phase_2_url(operator),
        "item_url_dict": item_url_dict,
        "skill_url_dict": skill_url_dict,
        "lvlup_data": lvlup_data,
        "mastery_skill_data": mastery_skill_data,
        "mastery_icons": await get_mastery_icon_url(),
    }
    browser = RenderBrowser(TEMPLATE_PATH)
    await browser.init()
    bufffer = BytesIO(
        await browser.screenshot_template(
            "mastery/mastery.html",
            params=params,
            viewport={"width": 1500, "height": 600},
        )
    )
    await browser.shutdown()
    return bufffer
