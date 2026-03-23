# mcp-xlsx2md

MCP (Model Context Protocol) server that lets **GitHub Copilot in VS Code** convert `.xlsx` files to Markdown automatically.

## What is this?

VS Code 1.99+ supports [MCP servers](https://code.visualstudio.com/docs/copilot/chat/mcp-servers) as Copilot tools. Once registered, Copilot can call `convert_xlsx_to_markdown` whenever you reference an Excel file in chat — no plugin needed.

## Quick start

### 1. Install dependencies

```bash
pip install -r mcp-xlsx2md/requirements.txt
```

### 2. Register the server in VS Code

Create or edit `.vscode/mcp.json` in your workspace (copy from `mcp.json.example`):

```json
{
  "servers": {
    "xlsx2md": {
      "type": "stdio",
      "command": "python",
      "args": ["${workspaceFolder}/mcp-xlsx2md/server.py"]
    }
  }
}
```

Alternatively, add this to VS Code **User Settings (JSON)**:

```json
"mcp": {
  "servers": {
    "xlsx2md": {
      "type": "stdio",
      "command": "python",
      "args": ["/absolute/path/to/EaseTools/mcp-xlsx2md/server.py"]
    }
  }
}
```

### 3. Use in Copilot Chat

After reloading VS Code, open Copilot Chat and type:

```
Convert mydata.xlsx to Markdown
```

or attach the file directly:

```
#mydata.xlsx  Please convert this to Markdown
```

Copilot will call the `convert_xlsx_to_markdown` tool and stream back the result.

## Tool reference

### `convert_xlsx_to_markdown`

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `xlsx_path` | string | *(required)* | Path to the `.xlsx` file |
| `image_dir` | string | `"images"` | Sub-directory for extracted images |
| `sheet` | string | `""` (all) | Only convert the named sheet |
| `no_images` | boolean | `false` | Skip image extraction |

**Returns:** The complete Markdown content as a string (images are also saved to disk).

## Testing the server manually

```bash
cd EaseTools
python mcp-xlsx2md/server.py
```

The server speaks the MCP JSON-RPC protocol over stdin/stdout. Use the [MCP Inspector](https://github.com/modelcontextprotocol/inspector) for interactive testing.
