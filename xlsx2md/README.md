# xlsx2md — XLSX 转 Markdown / XLSX to Markdown

> 将 Excel (`.xlsx`) 文件转换为 Markdown 表格，支持提取嵌入图片并正确映射到单元格位置。  
> Converts Excel (`.xlsx`) spreadsheets to Markdown tables, correctly mapping embedded images to their cells.

---

## 目录 / Table of Contents

- [安装 / Installation](#安装--installation)
- [使用 / Usage](#使用--usage)
- [输出示例 / Output Example](#输出示例--output-example)
- [图片处理 / Image Handling](#图片处理--image-handling)
- [边界情况 / Edge Cases](#边界情况--edge-cases)
- [运行测试 / Run Tests](#运行测试--run-tests)

---

## 安装 / Installation

### 1. Python 版本要求 / Python version

Python 3.7 或更高版本 / Python 3.7 or higher.

### 2. 安装依赖 / Install dependencies

```bash
pip install -r requirements.txt
```

依赖包 / Dependencies:

| 包 / Package | 版本 / Version | 用途 / Purpose |
|---|---|---|
| `openpyxl` | ≥ 3.0.0 | 读取 XLSX 及嵌入图片 / Read XLSX and embedded images |
| `Pillow` | ≥ 9.0.0 | 图片格式统一为 PNG（可选）/ Normalise images to PNG (optional) |

`Pillow` 为可选依赖：未安装时直接写入原始图片数据，安装后统一输出 PNG 格式。  
`Pillow` is optional: without it, raw image bytes are written; with it, all images are normalised to PNG.

---

## 使用 / Usage

### 基本用法 / Basic usage

```bash
python xlsx2md.py input.xlsx
```

将 `input.xlsx` 转换为同目录下的 `input.md`，图片保存到 `images/` 子目录。  
Converts `input.xlsx` to `input.md` in the same directory; images saved to `images/`.

### 完整参数 / All options

```
用法 / Usage:
  python xlsx2md.py [-h] [-o OUTPUT] [-i IMAGE_DIR] [--no-images] [--sheet SHEET] input

位置参数 / Positional:
  input                 输入 XLSX 文件路径 / Input XLSX file path

可选参数 / Optional:
  -h, --help            显示帮助 / Show help
  -o OUTPUT             输出 Markdown 文件路径 / Output .md file path
                        （默认：与输入同名，扩展名改为 .md / Default: same name, .md extension）
  -i IMAGE_DIR          图片输出目录 / Image output directory
                        （默认：images / Default: images）
  --no-images           忽略图片，只转换文本 / Skip images, text only
  --sheet SHEET         只转换指定名称的 Sheet / Convert only the named sheet
```

### 参数示例 / Examples

```bash
# 指定输出文件 / Specify output file
python xlsx2md.py input.xlsx -o output/result.md

# 指定图片目录 / Specify image directory
python xlsx2md.py input.xlsx -i assets/images

# 只转换文本 / Text only
python xlsx2md.py input.xlsx --no-images

# 只转换特定 Sheet / Convert specific sheet
python xlsx2md.py input.xlsx --sheet 员工信息
python xlsx2md.py input.xlsx --sheet Sheet1

# 组合使用 / Combined
python xlsx2md.py input.xlsx -o docs/output.md -i docs/images --sheet Summary
```

---

## 输出示例 / Output Example

给定一个包含姓名、头像图片和备注的 XLSX 文件：  
Given an XLSX with name, avatar image, and notes columns:

```markdown
## 员工信息

| 姓名 | 头像 | 备注 |
| --- | --- | --- |
| 张三 | ![image](images/员工信息_img_0.png) | 经理 |
| 李四 | ![image](images/员工信息_img_1.png) | 工程师 |
```

对应的文件结构 / Resulting file structure:

```
output/
├── output.md
└── images/
    ├── 员工信息_img_0.png   ← 张三的头像
    └── 员工信息_img_1.png   ← 李四的头像
```

---

## 图片处理 / Image Handling

| 特性 / Feature | 说明 / Details |
|---|---|
| 支持的锚定类型 | `TwoCellAnchor`、`OneCellAnchor`、`AbsoluteAnchor` |
| `TwoCellAnchor` / `OneCellAnchor` | 根据起始单元格坐标精确定位图片 / Precisely mapped to start cell |
| `AbsoluteAnchor` | 无法映射单元格，兜底放入首行首列 / Cannot map to a cell; falls back to row 1 col 1 |
| 图片命名格式 | `{Sheet名}_img_{序号}.png` |
| 文字+图片同格 | 两者均保留，图片引用附在文字后 / Both preserved; image ref appended after text |
| 无图片的 XLSX | 正常转换文本表格，不报错 / Converts normally, no error |

**关键修复说明：** openpyxl 加载工作簿时，`img.ref`（BytesIO）的游标不在起始位置。  
工具在读取前执行 `seek(0)` 确保图片数据完整读取，避免图片静默丢失。

**Key fix note:** openpyxl leaves the `img.ref` BytesIO cursor at a non-zero position after loading.  
The tool calls `seek(0)` before reading to ensure complete image data, preventing silent image loss.

---

## 边界情况 / Edge Cases

| 情况 / Situation | 处理方式 / Handling |
|---|---|
| 空单元格 | 输出空字符串 / Empty string |
| 合并单元格 | 非主单元格输出空字符串 / Non-master cells → empty string |
| 单元格内换行 `\n` | 替换为 `<br>` / Replaced with `<br>` |
| 单元格含竖线 `\|` | 自动转义为 `\\\|` / Auto-escaped to `\\\|` |
| Sheet 名含特殊字符 | 自动替换为下划线并合并连续下划线 / Replaced with `_`, consecutive `_` collapsed |
| 无任何 Sheet | 输出警告，写入空 Markdown / Warning printed, empty Markdown written |

---

## 运行测试 / Run Tests

```bash
pip install pytest openpyxl Pillow
pytest tests/
```

测试覆盖以下场景 / Tests cover:
- 锚点解析（三种类型）/ Anchor parsing (3 types)
- 单元格值转字符串（空值、换行、竖线、数字）/ Cell value to string
- Markdown 表格生成 / Markdown table generation
- 图片引用插入（正确行列）/ Image ref insertion (correct row/col)
- `xlsx_to_markdown_string` 返回字符串 / `xlsx_to_markdown_string` returns string
- 图片真实嵌入并保存到磁盘 / Real image embedding and disk save
- 多 Sheet 转换 / Multi-sheet conversion

---

## 项目结构 / Project Structure

```
xlsx2md/
├── xlsx2md.py          # 主程序 / Main script
├── requirements.txt    # 依赖列表 / Dependencies
├── README.md           # 本文档 / This document
└── tests/
    └── test_xlsx2md.py # 单元测试 / Unit tests
```
