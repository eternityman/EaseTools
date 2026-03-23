# xlsx2md — XLSX to Markdown

> Converts Excel (`.xlsx`) spreadsheets to Markdown tables, correctly mapping embedded images to their cells.

**Language / 语言:** [English](README.md) | [中文](README.zh-CN.md)

---

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Output Example](#output-example)
- [Image Handling](#image-handling)
- [Edge Cases](#edge-cases)
- [Run Tests](#run-tests)

---

## Installation

### 1. Python version

Python 3.7 or higher.

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

Dependencies:

| Package | Version | Purpose |
|---------|---------|---------|
| `openpyxl` | ≥ 3.0.0 | Read XLSX and embedded images |
| `Pillow` | ≥ 9.0.0 | Normalise images to PNG (optional) |

`Pillow` is optional: without it, raw image bytes are written; with it, all images are normalised to PNG.

---

## Usage

### Basic usage

```bash
python xlsx2md.py input.xlsx
```

Converts `input.xlsx` to `input.md` in the same directory; images saved to `images/`.

### All options

```
Usage:
  python xlsx2md.py [-h] [-o OUTPUT] [-i IMAGE_DIR] [--no-images] [--sheet SHEET] input

Positional:
  input                 Input XLSX file path

Optional:
  -h, --help            Show help
  -o OUTPUT             Output .md file path
                        (Default: same name, .md extension)
  -i IMAGE_DIR          Image output directory
                        (Default: images)
  --no-images           Skip images, text only
  --sheet SHEET         Convert only the named sheet
```

### Examples

```bash
# Specify output file
python xlsx2md.py input.xlsx -o output/result.md

# Specify image directory
python xlsx2md.py input.xlsx -i assets/images

# Text only
python xlsx2md.py input.xlsx --no-images

# Convert specific sheet
python xlsx2md.py input.xlsx --sheet Sheet1

# Combined
python xlsx2md.py input.xlsx -o docs/output.md -i docs/images --sheet Summary
```

---

## Output Example

Given an XLSX with name, avatar image, and notes columns:

```markdown
## 员工信息

| 姓名 | 头像 | 备注 |
| --- | --- | --- |
| 张三 | ![image](images/员工信息_img_0.png) | 经理 |
| 李四 | ![image](images/员工信息_img_1.png) | 工程师 |
```

Resulting file structure:

```
output/
├── output.md
└── images/
    ├── 员工信息_img_0.png
    └── 员工信息_img_1.png
```

---

## Image Handling

| Feature | Details |
|---------|---------|
| Supported anchor types | `TwoCellAnchor`, `OneCellAnchor`, `AbsoluteAnchor` |
| `TwoCellAnchor` / `OneCellAnchor` | Precisely mapped to start cell |
| `AbsoluteAnchor` | Cannot map to a cell; falls back to row 1 col 1 |
| Image naming | `{SheetName}_img_{index}.png` |
| Text + image in same cell | Both preserved; image ref appended after text |
| XLSX without images | Converts normally, no error |

**Key fix note:** openpyxl leaves the `img.ref` BytesIO cursor at a non-zero position after loading.  
The tool calls `seek(0)` before reading to ensure complete image data, preventing silent image loss.

---

## Edge Cases

| Situation | Handling |
|-----------|---------|
| Empty cell | Empty string |
| Merged cell | Non-master cells → empty string |
| Newline `\n` inside cell | Replaced with `<br>` |
| Cell contains `\|` | Auto-escaped to `\\\|` |
| Sheet name with special chars | Replaced with `_`, consecutive `_` collapsed |
| No sheets at all | Warning printed, empty Markdown written |

---

## Run Tests

```bash
pip install pytest openpyxl Pillow
pytest tests/
```

Tests cover:
- Anchor parsing (3 types)
- Cell value to string
- Markdown table generation
- Image ref insertion (correct row/col)
- `xlsx_to_markdown_string` returns string
- Real image embedding and disk save
- Multi-sheet conversion

---

## Project Structure

```
xlsx2md/
├── xlsx2md.py          # Main script
├── requirements.txt    # Dependencies
├── README.md           # This document (English)
├── README.zh-CN.md     # 中文文档
└── tests/
    └── test_xlsx2md.py # Unit tests
```
