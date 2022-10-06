from typing import List

from lxml import etree
from fake_useragent import UserAgent

from .core import async_get, GetRequest, ua
from .prts_utils import get_file_page, get_img_url


async def down_img_resource(urls: List[str]) -> List[bytes]:
    '''
    获取prts图片资源

    :param url: <str> 文件页面的url
    :return: <str> 页面的HTML文本
    '''
    img_urls = await get_img_url(urls)
    headers = {
        'user-agent': ua.random
    }
    req_ls = [GetRequest(url=url, headers=headers) for url in img_urls]
    responses = await async_get(req_ls)
    return [resp.content for resp in responses]


async def down_stand_phase_0(operator_name: str) -> bytes:
    '''
    获取干员精0立绘

    :param operator_name: <str> 干员名
    :return: <bytes> 干员精0立绘的二进制数据
    '''
    url = f'https://prts.wiki/w/文件:立绘_{operator_name}_1.png'
    return (await down_img_resource([url, ]))[0]

async def down_stand_phase_1(operator_name: str) -> bytes:
    '''
    获取干员精0立绘

    :param operator_name: <str> 干员名
    :return: <bytes> 干员精0立绘的二进制数据
    '''
    url = f'https://prts.wiki/w/文件:立绘_{operator_name}_1+.png'
    return (await down_img_resource([url, ]))[0]


async def down_stand_phase_2(operator_name: str) -> bytes:
    '''
    获取干员精0立绘

    :param operator_name: <str> 干员名
    :return: <bytes> 干员精0立绘的二进制数据
    '''
    url = f'https://prts.wiki/w/文件:立绘_{operator_name}_2.png'
    return (await down_img_resource([url, ]))[0]


async def down_skill_icon(skills: List[str]) -> List[bytes]:
    '''
    获取技能图标

    :param skill_name: <str> 技能名
    :return: <bytes> 技能图标的二进制数据
    '''
    urls = [f'https://prts.wiki/w/文件:技能_{skill}.png' for skill in skills]
    return await down_img_resource(urls)

async def down_item_icon(items: List[str], is_border: bool = True) -> List[bytes]:
    '''
    获取物品图标

    :param item_name: <List[str]> 物品名列表
    :param is_border: <bool> 物品图片是否有带框
    :return: <List[bytes]> 物品图标的二进制数据列表
    '''
    if is_border:
        urls = [f'https://prts.wiki/w/文件:道具_带框_{item}.png' for item in items]
    else:
        urls = [f'https://prts.wiki/w/文件:道具_{item}.png' for item in items]
    return await down_img_resource(urls)


async def get_item_icon_url(items: List[str], is_border: bool = True) -> List[str]:
    '''
    获取物品图标url

    :param items: <List[str]> 物品名称列表
    :param is_border: <bool> 物品图片是否有边框
    :return: <List[str]> 物品图标的url列表
    '''
    if is_border:
        urls = [f'https://prts.wiki/w/文件:道具_带框_{item}.png' for item in items]
    else:
        urls = [f'https://prts.wiki/w/文件:道具_{item}.png' for item in items]
    return await get_img_url(urls)


async def down_mastery_icon() -> List[bytes]:
    '''
    获取技能专精图标

    :return: <list[bytes]> 专精图标的二进制数据列表
    '''
    urls = [f'https://prts.wiki/w/文件:专精_{i+1}.png' for i in range(3)]
    return await down_img_resource(urls)
