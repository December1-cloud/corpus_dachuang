import sqlite3
from config import DATABASE_PATH, CATEGORY_MAPPING

def search_ocr_data(keyword, category=None):
    """根据关键词搜索OCR文本，返回匹配结果"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    base_query = '''
        SELECT docx_name, image_path, ocr_text, category 
        FROM ocr_data 
        WHERE ocr_text LIKE ?
    '''
    params = [f"%{keyword}%"]

    if category:
        allowed_docs = CATEGORY_MAPPING.get(category, [])
        if allowed_docs:
            placeholders = ','.join(['?'] * len(allowed_docs))
            base_query += f" AND docx_name IN ({placeholders})"
            params.extend(allowed_docs)

    cursor.execute(base_query, params)
    results = cursor.fetchall()
    conn.close()

    # 转换为字典列表
    return [
        {
            "docx_name": row[0],
            "image_path": row[1].replace("\\", "/"),
            "ocr_text": row[2],
            "category": row[3]
        } for row in results
    ]