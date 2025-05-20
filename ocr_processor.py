from PIL import Image, ImageEnhance
import pytesseract
import os
from config import BASE_DIR, TESSERACT_CMD  # 新增导入 BASE_DIR

# 配置Tesseract路径（Windows用户需设置）
if TESSERACT_CMD:
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD

def preprocess_image(image):
    """图片预处理（提高OCR准确率）"""
    image = image.convert("L")  # 转为灰度图
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(1.5)  # 增强对比度
    image = image.point(lambda x: 0 if x < 127 else 255, '1')  # 二值化
    return image

def ocr_image(relative_path):
    """对图片进行OCR识别，返回文本（使用绝对路径）"""
    try:
        # 替换为统一的反斜杠路径格式
        relative_path = relative_path.replace("/", "\\")
        absolute_path = os.path.join(BASE_DIR, relative_path)
        absolute_path = os.path.normpath(absolute_path)  # 规范化路径
        print(f"规范化后的绝对路径：{absolute_path}")  # 验证路径

        if not os.path.exists(absolute_path):
            print(f"错误：文件不存在！路径：{absolute_path}")
            return ""

        if not os.access(absolute_path, os.R_OK):
            print(f"错误：无读取权限！路径：{absolute_path}")
            return ""
        img = Image.open(absolute_path)
        img = preprocess_image(img)
        text = pytesseract.image_to_string(img, lang="chi_sim+eng")
        return text.strip()
    except Exception as e:
        print(f"OCR失败：{relative_path} - {e}")
        return ""
