#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
xlsx2md.py - 将 XLSX 文件转换为 Markdown 文件的命令行工具

支持功能：
- 多 Sheet 转换，每个 Sheet 作为二级标题
- 提取 XLSX 中嵌入的图片，保存到指定目录
- 将图片映射到 Markdown 表格中对应的单元格
- 处理合并单元格、空单元格、换行符等边界情况
"""

import argparse
import io
import os
import sys

import openpyxl
from openpyxl.drawing.spreadsheet_drawing import (
    AbsoluteAnchor,
    OneCellAnchor,
    TwoCellAnchor,
)

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False


def get_anchor_cell(anchor):
    """
    从锚点对象中提取单元格行列信息（均为 0-based 索引）。

    支持 TwoCellAnchor、OneCellAnchor、AbsoluteAnchor 三种类型。
    AbsoluteAnchor 无法映射到具体单元格，返回 None。

    :param anchor: openpyxl 锚点对象
    :return: (row, col) 元组（0-based），无法确定时返回 None
    """
    if anchor is None:
        return None
    if isinstance(anchor, TwoCellAnchor):
        # _from 是起始单元格
        return anchor._from.row, anchor._from.col
    if isinstance(anchor, OneCellAnchor):
        return anchor._from.row, anchor._from.col
    if isinstance(anchor, AbsoluteAnchor):
        # AbsoluteAnchor 以 EMU 为单位，无法直接映射到单元格
        return None
    return None


def extract_images(sheet, image_dir, sheet_name):
    """
    提取工作表中所有嵌入的图片，保存到 image_dir，并返回图片位置映射。

    :param sheet: openpyxl 工作表对象
    :param image_dir: 图片输出目录路径
    :param sheet_name: 当前 Sheet 名称，用于生成文件名
    :return: dict，键为 (row, col)（0-based），值为图片相对路径列表
    """
    image_map = {}  # { (row, col): [相对路径, ...] }

    drawings = getattr(sheet, '_images', [])
    if not drawings:
        return image_map

    os.makedirs(image_dir, exist_ok=True)

    # 生成合法文件名前缀（去除不能用于文件名的字符，合并连续下划线）
    safe_sheet = "".join(c if c.isalnum() or c in "-_" else "_" for c in sheet_name)
    safe_sheet = "_".join(part for part in safe_sheet.split("_") if part)

    for idx, img in enumerate(drawings):
        filename = f"{safe_sheet}_img_{idx}.png"
        filepath = os.path.join(image_dir, filename)

        # 将图片数据写入文件
        try:
            img_stream = img.ref  # BytesIO 或类似对象
            # openpyxl 加载时 BytesIO 游标不在起始位置，必须先 seek(0)
            if hasattr(img_stream, 'seek'):
                img_stream.seek(0)
            raw = img_stream.read() if hasattr(img_stream, 'read') else bytes(img_stream)

            if HAS_PIL:
                # 使用 Pillow 统一输出为 PNG 格式
                pil_img = Image.open(io.BytesIO(raw))
                pil_img.save(filepath, format="PNG")
            else:
                # 没有 Pillow 时直接写入原始数据
                with open(filepath, 'wb') as f:
                    f.write(raw)
        except Exception as e:
            print(f"警告：无法保存图片 {filename}：{e}", file=sys.stderr)
            continue

        # 获取锚点对应的单元格坐标
        cell_pos = get_anchor_cell(img.anchor)
        if cell_pos is not None:
            row, col = cell_pos
            image_map.setdefault((row, col), []).append(
                os.path.join(os.path.basename(image_dir), filename).replace("\\", "/")
            )
        else:
            # AbsoluteAnchor：无法定位，放入 (0, 0) 作为兜底
            image_map.setdefault((0, 0), []).append(
                os.path.join(os.path.basename(image_dir), filename).replace("\\", "/")
            )

    return image_map


def cell_value_to_str(cell):
    """
    将单元格值转换为字符串，处理 None 和换行符。

    :param cell: openpyxl Cell 对象
    :return: 处理后的字符串
    """
    value = cell.value
    if value is None:
        return ""
    text = str(value)
    # 将换行符替换为 HTML <br> 以兼容 Markdown 表格
    text = text.replace("\r\n", "<br>").replace("\r", "<br>").replace("\n", "<br>")
    # 转义 Markdown 表格中的竖线
    text = text.replace("|", "\\|")
    return text


def sheet_to_markdown(sheet, image_map, include_images=True):
    """
    将一个工作表转换为 Markdown 表格字符串。

    :param sheet: openpyxl 工作表对象
    :param image_map: 图片位置映射，由 extract_images 返回
    :param include_images: 是否在输出中包含图片引用
    :return: Markdown 表格字符串列表（每个元素为一行）
    """
    lines = []

    # 获取有效数据范围
    max_row = sheet.max_row or 0
    max_col = sheet.max_column or 0

    if max_row == 0 or max_col == 0:
        lines.append("*（此 Sheet 无数据）*")
        return lines

    # 读取所有单元格内容，构建二维列表（考虑合并单元格）
    # openpyxl 对合并单元格的非主单元格返回 None，这里统一处理为空字符串
    rows_data = []
    for row_idx in range(1, max_row + 1):
        row_cells = []
        for col_idx in range(1, max_col + 1):
            cell = sheet.cell(row=row_idx, column=col_idx)
            text = cell_value_to_str(cell)

            # 附加图片引用（行列均转为 0-based）
            if include_images:
                img_list = image_map.get((row_idx - 1, col_idx - 1), [])
                img_refs = " ".join(f"![image]({p})" for p in img_list)
                if img_refs:
                    text = f"{text} {img_refs}".strip() if text else img_refs

            row_cells.append(text)
        rows_data.append(row_cells)

    # 第一行作为表头
    header = rows_data[0]
    lines.append("| " + " | ".join(header) + " |")
    lines.append("| " + " | ".join("---" for _ in header) + " |")

    # 数据行
    for row in rows_data[1:]:
        lines.append("| " + " | ".join(row) + " |")

    return lines


def _build_md_sections(wb, abs_image_dir, image_dir, include_images, sheet_filter):
    """
    内部辅助：遍历工作簿中的 Sheet，生成 Markdown 段落列表。

    :param wb: openpyxl Workbook 对象
    :param abs_image_dir: 图片保存的绝对路径目录
    :param image_dir: 图片目录名（用于生成引用路径）
    :param include_images: 是否处理图片
    :param sheet_filter: 只处理指定名称的 Sheet（None 表示全部）
    :return: (list[str] md_sections, bool found_filter)
    """
    md_sections = []
    for sheet_name in wb.sheetnames:
        if sheet_filter and sheet_name != sheet_filter:
            continue

        sheet = wb[sheet_name]

        img_map = {}
        if include_images:
            img_map = extract_images(sheet, abs_image_dir, sheet_name)

        section_lines = [f"## {sheet_name}", ""]
        table_lines = sheet_to_markdown(sheet, img_map, include_images=include_images)
        section_lines.extend(table_lines)
        md_sections.append("\n".join(section_lines))

    return md_sections


def xlsx_to_markdown_string(
    input_path,
    image_dir="images",
    include_images=True,
    sheet_filter=None,
):
    """
    将 XLSX 文件转换为 Markdown 字符串（不写入文件）。

    图片仍会保存到 image_dir 目录（相对于 input_path 所在目录），
    Markdown 中的图片引用路径也相对于该目录。

    :param input_path: 输入 XLSX 文件路径
    :param image_dir: 图片输出目录（默认 images）
    :param include_images: 是否处理图片（默认 True）
    :param sheet_filter: 只转换指定名称的 Sheet（默认 None 表示全部）
    :return: Markdown 字符串
    :raises FileNotFoundError: 输入文件不存在时
    """
    if not os.path.isfile(input_path):
        raise FileNotFoundError(f"找不到输入文件 '{input_path}'")

    input_dir = os.path.dirname(os.path.abspath(input_path))
    abs_image_dir = os.path.join(input_dir, image_dir)

    wb = openpyxl.load_workbook(input_path, data_only=True)
    md_sections = _build_md_sections(wb, abs_image_dir, image_dir, include_images, sheet_filter)

    if not md_sections:
        return ""
    return "\n\n".join(md_sections) + "\n"


def xlsx_to_markdown(
    input_path,
    output_path=None,
    image_dir="images",
    include_images=True,
    sheet_filter=None,
):
    """
    将 XLSX 文件转换为 Markdown 文件。

    :param input_path: 输入 XLSX 文件路径
    :param output_path: 输出 Markdown 文件路径（默认与输入同名，扩展名 .md）
    :param image_dir: 图片输出目录（默认 images）
    :param include_images: 是否处理图片（默认 True）
    :param sheet_filter: 只转换指定名称的 Sheet（默认 None 表示全部）
    """
    if not os.path.isfile(input_path):
        print(f"错误：找不到输入文件 '{input_path}'", file=sys.stderr)
        sys.exit(1)

    # 默认输出路径与输入同目录，扩展名改为 .md
    if output_path is None:
        base = os.path.splitext(input_path)[0]
        output_path = base + ".md"

    # 图片目录相对于输出文件所在目录
    output_dir = os.path.dirname(os.path.abspath(output_path))
    abs_image_dir = os.path.join(output_dir, image_dir)

    wb = openpyxl.load_workbook(input_path, data_only=True)
    md_sections = _build_md_sections(wb, abs_image_dir, image_dir, include_images, sheet_filter)

    if not md_sections:
        if sheet_filter:
            print(f"警告：未找到名为 '{sheet_filter}' 的 Sheet。", file=sys.stderr)
        else:
            print("警告：工作簿中没有任何 Sheet。", file=sys.stderr)
        md_content = ""
    else:
        md_content = "\n\n".join(md_sections) + "\n"

    # 写入 Markdown 文件
    output_abs = os.path.abspath(output_path)
    output_parent = os.path.dirname(output_abs)
    if output_parent:
        os.makedirs(output_parent, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(md_content)

    print(f"转换完成：{output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="将 XLSX 文件转换为 Markdown 文件，支持提取嵌入图片。",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  python xlsx2md.py input.xlsx
  python xlsx2md.py input.xlsx -o output.md
  python xlsx2md.py input.xlsx -i assets/images
  python xlsx2md.py input.xlsx --no-images
  python xlsx2md.py input.xlsx --sheet Sheet1
""",
    )
    parser.add_argument("input", help="输入 XLSX 文件路径")
    parser.add_argument(
        "-o", "--output", default=None, help="输出 Markdown 文件路径（默认与输入同名，扩展名 .md）"
    )
    parser.add_argument(
        "-i", "--image-dir", default="images", help="图片输出目录（默认: images）"
    )
    parser.add_argument(
        "--no-images", action="store_true", help="忽略图片，只转换文本内容"
    )
    parser.add_argument(
        "--sheet", default=None, help="只转换指定名称的 Sheet"
    )

    args = parser.parse_args()

    xlsx_to_markdown(
        input_path=args.input,
        output_path=args.output,
        image_dir=args.image_dir,
        include_images=not args.no_images,
        sheet_filter=args.sheet,
    )


if __name__ == "__main__":
    main()
