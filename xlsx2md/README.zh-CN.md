# xlsx2md — XLSX 转 Markdown

> 将 Excel (`.xlsx`) 文件转换为 Markdown 表格，支持提取嵌入图片并正确映射到单元格位置。

**语言 / Language:** [中文](README.zh-CN.md) | [English](README.md)

---

## 目录

- [安装](#安装)
- [使用](#使用)
- [输出示例](#输出示例)
- [图片处理](#图片处理)
- [边界情况](#边界情况)
- [运行测试](#运行测试)

---

## 安装

### 1. Python 版本要求

Python 3.7 或更高版本。

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

依赖包：

| 包 | 版本 | 用途 |
|----|------|------|
| `openpyxl` | ≥ 3.0.0 | 读取 XLSX 及嵌入图片 |
| `Pillow` | ≥ 9.0.0 | 图片格式统一为 PNG（可选） |

`Pillow` 为可选依赖：未安装时直接写入原始图片数据，安装后统一输出 PNG 格式。

---

## 使用

### 基本用法

```bash
python xlsx2md.py input.xlsx
```

将 `input.xlsx` 转换为同目录下的 `input.md`，图片保存到 `images/` 子目录。

### 完整参数

```
用法：
  python xlsx2md.py [-h] [-o OUTPUT] [-i IMAGE_DIR] [--no-images] [--sheet SHEET] input

位置参数：
  input                 输入 XLSX 文件路径

可选参数：
  -h, --help            显示帮助
  -o OUTPUT             输出 Markdown 文件路径
                        （默认：与输入同名，扩展名改为 .md）
  -i IMAGE_DIR          图片输出目录（默认：images）
  --no-images           忽略图片，只转换文本
  --sheet SHEET         只转换指定名称的 Sheet
```

### 参数示例

```bash
# 指定输出文件
python xlsx2md.py input.xlsx -o output/result.md

# 指定图片目录
python xlsx2md.py input.xlsx -i assets/images

# 只转换文本
python xlsx2md.py input.xlsx --no-images

# 只转换特定 Sheet
python xlsx2md.py input.xlsx --sheet 员工信息
python xlsx2md.py input.xlsx --sheet Sheet1

# 组合使用
python xlsx2md.py input.xlsx -o docs/output.md -i docs/images --sheet Summary
```

---

## 输出示例

给定一个包含姓名、头像图片和备注的 XLSX 文件：

```markdown
## 员工信息

| 姓名 | 头像 | 备注 |
| --- | --- | --- |
| 张三 | ![image](images/员工信息_img_0.png) | 经理 |
| 李四 | ![image](images/员工信息_img_1.png) | 工程师 |
```

对应的文件结构：

```
output/
├── output.md
└── images/
    ├── 员工信息_img_0.png   ← 张三的头像
    └── 员工信息_img_1.png   ← 李四的头像
```

---

## 图片处理

| 特性 | 说明 |
|------|------|
| 支持的锚定类型 | `TwoCellAnchor`、`OneCellAnchor`、`AbsoluteAnchor` |
| `TwoCellAnchor` / `OneCellAnchor` | 根据起始单元格坐标精确定位图片 |
| `AbsoluteAnchor` | 无法映射单元格，兜底放入首行首列 |
| 图片命名格式 | `{Sheet名}_img_{序号}.png` |
| 文字+图片同格 | 两者均保留，图片引用附在文字后 |
| 无图片的 XLSX | 正常转换文本表格，不报错 |

**关键修复说明：** openpyxl 加载工作簿时，`img.ref`（BytesIO）的游标不在起始位置。  
工具在读取前执行 `seek(0)` 确保图片数据完整读取，避免图片静默丢失。

---

## 边界情况

| 情况 | 处理方式 |
|------|----------|
| 空单元格 | 输出空字符串 |
| 合并单元格 | 非主单元格输出空字符串 |
| 单元格内换行 `\n` | 替换为 `<br>` |
| 单元格含竖线 `\|` | 自动转义为 `\\\|` |
| Sheet 名含特殊字符 | 自动替换为下划线并合并连续下划线 |
| 无任何 Sheet | 输出警告，写入空 Markdown |

---

## 运行测试

```bash
pip install pytest openpyxl Pillow
pytest tests/
```

测试覆盖以下场景：
- 锚点解析（三种类型）
- 单元格值转字符串（空值、换行、竖线、数字）
- Markdown 表格生成
- 图片引用插入（正确行列）
- `xlsx_to_markdown_string` 返回字符串
- 图片真实嵌入并保存到磁盘
- 多 Sheet 转换

---

## 项目结构

```
xlsx2md/
├── xlsx2md.py          # 主程序
├── requirements.txt    # 依赖列表
├── README.md           # English 文档
├── README.zh-CN.md     # 本文档（中文）
└── tests/
    └── test_xlsx2md.py # 单元测试
```
