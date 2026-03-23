# EaseTools

Record My Easy Tools
```
记录我的日常小工具
```

---

## Tools

### xlsx2md — Excel to Markdown converter

Converts `.xlsx` spreadsheets to Markdown tables, with embedded image support.

```bash
pip install openpyxl Pillow
python xlsx2md/xlsx2md.py input.xlsx
```

See [`xlsx2md/xlsx2md.py`](xlsx2md/xlsx2md.py) for the full CLI reference.

---

## VS Code / GitHub Copilot integration

### Option A — VS Code Extension (`vscode-xlsx2md`)

Adds a **right-click → Convert XLSX to Markdown** command and a **`@xlsx2md`** Copilot Chat participant.

```
@xlsx2md #yourfile.xlsx
```

See [`vscode-xlsx2md/README.md`](vscode-xlsx2md/README.md) for installation & usage.

### Option B — MCP Server (`mcp-xlsx2md`)

Registers xlsx2md as a **GitHub Copilot tool** via the Model Context Protocol.  
Once configured, Copilot uses it *automatically* when you reference an XLSX file — no `@xlsx2md` needed.

```bash
pip install -r mcp-xlsx2md/requirements.txt
# copy mcp-xlsx2md/mcp.json.example → .vscode/mcp.json, then reload VS Code
```

See [`mcp-xlsx2md/README.md`](mcp-xlsx2md/README.md) for setup.
