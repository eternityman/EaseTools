# EaseTools

> Record My Easy Tools

**Language / 语言:** [English](README.md) | [中文](README.zh-CN.md)

---

## Tools

### xlsx2md — Excel to Markdown Converter

Converts Excel (`.xlsx`) spreadsheets to Markdown tables with embedded image support.

---

## Installation & Usage

### I. CLI Tool

#### 1. Install dependencies

```bash
pip install openpyxl Pillow
```

#### 2. Basic usage

```bash
# Convert input.xlsx to input.md
python xlsx2md/xlsx2md.py input.xlsx

# Specify output file
python xlsx2md/xlsx2md.py input.xlsx -o output.md

# Specify image directory
python xlsx2md/xlsx2md.py input.xlsx -i assets/images

# Text only, skip images
python xlsx2md/xlsx2md.py input.xlsx --no-images

# Convert only the sheet named "Sheet1"
python xlsx2md/xlsx2md.py input.xlsx --sheet Sheet1
```

Full documentation: [`xlsx2md/README.md`](xlsx2md/README.md).

---

### II. VS Code Extension

Lets Copilot Chat convert XLSX files to Markdown via the `@xlsx2md` command.

#### Quick start

1. Install Python dependencies:
   ```bash
   pip install openpyxl Pillow
   ```

2. Open `vscode-xlsx2md` in VS Code and press `F5` to run (developer mode).

3. Right-click any `.xlsx` file in Explorer → **Convert XLSX to Markdown**.

4. Or in Copilot Chat:
   ```
   @xlsx2md #yourfile.xlsx
   ```

Full installation & usage guide: [`vscode-xlsx2md/README.md`](vscode-xlsx2md/README.md)

---

### III. MCP Server (Automatic Copilot Tool)

Once registered, Copilot will automatically use the conversion tool whenever you mention an XLSX file — no `@xlsx2md` needed.

#### Quick start

1. Install dependencies:
   ```bash
   pip install -r mcp-xlsx2md/requirements.txt
   ```

2. Copy the example config to your workspace:
   ```bash
   cp mcp-xlsx2md/mcp.json.example .vscode/mcp.json
   ```

3. Reload VS Code (`Ctrl+Shift+P` → `Developer: Reload Window`).

4. Then just say in Copilot Chat:
   ```
   Convert report.xlsx to Markdown
   ```

Full setup guide: [`mcp-xlsx2md/README.md`](mcp-xlsx2md/README.md)

---

## Run Tests

```bash
pip install pytest openpyxl Pillow
pytest xlsx2md/tests/
```
