import sqlite3
import sys
import os

# 获取当前脚本所在目录（scripts目录）
current_script_dir = os.path.dirname(os.path.abspath(__file__))

# 获取项目根目录（向上取一级目录，即 corpus-back）
project_root = os.path.dirname(current_script_dir)

# 将项目根目录添加到Python搜索路径
sys.path.append(project_root)

# 现在可以正常导入config模块
from config import DATABASE_PATH, CATEGORY_MAPPING
from extract_images import batch_extract_images
from ocr_processor import ocr_image

def init_database():
    """创建数据库表"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ocr_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            docx_name TEXT NOT NULL,       -- 原docx文件名
            image_path TEXT NOT NULL,     -- 图片相对路径（static/images/xxx.png）
            ocr_text TEXT NOT NULL,        -- OCR识别文本
            category TEXT NOT NULL  -- 新增分类字段
        )
    ''')
    conn.commit()
    conn.close()

def insert_ocr_data():
    """提取图片、OCR识别并插入数据库"""
    # 提取所有图片信息（含绝对路径）
    all_image_info = batch_extract_images()
    if not all_image_info:
        print("无图片数据，跳过插入数据库")
        return

    # 转换为相对路径（统一为正斜杠）
    for item in all_image_info:
        # 1. 生成相对路径（以项目根目录为基准，而非数据库目录）
        # 假设 DATABASE_PATH 是 "D:\王雅萱\corpus-back\image_ocr.db"，则 BASE_DIR 是 "D:\王雅萱\corpus-back"
        from config import BASE_DIR  # 从 config.py 导入项目根目录（关键！）
        item["image_path"] = os.path.relpath(
            item["image_path"],  # 图片的绝对路径（如 "D:\王雅萱\corpus-back\static\images\file.png"）
            start=BASE_DIR       # 基准目录为项目根目录（如 "D:\王雅萱\corpus-back"）
        )
        # 2. 关键修改：将反斜杠替换为正斜杠（Windows系统必须）
        item["image_path"] = item["image_path"].replace("\\", "/")

        # 3. 验证OCR能否通过相对路径找到图片（可选，但建议添加）
        test_path = os.path.join(BASE_DIR, item["image_path"])  # 拼接绝对路径
        if not os.path.exists(test_path):
            print(f"警告：图片路径不存在！绝对路径：{test_path}")

        # 执行OCR识别（使用相对路径或绝对路径，根据实际情况选择）
        # 若相对路径无法找到图片，建议直接使用绝对路径（更可靠）
        # item["ocr_text"] = ocr_image(test_path)  # 替换为绝对路径
        item["ocr_text"] = ocr_image(item["image_path"])

        # 根据 docx_name 查找对应的分类
        category = "未分类"
        for cat, doc_list in CATEGORY_MAPPING.items():
            if item["docx_name"] in doc_list:
                category = cat
                break
        item["category"] = category

    # 插入数据库（此时 image_path 已统一为正斜杠）
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    for item in all_image_info:
        cursor.execute('''
            INSERT INTO ocr_data (docx_name, image_path, ocr_text, category)
            VALUES (?, ?, ?, ?)
        ''', (item["docx_name"], item["image_path"], item["ocr_text"], item["category"]))
    conn.commit()
    conn.close()
    print(f"成功插入 {len(all_image_info)} 条数据到数据库")

if __name__ == "__main__":
    init_database()
    insert_ocr_data()
    print(f"项目根目录：{project_root}")  # 应输出 D:\王雅萱\corpus-back