# xlsx2md — VS Code Extension

Convert **Excel (.xlsx) spreadsheets to Markdown** with embedded image support, directly inside VS Code.  
Integrates with **GitHub Copilot Chat** so you can ask Copilot to convert files naturally.

---

## Features

| Feature | How |
| --- | --- |
| Right-click → Convert XLSX to Markdown | Explorer context menu on any `.xlsx` file |
| Command Palette | `xlsx2md: Convert XLSX to Markdown` |
| Copilot Chat participant | `@xlsx2md #yourfile.xlsx` |
| Image extraction | Embedded images are saved to `images/` and referenced in the Markdown |
| Text-only mode | Skip image extraction with the *text only* command or `@xlsx2md no images` |

---

## Setup

### Requirements

- **Python 3.9+** with the following packages:

```bash
pip install openpyxl Pillow
```

The extension calls `python3 xlsx2md.py` internally. If your Python binary has a different name, update **Settings → xlsx2md.pythonPath**.

---

## Usage

### 1. Right-click in Explorer

Right-click any `.xlsx` file → **Convert XLSX to Markdown**.  
The `.md` file opens automatically next to the original.

### 2. Command Palette

`Ctrl+Shift+P` → `xlsx2md: Convert XLSX to Markdown`

### 3. Copilot Chat (`@xlsx2md`)

Open Copilot Chat (`Ctrl+Alt+I`) and type:

```
@xlsx2md #report.xlsx
```

Use the **#file** paperclip button to attach the file, or just type the name:

```
@xlsx2md convert budget.xlsx to markdown, no images
```

The Markdown content streams directly into the chat window. A **Open Markdown file** button lets you view the saved file.

#### Available Copilot commands

| Command | What it does |
| --- | --- |
| `@xlsx2md #file.xlsx` | Convert with images (default) |
| `@xlsx2md /convert #file.xlsx` | Explicit convert command |
| `@xlsx2md /help` | Show usage instructions |

---

## Extension settings

| Setting | Default | Description |
| --- | --- | --- |
| `xlsx2md.pythonPath` | `python3` | Python interpreter path |
| `xlsx2md.scriptPath` | *(bundled)* | Custom path to `xlsx2md.py` |
| `xlsx2md.imageDir` | `images` | Directory name for extracted images |

---

## MCP server (alternative Copilot integration)

For a deeper Copilot integration — where Copilot can *automatically* call xlsx2md as a **tool** without you typing `@xlsx2md` — use the bundled MCP server:

1. Install: `pip install -r mcp-xlsx2md/requirements.txt`
2. Copy `mcp-xlsx2md/mcp.json.example` to `.vscode/mcp.json`
3. Reload VS Code

Copilot will then discover the `convert_xlsx_to_markdown` tool and use it automatically when you reference an XLSX file in any chat prompt.

See [`../mcp-xlsx2md/README.md`](../mcp-xlsx2md/README.md) for details.
