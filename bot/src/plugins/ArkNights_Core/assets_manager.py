"""
本模块负责管理静态资源文件，即arknights文件夹下assets文件夹内的内容
包括资源及成品
"""

from io import BytesIO

from .paths import product_collection

class AssetsManager:
    """
    资源管理类
    """
    def mastery_exist(self, operator: str) -> bool:
        path = product_collection["mastery"]
        if (path / f"{operator}.jpg").exists():
            return True
        else:
            return False
    
    def promotion_exist(self, operator: str) -> bool:
        path = product_collection["promotion"]
        if (path / f"{operator}.jpg").exists():
            return True
        else:
            return False

    def save_mastery_product(self, operator: str, image: BytesIO):
        path = product_collection["mastery"]
        with (path / f"{operator}.jpg").open('wb') as fp:
            fp.write(image.getbuffer())

    def read_mastery_product(self, operator: str) -> BytesIO:
        path = product_collection["mastery"]
        if self.mastery_exist(operator):
            with (path / f"{operator}.jpg").open("rb") as fp:
                return BytesIO(fp.read())
        else:
            raise "Image not existed."
    
    def save_promotion_product(self, operator: str, image: BytesIO):
        path = product_collection["promotion"]
        with (path / f"{operator}.jpg").open('wb') as fp:
            fp.write(image.getbuffer())

    def read_promotion_product(self, operator: str) -> BytesIO:
        path = product_collection["promotion"]
        if self.promotion_exist(operator):
            with (path / f"{operator}.jpg").open("rb") as fp:
                return BytesIO(fp.read())
        else:
            raise FileNotFoundError("Image not existed.")


assets_manager = AssetsManager()