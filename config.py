# 项目根路径（自动获取当前目录）
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# docx文件存放目录（需提前创建并放入docx文件）
DOCX_FOLDER = os.path.join(BASE_DIR, "docx_files")

# 提取的图片存储目录（自动创建）
IMAGE_OUTPUT_DIR = os.path.join(BASE_DIR, "static", "images")

# 数据库路径（SQLite）
DATABASE_PATH = os.path.join(BASE_DIR, "image_ocr.db")

# Tesseract路径（Windows用户需修改，其他系统留空）
TESSERACT_CMD = r'D:\tesseract-ocr\tesseract.exe'

# 分类映射配置
CATEGORY_MAPPING = {
    # first.html 分类
    "自然停顿": ["边界-停顿-自然停顿"],
    "对称停顿": ["边界-停顿-对称停顿"],
    "情绪停顿": ["边界-停顿-情绪停顿"],
    "非自然停顿": ["边界-停顿-非自然停顿"],
    "非对称停顿": ["边界-停顿-非对称停顿"],
    "非情绪停顿": ["边界-停顿-非情绪停顿"],
    "口语型终止": ["边界-终止-口语型终止"],
    "书面型终止": ["边界-终止-书面型终止"],
    # second.html 分类
    "回归初始话题": ["插入-竞争性插入-回归初始话题"],
    "初始话题与插入话题共存": ["插入-竞争性插入-初始话题与插入话题共存"],
    "抛弃初始话题，继续插入话题": ["插入-竞争性插入-抛弃初始话题，继续插入话题"],
    "弱意义": ["插入-支持-弱"],
    "强意义": ["插入-支持-强"],
    # third.html 分类
    "补充": ["引用-引用自身话语-补充"],
    "修正": ["引用-引用自身话语-修正"],
    "针对性回应": ["引用-引用他人话语-针对性回应"]
}