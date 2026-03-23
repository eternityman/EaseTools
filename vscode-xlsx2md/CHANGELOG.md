# Change Log

All notable changes to **xlsx2md** are documented here.

## [0.1.0] — 2024-03-23

### Added
- Convert `.xlsx` files to Markdown tables via right-click context menu and Command Palette.
- Extract embedded images into an `images/` sub-directory alongside the `.md` output file.
- **Copilot Chat participant** (`@xlsx2md`) — attach an XLSX file and Copilot generates Markdown docs automatically.
- **Auto-dependency detection** — on activation the extension checks whether `openpyxl` and `Pillow` are installed; prompts to install if missing.
- New command `xlsx2md: Install Python Dependencies` to trigger pip install via the Command Palette.
- `xlsx2md.py` bundled inside the VSIX — no manual file-copy required after install.
- Settings: `xlsx2md.pythonPath`, `xlsx2md.scriptPath`, `xlsx2md.imageDir`, `xlsx2md.conversionTimeout`.
- CI workflow: automatic VSIX build on every push to `main`; automatic Marketplace publish on `v*.*.*` tags.
