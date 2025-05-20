# routes.py 修改后
from flask import Flask, jsonify, request
from flask_cors import CORS  # 新增导入
from database import search_ocr_data

app = Flask(__name__)
CORS(app)  # 启用CORS支持

@app.route('/search', methods=['GET'])
def search():
    keyword = request.args.get('q', '').strip()
    category = request.args.get('category', '').strip()  # 新增分类参数
    if not keyword:
        return jsonify([])
    try:
        results = search_ocr_data(keyword, category if category else None)
        return jsonify(results)
    except Exception as e:
        print(f"搜索出错: {e}")
        return jsonify([])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)