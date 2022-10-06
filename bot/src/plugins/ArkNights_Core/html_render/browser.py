import asyncio
from typing import Union
from pathlib import Path

from playwright.async_api import Page, Error ,Browser, Playwright, async_playwright
from .render import Render

class RenderBrowser:
    def __init__(self, template_path: Path = None) -> None:
        self._browser: Browser
        self._render: Render = None
        if template_path is not None:
            self._template_path = template_path
            self._render = Render(template_path)
            
    
    async def init(self, **kwargs):
        self._playwright = await async_playwright().start()
        try:
            self._browser = await self.launch_browser(**kwargs)
        except Error:
            await self.install_browser()
            self._browser = await self.launch_browser(**kwargs)

    async def launch_browser(self, **kwargs):
        try:
            browser = await self._playwright.chromium.launch(**kwargs)
        except Error:
            await self.install_browser()
            browser = await self._playwright.chromium.launch(**kwargs)
        return browser

    async def install_browser(self):
        import os
        import sys

        from playwright.__main__ import main

        sys.argv = ["", "install", "chromium"]
        try:
            os.system("playwright install-deps")
            main()
        except SystemExit:
            pass
    
    async def shutdown(self):
        if self._browser:
            await self._browser.close()
        if self._playwright:
            await self._playwright.stop()

    async def screenshot_html(self, html: Union[str, Path], viewport: dict) -> bytes:
        if isinstance(html, Path):
            with html.open('r', encoding='utf-8') as fp:
                html = fp.read()
        page = await self._browser.new_page(viewport=viewport)
        await page.set_content(html, wait_until="networkidle")
        await page.wait_for_timeout(2)
        img_raw = await page.screenshot(full_page=True)
        return img_raw
    
    async def screenshot_template(self, tamplate_name: str, params: dict, viewport: dict) -> bytes:
        if self._render is None:
            raise 'RenderBrowser do not have render'
        page = await self._browser.new_page(viewport=viewport)
        await page.goto(f'file:///{str(self._template_path / tamplate_name)}')
        html = await self._render.render_template(tamplate_name, params)
        await page.set_content(html, wait_until="networkidle")
        await page.wait_for_timeout(2)
        img_raw = await page.screenshot(full_page=True, quality=100, type="jpeg")
        return img_raw
        



    
