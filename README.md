# 多功能的数据格式转换工具
支持多种文件格式的相互转换、嵌套数据扁平化处理及字段筛选，适用于数据清洗、迁移、集成等场景。
## 一、核心功能
### 1. 多格式文件读写支持
类型	支持格式
输入格式	JSON、JSONL、CSV、Excel（XLS/XLSX）
输出格式	JSON、JSONL、CSV、Excel（XLSX）
### 2. 嵌套数据扁平化处理
通过 flatten_json 函数递归展开嵌套 JSON 结构，将多层级数据转换为平面表格形式。
示例：{"qa": [{"question": "Q1"}, {"answer": "A1"}]} → 转换为 qa_0_question、qa_1_answer 等字段。
### 3. 字段筛选与自定义命名
字段提取：通过 FIELDS_TO_EXTRACT 指定需提取的字段（支持嵌套字段路径，如 qa_0_question）。
列名重命名：通过 EXCEL_COLUMN_NAMES 为输出文件自定义列名（需与提取字段一一对应）。
### 4. 自动生成 ID 字段
为每条记录添加自增 id 字段，起始值可通过 start_id 配置，便于数据索引和追踪。
## 二、典型应用场景
### 1. 数据清洗与预处理
场景：将 API 返回的嵌套 JSON 数据、日志 JSONL 文件或 Excel 表格转换为统一格式（如 CSV），去除冗余字段，便于后续分析。
优势：快速扁平化复杂结构，简化数据层级。
### 2. 跨系统数据迁移
场景：在数据库、数据分析工具（如 Power BI）或业务系统间迁移数据时，自动转换文件格式（例如将 Excel 转为 JSONL 导入数据仓库）。
### 3. 数据集成与 ETL 流程
场景：作为 ETL（提取 - 转换 - 加载）的中间环节，批量处理多源数据（如 JSON、CSV），统一格式后加载至目标系统。
### 4. 数据分析与建模准备
场景：将嵌套 JSON 数据展开为二维表格，利用 Pandas 或 SQL 进行统计分析、特征工程等操作。
## 三、使用示例
### 1. Excel 转 JSONL（基础转换）
INPUT_FILE = "data.xlsx"        # 输入Excel文件  
OUTPUT_FILE = "output"         # 输出文件名为"output.jsonl"  
OUTPUT_FORMAT = "jsonl"        # 目标格式为JSONL  
### 2. 提取指定字段并重命名
FIELDS_TO_EXTRACT = ["id", "name", "qa_0_question"]  # 提取原始字段  
EXCEL_COLUMN_NAMES = ["用户ID", "姓名", "问题1"]       # 自定义输出列名  
### 3. 嵌套 JSON 数据扁平化示例
输入数据：
json
{  
  "id": 1,  
  "user": {  
    "name": "Alice",  
    "qa": [{"question": "Q1", "answer": "A1"}]  
  }  
}  

输出字段（CSV 格式）：
id	user_name	user_qa_0_question	user_qa_0_answer
1	Alice	Q1	A1
## 四、优势与特点
### 1.灵活性高：通过修改配置参数（如文件路径、格式、字段列表）即可适应不同需求，无需修改代码逻辑。
### 2.鲁棒性强：内置文件读取错误处理机制（如 JSON 解析异常、格式不匹配），确保程序稳定运行。
### 3.可扩展性佳：支持通过修改 flatten_json 函数或新增格式解析器扩展功能（如支持 XML 格式）。
## 五、适用人群
### 1.数据分析师：处理多源数据，快速转换格式以适配分析工具。
### 2.开发人员：在 API 接口数据处理、ETL 流程中集成数据转换逻辑。
### 3.业务人员：通过简单配置完成 Excel 与 JSON 等格式的互转，无需编程基础。
如需进一步调整或扩展功能，可直接修改脚本中的配置参数或添加自定义逻辑。
