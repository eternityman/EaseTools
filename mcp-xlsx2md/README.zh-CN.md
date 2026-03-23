# mcp-xlsx2md — Copilot MCP 服务器

> MCP (Model Context Protocol) 服务器，让 **VS Code 中的 GitHub Copilot** 自动将 `.xlsx` 文件转换为 Markdown。

**语言 / Language:** [中文](README.zh-CN.md) | [English](README.md)

---

## 目录

- [是什么？](#是什么)
- [安装](#安装)
- [使用](#使用)
- [工具参数](#工具参数)
- [手动测试](#手动测试)

---

## 是什么？

VS Code 1.99+ 支持通过 [MCP 协议](https://code.visualstudio.com/docs/copilot/chat/mcp-servers)向 Copilot 注册自定义工具。  
注册后，Copilot 在任何对话中只要你提到 XLSX 文件，就会 **自动** 调用 `convert_xlsx_to_markdown` 工具——无需输入 `@xlsx2md`。

---

## 安装

### 步骤 1 — 安装依赖

```bash
pip install -r mcp-xlsx2md/requirements.txt
```

依赖包含：
- `mcp` ≥ 1.0.0 — MCP Python SDK
- `openpyxl` ≥ 3.0.0 — 读取 XLSX
- `Pillow` ≥ 9.0.0 — 图片转换

---

### 步骤 2 — 在 VS Code 中注册服务器

#### 方式 A：工作区配置（推荐）

在项目根目录创建 `.vscode/mcp.json`（可直接复制 `mcp-xlsx2md/mcp.json.example`）：

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

#### 方式 B：用户全局配置

打开 VS Code 设置 JSON（`Ctrl+Shift+P` → `Open User Settings JSON`），添加：

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

### 步骤 3 — 重载 VS Code

按 `Ctrl+Shift+P` → `Developer: Reload Window`。

重载后，Copilot Chat 的工具列表中会出现 `convert_xlsx_to_markdown`。

---

## 使用

### 在 Copilot Chat 中

注册后，直接在 Copilot Chat 中描述你的需求：

```
请把 data.xlsx 转成 Markdown 文档
```

```
#data.xlsx  请把这个 Excel 转成 Markdown，不需要图片
```

Copilot 会自动调用 `convert_xlsx_to_markdown` 工具，将结果流式返回到对话窗口。

### 图片处理说明

- 图片默认保存到 XLSX 文件**同目录**下的 `images/` 子目录。
- Markdown 中的图片引用使用相对路径，将 `.md` 文件保存到 XLSX 同目录即可正常显示。

---

## 工具参数

### `convert_xlsx_to_markdown`

| 参数 | 类型 | 默认 | 说明 |
|------|------|------|------|
| `xlsx_path` | string | *(必填)* | XLSX 文件的绝对或相对路径 |
| `image_dir` | string | `"images"` | 图片输出子目录 |
| `sheet` | string | `""` (全部) | 只转换指定名称的 Sheet |
| `no_images` | boolean | `false` | 跳过图片提取 |

**返回：** 完整的 Markdown 字符串（图片同时保存到磁盘）。

---

## 手动测试

在终端中直接启动服务器（MCP JSON-RPC 协议通过 stdin/stdout 通信）：

```bash
cd EaseTools
python3 mcp-xlsx2md/server.py
```

使用 [MCP Inspector](https://github.com/modelcontextprotocol/inspector) 进行交互式测试：

```bash
npx @modelcontextprotocol/inspector python3 mcp-xlsx2md/server.py
```

---

## 版本要求

| 软件 | 版本 |
|------|------|
| VS Code | 1.99+ |
| Python | 3.7+ |
| mcp | 1.0.0+ |
| openpyxl | 3.0.0+ |
| Pillow | 9.0.0+（可选） |
