# mcp-xlsx2md — MCP Server for Copilot

> MCP (Model Context Protocol) 服务器，让 **VS Code 中的 GitHub Copilot** 自动将 `.xlsx` 文件转换为 Markdown。  
> An MCP server that lets **GitHub Copilot in VS Code** automatically convert `.xlsx` files to Markdown.

---

## 目录 / Table of Contents

- [是什么 / What is this?](#是什么--what-is-this)
- [安装 / Installation](#安装--installation)
- [使用 / Usage](#使用--usage)
- [工具参数 / Tool reference](#工具参数--tool-reference)
- [手动测试 / Manual testing](#手动测试--manual-testing)

---

## 是什么 / What is this?

VS Code 1.99+ 支持通过 [MCP 协议](https://code.visualstudio.com/docs/copilot/chat/mcp-servers)向 Copilot 注册自定义工具。  
注册后，Copilot 在任何对话中只要你提到 XLSX 文件，就会 **自动** 调用 `convert_xlsx_to_markdown` 工具——无需输入 `@xlsx2md`。

VS Code 1.99+ supports [MCP servers](https://code.visualstudio.com/docs/copilot/chat/mcp-servers) as Copilot tools.  
Once registered, Copilot will **automatically** call `convert_xlsx_to_markdown` whenever you reference an Excel file in chat — no `@xlsx2md` prefix needed.

---

## 安装 / Installation

### 步骤 1 — 安装依赖 / Step 1 — Install dependencies

```bash
pip install -r mcp-xlsx2md/requirements.txt
```

依赖包含 / Dependencies:
- `mcp` ≥ 1.0.0 — MCP Python SDK
- `openpyxl` ≥ 3.0.0 — 读取 XLSX / Read XLSX files
- `Pillow` ≥ 9.0.0 — 图片转换 / Image conversion

---

### 步骤 2 — 在 VS Code 中注册服务器 / Step 2 — Register the server in VS Code

#### 方式 A：工作区配置（推荐）/ Method A: Workspace config (recommended)

在项目根目录创建 `.vscode/mcp.json`（可直接复制 `mcp-xlsx2md/mcp.json.example`）：  
Create `.vscode/mcp.json` in your project root (copy from `mcp-xlsx2md/mcp.json.example`):

```json
{
  "servers": {
    "xlsx2md": {
      "type": "stdio",
      "command": "python3",
      "args": ["${workspaceFolder}/mcp-xlsx2md/server.py"]
    }
  }
}
```

> Windows 用户将 `python3` 改为 `python`。  
> On Windows, change `python3` to `python`.

#### 方式 B：用户全局配置 / Method B: User global settings

打开 VS Code 设置 JSON（`Ctrl+Shift+P` → `Open User Settings JSON`），添加：  
Open VS Code User Settings JSON (`Ctrl+Shift+P` → `Open User Settings JSON`), add:

```json
"mcp": {
  "servers": {
    "xlsx2md": {
      "type": "stdio",
      "command": "python3",
      "args": ["/absolute/path/to/EaseTools/mcp-xlsx2md/server.py"]
    }
  }
}
```

---

### 步骤 3 — 重载 VS Code / Step 3 — Reload VS Code

按 `Ctrl+Shift+P` → `Developer: Reload Window`。  
Press `Ctrl+Shift+P` → `Developer: Reload Window`.

重载后，Copilot Chat 的工具列表中会出现 `convert_xlsx_to_markdown`。  
After reloading, `convert_xlsx_to_markdown` will appear in Copilot's tool list.

---

## 使用 / Usage

### 在 Copilot Chat 中 / In Copilot Chat

注册后，直接在 Copilot Chat 中描述你的需求：  
After registration, just describe your need in Copilot Chat:

```
请把 data.xlsx 转成 Markdown 文档
```

```
Convert report.xlsx to Markdown
```

```
#data.xlsx  请把这个 Excel 转成 Markdown，不需要图片
```

Copilot 会自动调用 `convert_xlsx_to_markdown` 工具，将结果流式返回到对话窗口。  
Copilot will automatically call the `convert_xlsx_to_markdown` tool and stream the result into the chat.

### 图片处理说明 / Image handling

- 图片默认保存到 XLSX 文件**同目录**下的 `images/` 子目录。  
  Images are saved to an `images/` sub-directory **next to the XLSX file** by default.
- Markdown 中的图片引用使用相对路径，将 `.md` 文件保存到 XLSX 同目录即可正常显示。  
  Image references in Markdown use relative paths; saving the `.md` next to the XLSX ensures correct display.

---

## 工具参数 / Tool reference

### `convert_xlsx_to_markdown`

| 参数 / Parameter | 类型 / Type | 默认 / Default | 说明 / Description |
|---|---|---|---|
| `xlsx_path` | string | *(必填 / required)* | XLSX 文件的绝对或相对路径 / Path to the `.xlsx` file |
| `image_dir` | string | `"images"` | 图片输出子目录 / Sub-directory for extracted images |
| `sheet` | string | `""` (全部 / all) | 只转换指定名称的 Sheet / Convert only the named sheet |
| `no_images` | boolean | `false` | 跳过图片提取 / Skip image extraction |

**返回 / Returns:** 完整的 Markdown 字符串（图片同时保存到磁盘）。  
**Returns:** The complete Markdown content as a string (images also saved to disk).

---

## 手动测试 / Manual testing

在终端中直接启动服务器（MCP JSON-RPC 协议通过 stdin/stdout 通信）：  
Start the server manually to test (MCP JSON-RPC protocol over stdin/stdout):

```bash
cd EaseTools
python3 mcp-xlsx2md/server.py
```

使用 [MCP Inspector](https://github.com/modelcontextprotocol/inspector) 进行交互式测试：  
Use [MCP Inspector](https://github.com/modelcontextprotocol/inspector) for interactive testing:

```bash
npx @modelcontextprotocol/inspector python3 mcp-xlsx2md/server.py
```

---

## 版本要求 / Version requirements

| 软件 / Software | 版本 / Version |
|---|---|
| VS Code | 1.99+ |
| Python | 3.7+ |
| mcp | 1.0.0+ |
| openpyxl | 3.0.0+ |
| Pillow | 9.0.0+ (可选 / optional) |
