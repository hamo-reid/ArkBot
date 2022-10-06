"""
本模块负责管理各类路径
"""

from pathlib import Path

# 包路径
PACKAGE_PATH = Path(__file__).parent.absolute().resolve()
# 工作路径
CWD_PATH = Path.cwd()
# 文件总路径
TOTAL_PATH = Path.cwd() / "arknights"

# 资源路径
ASSETS_PATH = TOTAL_PATH / "assets"
# 生成图片路径
PRODUCT_PATH = ASSETS_PATH / "product"
product_collection = {
    "mastery": PRODUCT_PATH / "mastery",
    "promotion": PRODUCT_PATH / "promotion",
}
# 素材路径
RESOURCE_PATH = ASSETS_PATH / "resource"
resource_collection = {
    "others": RESOURCE_PATH / "others",
    "professions": RESOURCE_PATH / "professions",
    "subProfessions": RESOURCE_PATH / "subProfessions",
    "background": RESOURCE_PATH / "background",
}

# 模板路径
TEMPLATE_PATH = PACKAGE_PATH / "html_render" / "template"

# 数据库总路径
DB_PATH = TOTAL_PATH / "db"
# 干员数据库路径
OPERATOR_DB_PATH = DB_PATH / "operator.db"
# 技能数据库路径
SKILL_DB_PATH = DB_PATH / "skill.db"
# 物品数据库路径
ITEM_DB_PATH = DB_PATH / "item.db"
# 其他数据库路径
OTHER_DB_PATH = DB_PATH / "other.db"
