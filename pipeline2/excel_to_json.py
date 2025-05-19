import pandas as pd
import json
from datetime import datetime
import os

def excel_to_json(excel_file):
    # 读取Excel文件，跳过第一行（表头）
    df = pd.read_excel(excel_file, dtype=str)
    
    # 确保输出目录存在
    output_dir = 'timu'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 遍历每一行数据
    for index, row in df.iterrows():
        try:
            # 创建数据字典
            data = {
                "序号": row['序号'].strip() if pd.notna(row['序号']) else "",
                "题干": row['题干'].strip() if pd.notna(row['题干']) else "",
                "提问": row['提问'].strip() if pd.notna(row['提问']) else "",
                "最终答案": row['最终答案'].strip() if pd.notna(row['最终答案']) else ""
            }
            print(data)
            # 生成文件名：序号_时间戳.json
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{data['序号']}_{timestamp}.json"
            filepath = os.path.join(output_dir, filename)
            # 写入JSON文件
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print(f"已生成文件: {filename}")

        except Exception as e:
            print(f"处理第 {index + 2} 行时出错: {str(e)}")
            # print(f"行数据: {row.to_dict()}")
            continue

if __name__ == "__main__":
    excel_file = r".\500案例题.xlsx"  # 修改为你的实际文件路径
    try:
        excel_to_json(excel_file)
        print("所有文件处理完成！")
    except Exception as e:
        print(f"处理过程中出现错误: {str(e)}") 
