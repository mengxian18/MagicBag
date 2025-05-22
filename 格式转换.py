import json
import os
import pandas as pd

# 配置部分 - 可直接修改以下参数
INPUT_FILE = r"xsga45.xlsx"  # 输入文件路径，支持JSON、JSONL、CSV或Excel
OUTPUT_FILE = r"xsga46"  # 输出文件路径（不带扩展名）即输出文件命名
OUTPUT_FORMAT = "jsonl"  # 输出文件格式，支持 "excel"、"csv"、"json" 或 "jsonl"
start_id = 0  # id自增起始值
# json嵌套字段格式为：字段名_id_子字段名，比如，"qa": [{"question":"问题1", "answer": "答案1"}, {"question": "问题2", "answer": "答案2"}]字段格式：qa_0_question,qa_0_answer,qa_1_question,qa_1_answer
# 要提取的字段列表（为空时提取所有字段）
# 嵌套字段格式为：字段名_id_子字段名
FIELDS_TO_EXTRACT = [
    #  "id",
    #   "name",
    #   "qa_0_question",
    #   "qa_1_question",
    #   "qa_2_question",
    #  "case"
]

# 可选：为 Excel 或 JSON 列指定自定义名称（与字段列表一一对应）
EXCEL_COLUMN_NAMES = [
    #  "id",
    #  "question1",
    #  "question2",
    #  "question3"
    # "case"
]

def flatten_json(nested_json, parent_key='', sep='_'):
    """
    递归展开嵌套 JSON，将其转换为平面结构。
    :param nested_json: 嵌套的 JSON 对象
    :param parent_key: 父键名，用于递归时拼接
    :param sep: 键名分隔符
    :return: 平面化后的字典
    """
    items = []
    for key, value in nested_json.items():
        new_key = f"{parent_key}{sep}{key}" if parent_key else key
        if isinstance(value, dict):
            items.extend(flatten_json(value, new_key, sep=sep).items())
        elif isinstance(value, list):
            for i, item in enumerate(value):
                if isinstance(item, (dict, list)):
                    items.extend(flatten_json(item, f"{new_key}_{i}", sep=sep).items())
                else:
                    items.append((f"{new_key}_{i}", item))
        else:
            items.append((new_key, value))
    return dict(items)

def detect_file_format(file_path):
    """检测文件格式是JSON、JSONL、CSV还是Excel"""
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.json':
        return 'json'
    elif ext == '.jsonl':
        return 'jsonl'
    elif ext == '.csv':
        return 'csv'
    elif ext in ['.xls', '.xlsx']:
        return 'excel'
    return None

def read_json_file(file_path):
    """读取JSON文件，返回解析后的对象列表"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, dict):
                return [data]
            elif isinstance(data, list):
                return data
            else:
                print(f"警告: JSON文件包含非预期类型: {type(data).__name__}")
                return []
    except Exception as e:
        print(f"读取JSON文件失败: {e}")
        return []

def read_jsonl_file(file_path):
    """读取JSONL文件，返回解析后的对象列表"""
    data = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    try:
                        data.append(json.loads(line.strip()))
                    except json.JSONDecodeError as e:
                        print(f"JSONL解析错误: {e}")
    except Exception as e:
        print(f"读取JSONL文件失败: {e}")
    return data

def read_csv_file(file_path):
    """读取CSV文件，返回解析后的对象列表"""
    try:
        df = pd.read_csv(file_path)
        return df.to_dict(orient='records')
    except Exception as e:
        print(f"读取CSV文件失败: {e}")
        return []

def read_excel_file(file_path):
    """读取Excel文件，返回解析后的对象列表"""
    try:
        df = pd.read_excel(file_path)
        return df.to_dict(orient='records')
    except Exception as e:
        print(f"读取Excel文件失败: {e}")
        return []

def main():
    # 检测文件格式
    file_format = detect_file_format(INPUT_FILE)
    print(f"检测到文件格式: {file_format.upper()}")

    # 读取文件内容
    if file_format == 'json':
        records = read_json_file(INPUT_FILE)
    elif file_format == 'jsonl':
        records = read_jsonl_file(INPUT_FILE)
    elif file_format == 'csv':
        records = read_csv_file(INPUT_FILE)
    elif file_format == 'excel':
        records = read_excel_file(INPUT_FILE)
    else:
        print("不支持的文件格式")
        return
    
    # 处理数据
    data = []
    for record in records:
        flat_record = flatten_json(record)
        if FIELDS_TO_EXTRACT:
            row = {field: flat_record.get(field, '') for field in FIELDS_TO_EXTRACT}
        else:
            row = flat_record
        data.append(row)
    
    # 创建 DataFrame
    if not data:
        print("警告: 没有找到有效数据")
        df = pd.DataFrame(columns=EXCEL_COLUMN_NAMES or FIELDS_TO_EXTRACT)
    else:
        df = pd.DataFrame(data)
        df['id'] = range(start_id, start_id + len(df))
        if 'id' in df.columns and df.columns[0] != 'id':
            cols = ['id'] + [col for col in df.columns if col != 'id']
            df = df[cols]
        if EXCEL_COLUMN_NAMES and len(EXCEL_COLUMN_NAMES) == len(FIELDS_TO_EXTRACT):
            column_mapping = dict(zip(FIELDS_TO_EXTRACT, EXCEL_COLUMN_NAMES))
            df = df.rename(columns=column_mapping)
    
    # 保存为指定格式
    if OUTPUT_FORMAT.lower() == "excel":
        output_path = f"{OUTPUT_FILE}.xlsx"
        df.to_excel(output_path, index=False)
        print(f"成功转换 {len(data)} 条记录到 {output_path}")
    elif OUTPUT_FORMAT.lower() == "csv":
        output_path = f"{OUTPUT_FILE}.csv"
        df.to_csv(output_path, index=False, encoding='utf-8-sig')
        print(f"成功转换 {len(data)} 条记录到 {output_path}")
    elif OUTPUT_FORMAT.lower() == "json":
        output_path = f"{OUTPUT_FILE}.json"
        df.to_json(output_path, orient='records', force_ascii=False, indent=4)
        print(f"成功转换 {len(data)} 条记录到 {output_path}")
    elif OUTPUT_FORMAT.lower() == "jsonl":
        output_path = f"{OUTPUT_FILE}.jsonl"
        with open(output_path, 'w', encoding='utf-8') as f:
            for record in data:
                f.write(json.dumps(record, ensure_ascii=False) + '\n')
        print(f"成功转换 {len(data)} 条记录到 {output_path}")
    else:
        print("不支持的输出格式")

if __name__ == "__main__":
    main()
