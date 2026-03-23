# mcp-xlsx2md — MCP Server for Copilot

> An MCP server that lets **GitHub Copilot in VS Code** automatically convert `.xlsx` files to Markdown.

**Language / 语言:** [English](README.md) | [中文](README.zh-CN.md)

---

## Table of Contents

- [What is this?](#what-is-this)
- [Installation](#installation)
- [Usage](#usage)
- [Tool reference](#tool-reference)
- [Manual testing](#manual-testing)

---

## What is this?

VS Code 1.99+ supports [MCP servers](https://code.visualstudio.com/docs/copilot/chat/mcp-servers) as Copilot tools.  
Once registered, Copilot will **automatically** call `convert_xlsx_to_markdown` whenever you reference an Excel file in chat — no `@xlsx2md` prefix needed.

---

## Installation

### Step 1 — Install dependencies

```bash
pip install -r mcp-xlsx2md/requirements.txt
```

Dependencies:
- `mcp` ≥ 1.0.0 — MCP Python SDK
- `openpyxl` ≥ 3.0.0 — Read XLSX files
- `Pillow` ≥ 9.0.0 — Image conversion

---

### Step 2 — Register the server in VS Code

#### Method A: Workspace config (recommended)

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

> On Windows, change `python3` to `python`.

#### Method B: User global settings

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

### Step 3 — Reload VS Code

Press `Ctrl+Shift+P` → `Developer: Reload Window`.

After reloading, `convert_xlsx_to_markdown` will appear in Copilot's tool list.

---

## Usage

### In Copilot Chat

After registration, just describe your need in Copilot Chat:

```
Convert report.xlsx to Markdown
```

```
#data.xlsx  Convert this Excel to Markdown, no images
```

Copilot will automatically call the `convert_xlsx_to_markdown` tool and stream the result into the chat.

### Image handling

- Images are saved to an `images/` sub-directory **next to the XLSX file** by default.
- Image references in Markdown use relative paths; saving the `.md` next to the XLSX ensures correct display.

---

## Tool reference

### `convert_xlsx_to_markdown`

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `xlsx_path` | string | *(required)* | Path to the `.xlsx` file |
| `image_dir` | string | `"images"` | Sub-directory for extracted images |
| `sheet` | string | `""` (all) | Convert only the named sheet |
| `no_images` | boolean | `false` | Skip image extraction |

**Returns:** The complete Markdown content as a string (images also saved to disk).

---

## Manual testing

Start the server manually to test (MCP JSON-RPC protocol over stdin/stdout):

```bash
cd EaseTools
python3 mcp-xlsx2md/server.py
```

Use [MCP Inspector](https://github.com/modelcontextprotocol/inspector) for interactive testing:

```bash
npx @modelcontextprotocol/inspector python3 mcp-xlsx2md/server.py
```

---

## Version requirements

| Software | Version |
|----------|---------|
| VS Code | 1.99+ |
| Python | 3.7+ |
| mcp | 1.0.0+ |
| openpyxl | 3.0.0+ |
| Pillow | 9.0.0+ (optional) |
