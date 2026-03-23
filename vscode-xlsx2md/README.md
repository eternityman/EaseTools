# xlsx2md — VS Code Extension

> Convert Excel (`.xlsx`) spreadsheets to Markdown with embedded image support.  
> Integrates with **GitHub Copilot Chat** so Copilot can generate Markdown docs directly from XLSX files.

**Language / 语言:** [English](README.md) | [中文](README.zh-CN.md)

---

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Extension Settings](#extension-settings)
- [Features](#features)
- [FAQ](#faq)

---

## Installation

### Method A — VS Code Marketplace (recommended)

> The easiest one-click install method.

1. Open VS Code, press `Ctrl+Shift+X` to open the Extensions panel.

2. Search for **`xlsx2md`** or **`easetools.xlsx2md`**, then click **Install**.

3. After install, the extension automatically checks whether Python dependencies are present.
   - If packages are missing, a notification appears → click **"Install now"** to install `openpyxl` and `Pillow` automatically.

**Prerequisites:**

| Requirement | Version | Note |
|-------------|---------|------|
| **VS Code** | 1.90+ | Required |
| **Python** | 3.7+ | Required (extension auto-installs pip packages) |

> Python itself must be installed first. If not already installed, download it from [python.org](https://www.python.org/downloads/).

---

### Method B — Install from VSIX (offline)

If the marketplace is unavailable, download the `.vsix` from [GitHub Releases](https://github.com/eternityman/EaseTools/releases):

```bash
# One command install
code --install-extension easetools.xlsx2md-*.vsix
```

Or via UI:

1. Open Command Palette `Ctrl+Shift+P` → `Extensions: Install from VSIX…`
2. Select the downloaded `.vsix` file.

---

### Method C — Install from source (developers)

```bash
git clone https://github.com/eternityman/EaseTools.git
code EaseTools/vscode-xlsx2md   # open extension folder
# Press F5 to launch Extension Development Host
```

---

### Manual Python dependency install

If auto-install fails, or you need to reinstall manually:

**Method 1 — Command Palette** `Ctrl+Shift+P` → `xlsx2md: Install Python Dependencies`

**Method 2 — Terminal**
```bash
pip install openpyxl Pillow
# Windows fallback if pip is not on PATH:
python -m pip install openpyxl Pillow
```

---

## Usage

### Method 1 — Right-click context menu

Right-click any `.xlsx` file in the Explorer:

| Menu item | Function |
|-----------|----------|
| **Convert XLSX to Markdown** | Convert with image extraction |
| **Convert XLSX to Markdown (text only)** | Text only, skip images |

The `.md` file opens automatically; images are saved to the `images/` sub-folder.

---

### Method 2 — Command Palette

Press `Ctrl+Shift+P` (macOS: `Cmd+Shift+P`) and type:

```
xlsx2md: Convert XLSX to Markdown
xlsx2md: Convert XLSX to Markdown (text only)
```

If no XLSX is open in the editor, a file picker dialog will appear.

---

### Method 3 — Copilot Chat (`@xlsx2md`)

> Requires VS Code 1.90+ with GitHub Copilot Chat extension.

Open Copilot Chat (`Ctrl+Alt+I`) and type:

#### Basic usage

```
@xlsx2md #yourfile.xlsx
```

Click the **paperclip icon** in the chat input to attach a file, or type the filename:

```
@xlsx2md convert report.xlsx to markdown
```

#### Skip images

```
@xlsx2md #budget.xlsx no images
```

#### Convert a specific sheet

Sheet filtering is available via the MCP server (see below). The `@xlsx2md` participant converts all sheets.

#### Show help

```
@xlsx2md /help
```

#### Available commands

| Command | Description |
|---------|-------------|
| `@xlsx2md #file.xlsx` | Convert with images |
| `@xlsx2md /convert #file.xlsx` | Explicit convert |
| `@xlsx2md /help` | Show help |

---

### Method 4 — MCP Server (automatic Copilot tool)

> This is the deepest integration: Copilot can read XLSX files automatically in any chat, without typing `@xlsx2md`.

See [`../mcp-xlsx2md/README.md`](../mcp-xlsx2md/README.md) for full setup instructions.

---

## Extension Settings

Open VS Code Settings (`Ctrl+,`) and search `xlsx2md` to see all options:

| Setting | Default | Description |
|---------|---------|-------------|
| `xlsx2md.pythonPath` | `python3` | Python interpreter path |
| `xlsx2md.scriptPath` | *(bundled)* | Custom path to `xlsx2md.py`; leave empty for bundled |
| `xlsx2md.imageDir` | `images` | Sub-directory name for extracted images |
| `xlsx2md.conversionTimeout` | `120` | Max wait seconds (increase for large files) |

---

## Features

### Output example

Given an XLSX with name, avatar image, and notes columns, the output looks like:

```markdown
## Sheet1

| 姓名 | 头像 | 备注 |
| --- | --- | --- |
| 张三 | ![image](images/Sheet1_img_0.png) | 经理 |
| 李四 | ![image](images/Sheet1_img_1.png) | 工程师 |
```

Image files saved at:

```
output/
├── output.md
└── images/
    ├── Sheet1_img_0.png
    └── Sheet1_img_1.png
```

### Edge case handling

| Situation | Handling |
|-----------|----------|
| Cell contains `\|` | Auto-escaped to `\\\|` |
| Newline inside cell | Replaced with `<br>` |
| Merged cell | Non-master cells output empty string |
| Empty sheet | Outputs placeholder text |
| XLSX without images | Text table converted normally |

---

## FAQ

**Q: Conversion fails with "python3 not found"**  
A: Open Settings and set `xlsx2md.pythonPath` to your Python binary (e.g. `python` or an absolute path).

**Q: Images missing from Markdown**  
A: Ensure `openpyxl` and `Pillow` are installed. Run Command Palette → `xlsx2md: Install Python Dependencies`, or manually: `pip install openpyxl Pillow`

**Q: `@xlsx2md` doesn't appear in Copilot Chat**  
A: Ensure GitHub Copilot Chat extension is installed and VS Code ≥ 1.90.

**Q: Conversion timed out**  
A: For large files, increase `xlsx2md.conversionTimeout` (in seconds).

**Q: How to reinstall Python dependencies**  
A: Open Command Palette `Ctrl+Shift+P` → `xlsx2md: Install Python Dependencies`.
