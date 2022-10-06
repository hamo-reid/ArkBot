"""
负责所有图片资源的获取和管理
"""

from io import BytesIO
from .mastery import mastery_generate
from .promotion import promotion_generate
from ..assets_manager import assets_manager

class ImageManager:
    async def get_mastery_image(self, operator: str) -> BytesIO:
        """
        获取专精图片，优先向资源管理器索取，若无则生成并保存
        """
        if assets_manager.mastery_exist(operator):
            image = assets_manager.read_mastery_product(operator)
            return image
        else:
            image = await mastery_generate(operator)
            assets_manager.save_mastery_product(operator, image)
            return image
    
    async def get_promotion_image(self, operator: str) -> BytesIO:
        """
        获取精英化图片，优先向资源管理器索取，若无则生成并保存
        """
        if assets_manager.promotion_exist(operator):
            image = assets_manager.read_promotion_product(operator)
            return image
        else:
            image = await promotion_generate(operator)
            assets_manager.save_promotion_product(operator, image)
            return image

image_manager = ImageManager()
