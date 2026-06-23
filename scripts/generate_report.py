import sys
import os
import json
import webbrowser

def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_report.py <path_to_json>")
        sys.exit(1)

    json_path = os.path.abspath(sys.argv[1])
    if not os.path.exists(json_path):
        print(f"Error: File not found {json_path}")
        sys.exit(1)

    # 读取 JSON 数据
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 使用 Python 进行计算以保证准确性
    for row in data:
        # 计算金额 = 价格 * 数量
        row['amount'] = row['price'] * row['quantity']
        # 计算成本：仅“买”单收费，每张 1.7 元
        is_buy = '买' in row['type']
        row['cost'] = row['quantity'] * 1.7 if is_buy else 0.0

    # 加载 HTML 模板
    skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    template_path = os.path.join(skill_dir, 'assets', 'template.html')
    with open(template_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # 将数据注入到模板中
    json_str = json.dumps(data, ensure_ascii=False)
    html_content = html_content.replace('INJECT_JSON_DATA_HERE', json_str)

    # 将生成的 HTML 报告保存在 raw_data.json 同一目录下
    output_dir = os.path.dirname(json_path)
    report_path = os.path.join(output_dir, 'report.html')
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"报告生成成功: {report_path}")
    
    # 自动在浏览器中打开
    webbrowser.open(f"file://{report_path}")

if __name__ == '__main__':
    main()
