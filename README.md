# EaseTools

> Record My Easy Tools / 记录我的日常小工具

---

## 工具列表 / Tools

### xlsx2md — Excel 转 Markdown / Excel to Markdown Converter

将 Excel (`.xlsx`) 电子表格转换为 Markdown 表格，支持提取嵌入图片。  
Converts Excel (`.xlsx`) spreadsheets to Markdown tables with embedded image support.

---

## 安装与使用 / Installation & Usage

### 一、命令行工具 / CLI Tool

#### 1. 安装依赖 / Install dependencies

```bash
pip install openpyxl Pillow
```

#### 2. 基本用法 / Basic usage

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

详细说明见 [`xlsx2md/README.md`](xlsx2md/README.md)。  
Full documentation: [`xlsx2md/README.md`](xlsx2md/README.md).

---

### 二、VS Code 插件 / VS Code Extension

让 Copilot Chat 通过 `@xlsx2md` 指令直接将 XLSX 文件转换为 Markdown。  
Lets Copilot Chat convert XLSX files to Markdown via the `@xlsx2md` command.

#### 快速开始 / Quick start

1. 安装 Python 依赖 / Install Python dependencies:
   ```bash
   pip install openpyxl Pillow
   ```

2. 用 VS Code 打开 `vscode-xlsx2md` 文件夹，按 `F5` 启动（开发者模式）。  
   Open `vscode-xlsx2md` in VS Code and press `F5` to run (developer mode).

3. 在资源管理器中右键任意 `.xlsx` 文件，选择 **Convert XLSX to Markdown**。  
   Right-click any `.xlsx` file in Explorer → **Convert XLSX to Markdown**.

4. 或在 Copilot Chat 中输入：/ Or in Copilot Chat:
   ```
   @xlsx2md #yourfile.xlsx
   ```

完整安装和使用说明（含中英文）：[`vscode-xlsx2md/README.md`](vscode-xlsx2md/README.md)  
Full bilingual installation & usage guide: [`vscode-xlsx2md/README.md`](vscode-xlsx2md/README.md)

---

### 三、MCP 服务器（让 Copilot 自动使用）/ MCP Server (Automatic Copilot Tool)

注册后，Copilot 在任何对话中只要你提到 XLSX 文件就会自动调用转换工具——无需 `@xlsx2md`。  
Once registered, Copilot will automatically use the conversion tool whenever you mention an XLSX file — no `@xlsx2md` needed.

#### 快速开始 / Quick start

1. 安装依赖 / Install dependencies:
   ```bash
   pip install -r mcp-xlsx2md/requirements.txt
   ```

2. 将示例配置复制为工作区 MCP 配置 / Copy the example config to your workspace:
   ```bash
   cp mcp-xlsx2md/mcp.json.example .vscode/mcp.json
   ```

3. 重载 VS Code (`Ctrl+Shift+P` → `Developer: Reload Window`)。

4. 在 Copilot Chat 中直接说：/ Then just say in Copilot Chat:
   ```
   请把 data.xlsx 转成 Markdown
   Convert report.xlsx to Markdown
   ```

完整安装和使用说明（含中英文）：[`mcp-xlsx2md/README.md`](mcp-xlsx2md/README.md)  
Full bilingual setup guide: [`mcp-xlsx2md/README.md`](mcp-xlsx2md/README.md)

---

## 运行测试 / Run Tests

```bash
pip install pytest openpyxl Pillow
pytest xlsx2md/tests/
```
