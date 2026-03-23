# EaseTools

> 记录我的日常小工具

**语言 / Language:** [中文](README.zh-CN.md) | [English](README.md)

---

## 工具列表

### xlsx2md — Excel 转 Markdown

将 Excel (`.xlsx`) 电子表格转换为 Markdown 表格，支持提取嵌入图片。

---

## 安装与使用

### 一、命令行工具

#### 1. 安装依赖

```bash
pip install openpyxl Pillow
```

#### 2. 基本用法

```bash
# 将 input.xlsx 转换为 input.md
python xlsx2md/xlsx2md.py input.xlsx

# 指定输出文件
python xlsx2md/xlsx2md.py input.xlsx -o output.md

# 指定图片目录
python xlsx2md/xlsx2md.py input.xlsx -i assets/images

# 只转换文本，不提取图片
python xlsx2md/xlsx2md.py input.xlsx --no-images

# 只转换名为 "Sheet1" 的 Sheet
python xlsx2md/xlsx2md.py input.xlsx --sheet Sheet1
```

详细说明见 [`xlsx2md/README.zh-CN.md`](xlsx2md/README.zh-CN.md)。

---

### 二、VS Code 插件

让 Copilot Chat 通过 `@xlsx2md` 指令直接将 XLSX 文件转换为 Markdown。

#### 快速开始

1. 安装 Python 依赖：
   ```bash
   pip install openpyxl Pillow
   ```

2. 用 VS Code 打开 `vscode-xlsx2md` 文件夹，按 `F5` 启动（开发者模式）。

3. 在资源管理器中右键任意 `.xlsx` 文件，选择 **Convert XLSX to Markdown**。

4. 或在 Copilot Chat 中输入：
   ```
   @xlsx2md #yourfile.xlsx
   ```

完整安装和使用说明：[`vscode-xlsx2md/README.zh-CN.md`](vscode-xlsx2md/README.zh-CN.md)

---

### 三、MCP 服务器（让 Copilot 自动使用）

注册后，Copilot 在任何对话中只要你提到 XLSX 文件就会自动调用转换工具——无需 `@xlsx2md`。

#### 快速开始

1. 安装依赖：
   ```bash
   pip install -r mcp-xlsx2md/requirements.txt
   ```

2. 将示例配置复制为工作区 MCP 配置：
   ```bash
   cp mcp-xlsx2md/mcp.json.example .vscode/mcp.json
   ```

3. 重载 VS Code（`Ctrl+Shift+P` → `Developer: Reload Window`）。

4. 在 Copilot Chat 中直接说：
   ```
   请把 data.xlsx 转成 Markdown
   ```

完整安装和使用说明：[`mcp-xlsx2md/README.zh-CN.md`](mcp-xlsx2md/README.zh-CN.md)

---

## 运行测试

```bash
pip install pytest openpyxl Pillow
pytest xlsx2md/tests/
```
