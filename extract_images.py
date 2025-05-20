import os
import zipfile
import shutil
from pathlib import Path
from config import DOCX_FOLDER, IMAGE_OUTPUT_DIR

def extract_images_from_docx(docx_path, output_dir):
    """解析docx文件，提取图片到指定目录，返回图片路径列表"""
    docx_name = Path(docx_path).stem  # 原docx文件名（无后缀）
    temp_dir = Path(output_dir) / "temp"  # 临时解压目录
    temp_dir.mkdir(parents=True, exist_ok=True)

    try:
        # 解压docx到临时目录
        with zipfile.ZipFile(docx_path, 'r') as zf:
            zf.extractall(temp_dir)
    except zipfile.BadZipFile:
        print(f"错误：{docx_path} 不是有效的docx文件，跳过！")
        return []

    # 复制图片到正式存储目录（避免重名，用原docx名+序号命名）
    media_dir = temp_dir / "word" / "media"
    image_paths = []
    if media_dir.exists():
        for idx, img_file in enumerate(media_dir.iterdir(), 1):
            # 重命名图片（原docx名_序号.扩展名）
            new_img_name = f"{docx_name}_{idx}{img_file.suffix.lower()}"
            new_img_path = Path(output_dir) / new_img_name
            # 复制并确保文件名唯一（避免不同docx同名图片冲突）
            if new_img_path.exists():
                new_img_name = f"{docx_name}_{idx}_dup{img_file.suffix.lower()}"
                new_img_path = Path(output_dir) / new_img_name
            shutil.copy(img_file, new_img_path)
            image_paths.append(str(new_img_path))

    # 清理临时目录
    shutil.rmtree(temp_dir, ignore_errors=True)
    return image_paths

def batch_extract_images():
    """批量处理所有docx文件，返回图片信息列表"""
    Path(IMAGE_OUTPUT_DIR).mkdir(parents=True, exist_ok=True)  # 创建图片目录
    all_image_info = []

    for docx_file in Path(DOCX_FOLDER).glob("*.docx"):
        docx_path = str(docx_file)
        docx_name = docx_file.stem
        print(f"正在处理文件：{docx_name}")
        image_paths = extract_images_from_docx(docx_path, IMAGE_OUTPUT_DIR)
        for img_path in image_paths:
            all_image_info.append({
                "docx_name": docx_name,
                "image_path": img_path,  # 存储绝对路径（后续转为相对路径）
                "ocr_text": ""  # 后续填充OCR结果
            })
    return all_image_info

if __name__ == "__main__":
    # 测试：提取所有docx的图片
    images = batch_extract_images()
    print(f"共提取 {len(images)} 张图片")