import streamlit as st
import pandas as pd
import json
import os
import tempfile
from io import BytesIO

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
                st.warning(f"JSON文件包含非预期类型: {type(data).__name__}")
                return []
    except Exception as e:
        st.error(f"读取JSON文件失败: {e}")
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
                        st.warning(f"JSONL解析错误: {e}")
    except Exception as e:
        st.error(f"读取JSONL文件失败: {e}")
    return data

def read_csv_file(file_path):
    """读取CSV文件，返回解析后的对象列表"""
    try:
        df = pd.read_csv(file_path)
        return df.to_dict(orient='records')
    except Exception as e:
        st.error(f"读取CSV文件失败: {e}")
        return []

def read_excel_file(file_path):
    """读取Excel文件，返回解析后的对象列表"""
    try:
        df = pd.read_excel(file_path)
        return df.to_dict(orient='records')
    except Exception as e:
        st.error(f"读取Excel文件失败: {e}")
        return []

def convert_file(input_file, output_format, start_id, fields_to_extract, excel_column_names):
    """处理文件转换的主函数"""
    # 创建临时文件
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(input_file.name)[1]) as temp_file:
        temp_file.write(input_file.getvalue())
        temp_path = temp_file.name
    
    # 检测文件格式
    file_format = detect_file_format(temp_path)
    st.info(f"检测到文件格式: {file_format.upper()}")

    # 读取文件内容
    if file_format == 'json':
        records = read_json_file(temp_path)
    elif file_format == 'jsonl':
        records = read_jsonl_file(temp_path)
    elif file_format == 'csv':
        records = read_csv_file(temp_path)
    elif file_format == 'excel':
        records = read_excel_file(temp_path)
    else:
        st.error("不支持的文件格式")
        return None, None
    
    # 处理数据
    data = []
    for record in records:
        flat_record = flatten_json(record)
        if fields_to_extract:
            row = {field: flat_record.get(field, '') for field in fields_to_extract}
        else:
            row = flat_record
        data.append(row)
    
    # 创建 DataFrame
    if not data:
        st.warning("警告: 没有找到有效数据")
        df = pd.DataFrame(columns=fields_to_extract)
    else:
        df = pd.DataFrame(data)
        df['id'] = range(start_id, start_id + len(df))
        if 'id' in df.columns and df.columns[0] != 'id':
            cols = ['id'] + [col for col in df.columns if col != 'id']
            df = df[cols]
        
        # 只在用户提供了完整的列名列表时才重命名
        if excel_column_names and len(excel_column_names) == len(fields_to_extract) and all(excel_column_names):
            column_mapping = dict(zip(fields_to_extract, excel_column_names))
            df = df.rename(columns=column_mapping)
    
    # 生成输出文件名
    base_name = os.path.splitext(input_file.name)[0]
    output_ext = {'excel': '.xlsx', 'csv': '.csv', 'json': '.json', 'jsonl': '.jsonl'}[output_format]
    output_name = f"{base_name}_converted{output_ext}"
    
    # 根据输出格式生成不同的输出内容
    if output_format == "excel":
        output = BytesIO()
        df.to_excel(output, index=False)
        output.seek(0)
    elif output_format == "csv":
        # 修复CSV输出问题：添加index=False参数
        output = df.to_csv(sep=',', na_rep='nan', index=False).encode('utf-8-sig')
    elif output_format == "json":
        output = df.to_json(orient='records', force_ascii=False, indent=4).encode('utf-8')
    elif output_format == "jsonl":
        output = "\n".join([json.dumps(record, ensure_ascii=False) for record in data]).encode('utf-8')
    
    # 删除临时文件
    os.unlink(temp_path)
    
    return output, output_name

# 添加此辅助函数
def rerun_app():
    """兼容不同版本的 Streamlit 重新运行应用的函数"""
    if hasattr(st, 'rerun'):
        st.rerun()
    else:
        st.experimental_rerun()

def main():
    st.set_page_config(page_title="格式转换工具", layout="wide")
    st.title("格式转换工具 🛠️")
    st.markdown("author：mengxian")
    # 添加工具介绍
    st.markdown(
        """
        支持 **Excel、CSV、JSON、JSONL** 四种格式文件的相互转换，  
        内置 **JSON嵌套数据扁平化处理** 及 **字段筛选** 功能，  
        适用于数据清洗、迁移、集成等场景，帮助您快速处理多源异构数据。
        """,
        unsafe_allow_html=True
    )
    
    # 上传文件
    uploaded_file = st.file_uploader("选择文件", type=["json", "jsonl", "csv", "xls", "xlsx"])
    
    if uploaded_file:
        # 初始化会话状态
        if 'records' not in st.session_state:
            st.session_state.records = None
        if 'flat_records' not in st.session_state:
            st.session_state.flat_records = None
        if 'preview_df' not in st.session_state:
            st.session_state.preview_df = None
        
        # 只在首次上传或文件改变时读取数据
        if st.session_state.records is None:
            # 创建临时文件用于预览
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as temp_file:
                temp_file.write(uploaded_file.getvalue())
                temp_path = temp_file.name
            
            # 检测文件格式
            file_format = detect_file_format(temp_path)
            st.info(f"检测到文件格式: {file_format.upper()}")
            
            # 读取前10条记录用于预览
            if file_format == 'json':
                st.session_state.records = read_json_file(temp_path)[:10]
            elif file_format == 'jsonl':
                st.session_state.records = read_jsonl_file(temp_path)[:10]
            elif file_format == 'csv':
                st.session_state.records = read_csv_file(temp_path)[:10]
            elif file_format == 'excel':
                st.session_state.records = read_excel_file(temp_path)[:10]
            else:
                st.session_state.records = []
            
            # 删除临时文件
            os.unlink(temp_path)
            
            # 扁平化数据用于预览
            if st.session_state.records:
                st.session_state.flat_records = [flatten_json(record) for record in st.session_state.records]
                st.session_state.preview_df = pd.DataFrame(st.session_state.flat_records)
        
        # 设置左右两侧各占一半宽度
        col1, col2 = st.columns(2)
        
        # 左侧面板：配置参数
        with col1:
            st.subheader("配置参数")
            
            # 输出格式
            output_format = st.selectbox(
                "输出格式",
                ["csv", "excel", "json", "jsonl"],
                format_func=lambda x: x.upper()
            )
            
            # 起始ID
            start_id = st.number_input("起始ID", min_value=0, value=0, step=1)
            
            # 要提取的字段
            st.subheader("要提取的字段")
            # 初始化会话状态
            if 'fields_to_extract' not in st.session_state:
                st.session_state.fields_to_extract = []
            
            # 显示已选择的字段
            if st.session_state.fields_to_extract:
                st.write("已选择的字段:")
                cols_per_row = 4  # 每行显示4个字段
                num_rows = (len(st.session_state.fields_to_extract) + cols_per_row - 1) // cols_per_row
                for row in range(num_rows):
                    cols = st.columns(cols_per_row)
                    start_idx = row * cols_per_row
                    end_idx = min(start_idx + cols_per_row, len(st.session_state.fields_to_extract))
                    for i in range(start_idx, end_idx):
                        field = st.session_state.fields_to_extract[i]
                        with cols[i % cols_per_row]:
                            st.text_input(f"字段 {i+1}", value=field, key=f"field_{i}")
                            if st.button(f"删除", key=f"delete_{i}"):
                                st.session_state.fields_to_extract.pop(i)
                                rerun_app()
            
            # 提取全部字段和删除全部字段按钮
            if st.session_state.preview_df is not None:
                available_fields = list(set(st.session_state.preview_df.columns) - set(st.session_state.fields_to_extract))
                col_extract, col_delete = st.columns([1, 1])  # 两个按钮并排显示
                with col_extract:
                    if st.button("提取全部字段"):
                        st.session_state.fields_to_extract = list(st.session_state.preview_df.columns)
                        rerun_app()
                with col_delete:
                    if st.button("删除全部字段"):
                        st.session_state.fields_to_extract = []
                        rerun_app()
            
            # 可用字段区域 - 使用固定高度的容器
            st.subheader("可用字段（点击添加）")
            
            if st.session_state.preview_df is not None:
                available_fields = list(set(st.session_state.preview_df.columns) - set(st.session_state.fields_to_extract))
                if available_fields:
                    # 使用固定高度的容器并添加滚动条
                    with st.container():
                        # 每行显示4个字段按钮
                        cols_per_row = 4
                        num_rows = (len(available_fields) + cols_per_row - 1) // cols_per_row
                        
                        for row in range(num_rows):
                            cols = st.columns(cols_per_row)
                            start_idx = row * cols_per_row
                            end_idx = min(start_idx + cols_per_row, len(available_fields))
                            
                            for i in range(start_idx, end_idx):
                                field = available_fields[i]
                                col_idx = i % cols_per_row
                                
                                with cols[col_idx]:
                                    # 使用更紧凑的按钮样式
                                    if st.button(
                                        field, 
                                        key=f"field_btn_{i}",
                                        type="secondary",
                                        use_container_width=True
                                    ):
                                        if field not in st.session_state.fields_to_extract:
                                            st.session_state.fields_to_extract.append(field)
                                            rerun_app()
                                        else:
                                            st.warning(f"字段 '{field}' 已在提取列表中")
            else:
                st.write("无法读取文件内容，无法显示可用字段")
            
            # Excel列名
            st.subheader("Excel列名（可选）")
            st.markdown("""
            为提取的字段指定自定义列名（与字段列表一一对应）。
            - 若不设置，将保持原字段名
            - 设置后，输出文件将使用指定的列名
            """)
            
            # 初始化会话状态
            if 'excel_column_names' not in st.session_state:
                st.session_state.excel_column_names = []
            
            # 同步Excel列名数量与提取字段数量
            if len(st.session_state.excel_column_names) != len(st.session_state.fields_to_extract):
                st.session_state.excel_column_names = [""] * len(st.session_state.fields_to_extract)
            
            # 显示Excel列名输入框
            if st.session_state.fields_to_extract:
                cols_per_row = 4  # 每行显示4个列名输入框
                num_rows = (len(st.session_state.fields_to_extract) + cols_per_row - 1) // cols_per_row
                for row in range(num_rows):
                    cols = st.columns(cols_per_row)
                    start_idx = row * cols_per_row
                    end_idx = min(start_idx + cols_per_row, len(st.session_state.fields_to_extract))
                    for i in range(start_idx, end_idx):
                        field = st.session_state.fields_to_extract[i]
                        with cols[i % cols_per_row]:
                            value = st.text_input(f"列名 {i+1}（对应字段: {field}）", 
                                                  value=st.session_state.excel_column_names[i], 
                                                  key=f"col_name_{i}")
                            st.session_state.excel_column_names[i] = value
        
        # 右侧面板：预览和结果
        with col2:
            st.subheader("数据预览")
            
            # 预览数据
            if st.session_state.preview_df is not None:
                # 显示数据预览，使用固定高度
                st.write(f"数据预览（前{len(st.session_state.records)}条记录）:")
                st.dataframe(st.session_state.preview_df, height=300)
            
            # 转换按钮 - 放在数据预览表下方，宽度更大
            convert_button = st.button("开始转换", key="convert_button", use_container_width=True)
            
            # 处理转换结果
            if convert_button:
                # 检查是否所有必填字段都已设置
                if not st.session_state.fields_to_extract:
                    st.error("请至少选择一个要提取的字段")
                    return
                
                with st.spinner("正在处理..."):
                    output, output_name = convert_file(
                        uploaded_file, 
                        output_format, 
                        start_id, 
                        st.session_state.fields_to_extract, 
                        st.session_state.excel_column_names
                    )
                
                if output is not None:
                    st.subheader("转换完成")
                    
                    # 根据输出格式设置MIME类型
                    mime_types = {
                        'excel': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                        'csv': 'text/csv',
                        'json': 'application/json',
                        'jsonl': 'application/jsonl'
                    }
                    
                    # 提供下载链接
                    st.download_button(
                        label="下载转换后的文件",
                        data=output,
                        file_name=output_name,
                        mime=mime_types[output_format]
                    )
                    
                    # 预览转换后的数据
                    st.write("转换后数据预览:")
                    if output_format == 'json' or output_format == 'jsonl':
                        try:
                            if output_format == 'json':
                                preview_data = json.loads(output.decode('utf-8'))
                            else:  # jsonl
                                preview_data = [json.loads(line) for line in output.decode('utf-8').split('\n') if line]
                            st.json(preview_data[:10])
                        except:
                            st.write("无法预览JSON数据")
                    else:
                        try:
                            if output_format == 'excel':
                                preview_df = pd.read_excel(output)
                            else:  # csv
                                preview_df = pd.read_csv(BytesIO(output))
                            st.dataframe(preview_df.head(10), height=300)
                        except:
                            st.write("无法预览数据")

if __name__ == "__main__":
    main()
