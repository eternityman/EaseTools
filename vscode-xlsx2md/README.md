# xlsx2md — VS Code Extension

> Convert Excel (`.xlsx`) spreadsheets to Markdown with embedded image support.  
> Integrates with **GitHub Copilot Chat** so Copilot can generate Markdown docs directly from XLSX files.

---

## 目录 / Table of Contents

- [安装 / Installation](#安装--installation)
- [使用 / Usage](#使用--usage)
- [插件设置 / Extension Settings](#插件设置--extension-settings)
- [功能说明 / Features](#功能说明--features)
- [常见问题 / FAQ](#常见问题--faq)

---

## 安装 / Installation

### 前置条件 / Prerequisites

| 要求 | 版本 | 说明 |
|------|------|------|
| **VS Code** | 1.90+ | 必须 / Required |
| **Python** | 3.7+ | 必须 / Required |
| **openpyxl** | ≥ 3.0.0 | 必须 / Required |
| **Pillow** | ≥ 9.0.0 | 推荐（图片处理）/ Recommended (image support) |

> **Requirements:** VS Code 1.90+, Python 3.7+, openpyxl, Pillow

---

### 步骤 1 — 安装 Python 依赖 / Step 1 — Install Python dependencies

```bash
pip install openpyxl Pillow
```

Windows 用户如果 `pip` 不在 PATH，可以使用：  
On Windows, if `pip` is not on PATH:
```bat
python -m pip install openpyxl Pillow
```

---

### 步骤 2 — 安装插件 / Step 2 — Install the extension

#### 方式 A：从源码安装（开发者模式）/ Method A: Install from source (developer mode)

1. 克隆仓库到本地 / Clone the repo:
   ```bash
   git clone https://github.com/eternityman/EaseTools.git
   cd EaseTools
   ```

2. 用 VS Code 打开 `vscode-xlsx2md` 文件夹 / Open the `vscode-xlsx2md` folder in VS Code:
   ```bash
   code vscode-xlsx2md
   ```

3. 按 `F5` 启动扩展开发主机，即可在新窗口中使用插件。  
   Press `F5` to launch the Extension Development Host — the extension is active in the new window.

#### 方式 B：安装 VSIX 包 / Method B: Install VSIX package

如果已有 `.vsix` 安装包 / If you have a `.vsix` package:

1. 打开命令面板 `Ctrl+Shift+P` / Open Command Palette: `Ctrl+Shift+P`
2. 选择 `Extensions: Install from VSIX…` 
3. 选择 `.vsix` 文件 / Select the `.vsix` file

---

### 步骤 3 — 检查 Python 路径配置 / Step 3 — Verify Python path setting

打开 VS Code 设置 (`Ctrl+,`) 搜索 `xlsx2md`：  
Open VS Code Settings (`Ctrl+,`) and search for `xlsx2md`:

- **`xlsx2md.pythonPath`**：默认为 `python3`。如果您的 Python 可执行文件名不同，请修改此项。  
  Default is `python3`. Change this if your Python binary has a different name.  
  - macOS/Linux: `python3` ✓  
  - Windows (通常 / typical): `python`  
  - 虚拟环境 / virtualenv: `/path/to/.venv/bin/python3`

---

## 使用 / Usage

### 方式 1 — 右键菜单 / Method 1 — Right-click context menu

在资源管理器中右键点击任意 `.xlsx` 文件，选择：  
Right-click any `.xlsx` file in the Explorer:

| 菜单项 | 功能 |
|--------|------|
| **Convert XLSX to Markdown** | 转换并提取图片 / Convert with image extraction |
| **Convert XLSX to Markdown (text only)** | 仅转换文本，不提取图片 / Text only, skip images |

转换完成后，`.md` 文件会自动在编辑器中打开，图片保存在同目录的 `images/` 子文件夹。  
The `.md` file opens automatically; images are saved to the `images/` sub-folder.

---

### 方式 2 — 命令面板 / Method 2 — Command Palette

按 `Ctrl+Shift+P`（macOS: `Cmd+Shift+P`），输入：  
Press `Ctrl+Shift+P` (macOS: `Cmd+Shift+P`) and type:

```
xlsx2md: Convert XLSX to Markdown
xlsx2md: Convert XLSX to Markdown (text only)
```

如果当前编辑器没有打开 XLSX 文件，会弹出文件选择对话框。  
If no XLSX is open in the editor, a file picker dialog will appear.

---

### 方式 3 — Copilot Chat（`@xlsx2md`）/ Method 3 — Copilot Chat

> 需要 VS Code 1.90+ 并安装 GitHub Copilot Chat 扩展。  
> Requires VS Code 1.90+ with GitHub Copilot Chat extension.

打开 Copilot Chat 面板（`Ctrl+Alt+I`），然后输入：  
Open Copilot Chat (`Ctrl+Alt+I`) and type:

#### 基本用法 / Basic usage

```
@xlsx2md #yourfile.xlsx
```

点击聊天输入框左侧的 **回形针图标**，选择 `.xlsx` 文件，或者直接输入文件名：  
Click the **paperclip icon** in the chat input to attach a file, or type the filename:

```
@xlsx2md convert report.xlsx to markdown
```

#### 不提取图片 / Skip images

```
@xlsx2md #budget.xlsx no images
```

#### 只转换某个 Sheet / Convert a specific sheet

通过 MCP 服务器可指定 Sheet（见下文）。Chat 参与者模式会转换所有 Sheet。  
Sheet filtering is available via the MCP server (see below). The `@xlsx2md` participant converts all sheets.

#### 查看帮助 / Show help

```
@xlsx2md /help
```

#### 可用命令 / Available commands

| 命令 / Command | 说明 / Description |
|---|---|
| `@xlsx2md #file.xlsx` | 转换（含图片）/ Convert with images |
| `@xlsx2md /convert #file.xlsx` | 显式转换命令 / Explicit convert |
| `@xlsx2md /help` | 显示帮助 / Show help |

---

### 方式 4 — MCP 服务器（让 Copilot 自动使用）/ Method 4 — MCP Server (automatic Copilot tool)

> 这是最深度的集成方式：Copilot 无需 `@xlsx2md` 前缀，在任何对话中都能自动读取 XLSX 文件。  
> This is the deepest integration: Copilot can read XLSX files automatically in any chat, without typing `@xlsx2md`.

详细步骤见 [`../mcp-xlsx2md/README.md`](../mcp-xlsx2md/README.md)。  
See [`../mcp-xlsx2md/README.md`](../mcp-xlsx2md/README.md) for full setup instructions.

---

## 插件设置 / Extension Settings

打开 VS Code 设置 (`Ctrl+,`) 并搜索 `xlsx2md` 来查看所有选项：  
Open VS Code Settings (`Ctrl+,`) and search `xlsx2md` to see all options:

| 设置键 / Setting | 默认值 / Default | 说明 / Description |
|---|---|---|
| `xlsx2md.pythonPath` | `python3` | Python 解释器路径 / Python interpreter path |
| `xlsx2md.scriptPath` | *(内置 / bundled)* | 自定义 `xlsx2md.py` 路径；留空使用内置脚本 / Custom path to `xlsx2md.py`; leave empty for bundled |
| `xlsx2md.imageDir` | `images` | 图片输出子目录名 / Sub-directory name for extracted images |
| `xlsx2md.conversionTimeout` | `120` | 最大等待秒数（大文件可增加）/ Max wait seconds (increase for large files) |

---

## 功能说明 / Features

### 输出示例 / Output example

给定包含姓名、头像图片、备注的 XLSX 文件，输出结果如下：  
Given an XLSX with name, avatar image, and notes columns, the output looks like:

```markdown
## Sheet1

| 姓名 | 头像 | 备注 |
| --- | --- | --- |
| 张三 | ![image](images/Sheet1_img_0.png) | 经理 |
| 李四 | ![image](images/Sheet1_img_1.png) | 工程师 |
```

图片文件保存在：/ Image files saved at:

```
output/
├── output.md
└── images/
    ├── Sheet1_img_0.png
    └── Sheet1_img_1.png
```

### 边界情况处理 / Edge case handling

| 情况 / Situation | 处理方式 / Handling |
|---|---|
| 单元格含竖线 `\|` | 自动转义为 `\\\|` / Auto-escaped to `\\\|` |
| 单元格内换行 | 替换为 `<br>` / Replaced with `<br>` |
| 合并单元格 | 非主单元格输出空字符串 / Non-master cells output empty string |
| 空 Sheet | 输出提示文字 / Outputs placeholder text |
| 无图片的 XLSX | 正常转换文本表格 / Text table converted normally |

---

## 常见问题 / FAQ

**Q: 转换失败，提示 "找不到命令 python3" / "python3 not found"**  
A: 打开设置，将 `xlsx2md.pythonPath` 改为您系统上的 Python 路径（如 `python` 或绝对路径）。  
A: Open Settings and set `xlsx2md.pythonPath` to your Python binary (e.g. `python` or an absolute path).

**Q: 图片没有出现在 Markdown 中 / Images missing from Markdown**  
A: 确认已安装 `openpyxl` 和 `Pillow`：`pip install openpyxl Pillow`  
A: Ensure `openpyxl` and `Pillow` are installed: `pip install openpyxl Pillow`

**Q: `@xlsx2md` 在 Copilot Chat 中不出现 / `@xlsx2md` doesn't appear in Copilot Chat**  
A: 确认已安装 GitHub Copilot Chat 扩展，且 VS Code 版本 ≥ 1.90。  
A: Ensure GitHub Copilot Chat extension is installed and VS Code ≥ 1.90.

**Q: 转换超时 / Conversion timed out**  
A: 对于大文件，增加 `xlsx2md.conversionTimeout` 的值（单位：秒）。  
A: For large files, increase `xlsx2md.conversionTimeout` (in seconds).
