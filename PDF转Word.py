import fitz  # PyMuPDF 库，用于处理 PDF 文件
from docx import Document
import os
import argparse
from tqdm import tqdm

def extract_text_from_pdf(pdf_path):
    """从 PDF 文件中提取文本内容"""
    text = ""
    try:
        with fitz.open(pdf_path) as pdf_document:
            # 使用 tqdm 显示进度条
            for page_num in tqdm(range(len(pdf_document)), desc=f"正在读取 {os.path.basename(pdf_path)}"):
                page = pdf_document[page_num]
                text += page.get_text()
    except Exception as e:
        print(f"错误：处理 PDF 文件时出错 - {str(e)}")
        return None
    return text

def create_word_document(text, output_path):
    """创建 Word 文档并写入提取的文本"""
    try:
        doc = Document()
        # 将文本按段落分割并添加到 Word 文档中
        paragraphs = text.split('\n\n')
        for paragraph in tqdm(paragraphs, desc="正在创建 Word 文档"):
            if paragraph.strip():  # 跳过空段落
                doc.add_paragraph(paragraph)
        
        doc.save(output_path)
        print(f"成功保存 Word 文档到: {output_path}")
        return True
    except Exception as e:
        print(f"错误：创建 Word 文档时出错 - {str(e)}")
        return False

def convert_pdf_to_word(pdf_path, output_path=None):
    """将 PDF 转换为 Word 文档的主函数"""
    # 如果未指定输出路径，使用与 PDF 相同的文件名，扩展名为 .docx
    if output_path is None:
        base_name = os.path.splitext(pdf_path)[0]
        output_path = f"{base_name}.docx"
    
    # 检查输入文件是否存在
    if not os.path.exists(pdf_path):
        print(f"错误：文件不存在 - {pdf_path}")
        return False
    
    # 检查输入文件是否为 PDF
    if not pdf_path.lower().endswith('.pdf'):
        print(f"错误：文件不是 PDF 格式 - {pdf_path}")
        return False
    
    # 提取 PDF 文本
    text = extract_text_from_pdf(pdf_path)
    if text is None:
        return False
    
    # 创建 Word 文档
    return create_word_document(text, output_path)

def main():
    """主函数，直接指定输入和输出路径并执行转换"""
    # 指定输入 PDF 文件路径
    input_pdf = r"test.pdf"
    # 指定输出 Word 文件路径
    output_word = r"test.docx"
    
    # 执行转换
    success = convert_pdf_to_word(input_pdf, output_word)
    
    # 根据转换结果设置退出码
    exit(0 if success else 1)

if __name__ == "__main__":
    main()
