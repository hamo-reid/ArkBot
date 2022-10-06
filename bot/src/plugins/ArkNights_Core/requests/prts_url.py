from typing import List

from .prts_utils import get_img_url


async def get_stand_phase_0_url(operator_name: str) -> str:
    """
    获取干员精0立绘url

    :param operator_name: <str> 干员名
    :return: <str> 干员精0立绘url
    """
    url = f"https://prts.wiki/w/文件:立绘_{operator_name}_1.png"
    return (
        await get_img_url(
            [
                url,
            ]
        )
    )[0]


async def get_stand_phase_2_url(operator_name: str) -> str:
    """
    获取干员精2立绘url
    """
    url = f"https://prts.wiki/w/文件:立绘_{operator_name}_2.png"
    return (
        await get_img_url(
            [
                url,
            ]
        )
    )[0]


async def get_half_body_0_url(oprator_name: str) -> str:
    url = f"https://prts.wiki/w/文件:半身像_{oprator_name}_1.png"
    return (
        await get_img_url(
            [
                url,
            ]
        )
    )[0]

async def get_half_body_2_url(oprator_name: str) -> str:
    url = f"https://prts.wiki/w/文件:半身像_{oprator_name}_2.png"
    return (
        await get_img_url(
            [
                url,
            ]
        )
    )[0]


async def get_skill_icon_url(skills: List[str]) -> List[str]:
    urls = [f"https://prts.wiki/w/文件:技能_{skill}.png" for skill in skills]
    return await get_img_url(urls)


async def get_item_icon_url(items: List[str], is_border: bool = True) -> List[str]:
    """
    获取物品图标url

    :param items: <List[str]> 物品名称列表
    :param is_border: <bool> 物品图片是否有边框
    :return: <List[str]> 物品图标的url列表
    """
    if is_border:
        urls = [f"https://prts.wiki/w/文件:道具_带框_{item}.png" for item in items]
    else:
        urls = [f"https://prts.wiki/w/文件:道具_{item}.png" for item in items]
    return await get_img_url(urls)

async def get_subProfession_icon_url(subProfession: str) -> str:
    url = f"https://prts.wiki/w/文件:职业分支图标_{subProfession}.png"
    return (
        await get_img_url(
            [
                url,
            ]
        )
    )[0]


async def get_mastery_icon_url() -> List[str]:
    urls = [f"https://prts.wiki/w/文件:专精_{i+1}.png" for i in range(3)]
    return await get_img_url(urls)
