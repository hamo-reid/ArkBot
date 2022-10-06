from typing import List

from lxml import etree

from .core import async_get, GetRequest, ua

async def get_file_page(urls: List[str]) -> List[str]:
    '''
    获取文件页面的HTML文本

    :param urls: <List[str]> 文件页面url列表
    :return: <List[str]> 文件页面的html文本列表
    '''
    headers = {
        'user-agent': ua.random
    }
    req_ls = [GetRequest(url=url, headers=headers) for url in urls]
    responses = await async_get(req_ls)
    return [resp.text for resp in responses]

async def get_img_url(urls: List[str]) -> List[str]:
    '''
    通过文件页面的url获取图片的url

    :params url: <List[str]> 文件页面url列表
    :return: <List[str]> 图片url列表
    '''
    text_ls = await get_file_page(urls)
    image_url_ls = []
    for text in text_ls:
        tree = etree.HTML(text)
        image_url = 'https://prts.wiki' + \
            tree.xpath('//div[@class="fullImageLink"]/a/@href')[0]
        image_url_ls.append(image_url)
    return image_url_ls

async def get_skill_icon_url(skills: List[str]) -> List[str]:
    urls = [f'https://prts.wiki/w/文件:技能_{skill}.png' for skill in skills]
    return await get_img_url(urls)

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