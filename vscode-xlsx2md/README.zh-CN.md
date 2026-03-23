# xlsx2md — VS Code 插件

> 将 Excel (`.xlsx`) 电子表格转换为 Markdown，支持提取嵌入图片。  
> 与 **GitHub Copilot Chat** 深度集成，Copilot 可直接从 XLSX 文件生成 Markdown 文档。

**语言 / Language:** [中文](README.zh-CN.md) | [English](README.md)

---

## 目录

- [安装](#安装)
- [使用](#使用)
- [插件设置](#插件设置)
- [功能说明](#功能说明)
- [常见问题](#常见问题)

---

## 安装

### 方式 A — VS Code 插件市场（推荐）

> 最简单的一键安装方式。

1. 打开 VS Code，按 `Ctrl+Shift+X` 打开插件面板。

2. 搜索 **`xlsx2md`** 或 **`easetools.xlsx2md`**，点击 **Install**。

3. 安装完成后，插件会自动检测 Python 依赖是否就绪。
   - 若缺少依赖，会弹出通知 → 点击 **"Install now"** 即可一键安装 `openpyxl` 和 `Pillow`。

**前置条件：**

| 要求 | 版本 | 说明 |
|------|------|------|
| **VS Code** | 1.90+ | 必须 |
| **Python** | 3.7+ | 必须（插件会自动安装 pip 包） |

> Python 本身需要预先安装。如果系统还没有 Python，请先访问 [python.org](https://www.python.org/downloads/) 下载安装。

---

### 方式 B — 下载 VSIX 离线安装

如果无法访问插件市场，可以从 [GitHub Releases](https://github.com/eternityman/EaseTools/releases) 下载 `.vsix` 文件：

```bash
# 命令行一键安装
code --install-extension easetools.xlsx2md-*.vsix
```

或通过 UI：

1. 打开命令面板 `Ctrl+Shift+P` → `Extensions: Install from VSIX…`
2. 选择下载的 `.vsix` 文件。

---

### 方式 C — 从源码安装（开发者）

```bash
git clone https://github.com/eternityman/EaseTools.git
code EaseTools/vscode-xlsx2md   # 打开扩展目录
# 按 F5 启动扩展开发主机
```

---

### Python 依赖手动安装

如果自动安装失败，或者需要手动重新安装：

**方法 1 — 命令面板** `Ctrl+Shift+P` → `xlsx2md: Install Python Dependencies`

**方法 2 — 终端**
```bash
pip install openpyxl Pillow
# Windows 上如果 pip 不在 PATH：
python -m pip install openpyxl Pillow
```

---

## 使用

### 方式 1 — 右键菜单

在资源管理器中右键点击任意 `.xlsx` 文件，选择：

| 菜单项 | 功能 |
|--------|------|
| **Convert XLSX to Markdown** | 转换并提取图片 |
| **Convert XLSX to Markdown (text only)** | 仅转换文本，不提取图片 |

转换完成后，`.md` 文件会自动在编辑器中打开，图片保存在同目录的 `images/` 子文件夹。

---

### 方式 2 — 命令面板

按 `Ctrl+Shift+P`（macOS: `Cmd+Shift+P`），输入：

```
xlsx2md: Convert XLSX to Markdown
xlsx2md: Convert XLSX to Markdown (text only)
```

如果当前编辑器没有打开 XLSX 文件，会弹出文件选择对话框。

---

### 方式 3 — Copilot Chat（`@xlsx2md`）

> 需要 VS Code 1.90+ 并安装 GitHub Copilot Chat 扩展。

打开 Copilot Chat 面板（`Ctrl+Alt+I`），然后输入：

#### 基本用法

```
@xlsx2md #yourfile.xlsx
```

点击聊天输入框左侧的 **回形针图标**，选择 `.xlsx` 文件，或者直接输入文件名：

```
@xlsx2md convert report.xlsx to markdown
```

#### 不提取图片

```
@xlsx2md #budget.xlsx no images
```

#### 只转换某个 Sheet

通过 MCP 服务器可指定 Sheet（见下文）。Chat 参与者模式会转换所有 Sheet。

#### 查看帮助

```
@xlsx2md /help
```

#### 可用命令

| 命令 | 说明 |
|------|------|
| `@xlsx2md #file.xlsx` | 转换（含图片） |
| `@xlsx2md /convert #file.xlsx` | 显式转换命令 |
| `@xlsx2md /help` | 显示帮助 |

---

### 方式 4 — MCP 服务器（让 Copilot 自动使用）

> 这是最深度的集成方式：Copilot 无需 `@xlsx2md` 前缀，在任何对话中都能自动读取 XLSX 文件。

详细步骤见 [`../mcp-xlsx2md/README.zh-CN.md`](../mcp-xlsx2md/README.zh-CN.md)。

---

## 插件设置

打开 VS Code 设置（`Ctrl+,`）并搜索 `xlsx2md` 来查看所有选项：

| 设置键 | 默认值 | 说明 |
|--------|--------|------|
| `xlsx2md.pythonPath` | `python3` | Python 解释器路径 |
| `xlsx2md.scriptPath` | *(内置)* | 自定义 `xlsx2md.py` 路径；留空使用内置脚本 |
| `xlsx2md.imageDir` | `images` | 图片输出子目录名 |
| `xlsx2md.conversionTimeout` | `120` | 最大等待秒数（大文件可增加） |

---

## 功能说明

### 输出示例

给定包含姓名、头像图片、备注的 XLSX 文件，输出结果如下：

```markdown
## Sheet1

| 姓名 | 头像 | 备注 |
| --- | --- | --- |
| 张三 | ![image](images/Sheet1_img_0.png) | 经理 |
| 李四 | ![image](images/Sheet1_img_1.png) | 工程师 |
```

图片文件保存在：

```
output/
├── output.md
└── images/
    ├── Sheet1_img_0.png
    └── Sheet1_img_1.png
```

### 边界情况处理

| 情况 | 处理方式 |
|------|----------|
| 单元格含竖线 `\|` | 自动转义为 `\\\|` |
| 单元格内换行 | 替换为 `<br>` |
| 合并单元格 | 非主单元格输出空字符串 |
| 空 Sheet | 输出提示文字 |
| 无图片的 XLSX | 正常转换文本表格 |

---

## 常见问题

**Q: 转换失败，提示 "找不到命令 python3"**  
A: 打开设置，将 `xlsx2md.pythonPath` 改为您系统上的 Python 路径（如 `python` 或绝对路径）。

**Q: 图片没有出现在 Markdown 中**  
A: 确认已安装 `openpyxl` 和 `Pillow`。运行命令面板 → `xlsx2md: Install Python Dependencies`，或手动执行：`pip install openpyxl Pillow`

**Q: `@xlsx2md` 在 Copilot Chat 中不出现**  
A: 确认已安装 GitHub Copilot Chat 扩展，且 VS Code 版本 ≥ 1.90。

**Q: 转换超时**  
A: 对于大文件，增加 `xlsx2md.conversionTimeout` 的值（单位：秒）。

**Q: 如何重新安装 Python 依赖**  
A: 打开命令面板 `Ctrl+Shift+P` → `xlsx2md: Install Python Dependencies`。
