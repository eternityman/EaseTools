# xlsx2md — XLSX 转 Markdown 工具

将 Excel（`.xlsx`）文件转换为 Markdown 格式，支持**提取嵌入图片**并在 Markdown 表格中正确定位。

---

## 安装

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

依赖库：
- `openpyxl` ≥ 3.0.0 — 读取 XLSX 文件及其嵌入图片
- `Pillow` ≥ 9.0.0 — 图片格式处理（可选，不安装时直接写入原始数据）

### 2. Python 版本要求

Python 3.7+

---

## 使用方法

### 基本用法

```bash
python xlsx2md.py input.xlsx
```

将 `input.xlsx` 转换为 `input.md`，图片保存到 `images/` 目录。

### 完整参数

```
usage: xlsx2md.py [-h] [-o OUTPUT] [-i IMAGE_DIR] [--no-images] [--sheet SHEET] input

positional arguments:
  input                 输入 XLSX 文件路径

optional arguments:
  -h, --help            显示帮助信息
  -o OUTPUT, --output OUTPUT
                        输出 Markdown 文件路径（默认与输入文件同名，扩展名改为 .md）
  -i IMAGE_DIR, --image-dir IMAGE_DIR
                        图片输出目录（默认: images）
  --no-images           忽略图片，只转换文本内容
  --sheet SHEET         只转换指定名称的 Sheet
```

### 参数示例

```bash
# 指定输出文件
python xlsx2md.py input.xlsx -o output/result.md

# 指定图片目录
python xlsx2md.py input.xlsx -i assets/images

# 不提取图片，只转换文本
python xlsx2md.py input.xlsx --no-images

# 只转换名为 "员工信息" 的 Sheet
python xlsx2md.py input.xlsx --sheet 员工信息
```

---

## 输出示例

给定包含姓名、头像图片、备注的 XLSX 文件：

```markdown
## Sheet1

| 姓名 | 头像 | 备注 |
|------|------|------|
| 张三 | ![image](images/Sheet1_img_0.png) | 经理 |
| 李四 | ![image](images/Sheet1_img_1.png) | 工程师 |
```

图片文件保存在：

```
images/
├── Sheet1_img_0.png
└── Sheet1_img_1.png
```

---

## 图片处理说明

- 支持三种锚定方式：`TwoCellAnchor`、`OneCellAnchor`、`AbsoluteAnchor`
- `TwoCellAnchor` / `OneCellAnchor`：根据起始单元格坐标精确定位
- `AbsoluteAnchor`：无法映射到单元格，图片放置在首行首列
- 图片命名格式：`{Sheet名}_img_{序号}.png`
- 若单元格同时有文字和图片，两者均会保留

---

## 项目结构

```
xlsx2md/
├── xlsx2md.py          # 主程序
├── requirements.txt    # 依赖列表
├── README.md           # 本文档
└── tests/
    └── test_xlsx2md.py # 单元测试
```

---

## 运行测试

```bash
pip install pytest openpyxl Pillow
pytest tests/
```

---

## 边界情况处理

| 情况 | 处理方式 |
|------|---------|
| 空单元格 | 输出空字符串 |
| 合并单元格 | 不报错，非主单元格输出空字符串 |
| 单元格内换行 | 替换为 `<br>` |
| 没有图片的 XLSX | 正常转换表格文本 |
| 单元格含竖线 `\|` | 自动转义为 `\\\|` |
