from pathlib import Path
import asyncio
from jinja2 import Environment, FileSystemLoader, Template

class Render:
    """
    模板渲染类
    """
    def __init__(self, template_path: Path) -> None:
        """
        设置模板文件夹
        """
        self._env = Environment(
            loader=FileSystemLoader(template_path),
            enable_async=True
        )
    
    async def get_template(self, template_name: str) -> Template:
        """
        
        """
        return self._env.get_template(template_name)
    
    async def render_template(self, template_name: str, params: dict) -> str:
        template = await self.get_template(template_name)
        return await template.render_async(**params)