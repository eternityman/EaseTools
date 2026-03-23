#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
mcp-xlsx2md/server.py
~~~~~~~~~~~~~~~~~~~~~
MCP (Model Context Protocol) server that exposes xlsx2md as a Copilot tool.

When registered in VS Code, GitHub Copilot can call `convert_xlsx_to_markdown`
automatically whenever it needs to read an XLSX file.

Usage
-----
Start manually (for testing):
    python server.py

Register in VS Code (.vscode/mcp.json or user settings):
    See mcp.json.example in this directory.
"""

import os
import sys

# 将父目录的 xlsx2md 模块加入路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "xlsx2md"))

from mcp.server.fastmcp import FastMCP

from xlsx2md import xlsx_to_markdown_string

mcp = FastMCP(
    "xlsx2md",
    instructions=(
        "Use convert_xlsx_to_markdown to read an XLSX spreadsheet and get its "
        "full Markdown representation, including text, tables, and embedded images."
    ),
)


@mcp.tool()
def convert_xlsx_to_markdown(
    xlsx_path: str,
    image_dir: str = "images",
    sheet: str = "",
    no_images: bool = False,
) -> str:
    """
    Convert an XLSX spreadsheet to Markdown format.

    Extracts all sheets as Markdown tables and saves embedded images to the
    `image_dir` directory (relative to the XLSX file location). Image references
    in the returned Markdown use relative paths so they render correctly when the
    Markdown file is saved next to the XLSX.

    Args:
        xlsx_path: Absolute or workspace-relative path to the .xlsx file.
        image_dir: Sub-directory name for extracted images (default: "images").
        sheet: Only convert the named sheet; leave empty to convert all sheets.
        no_images: Set to true to skip image extraction (text only).

    Returns:
        The full Markdown content as a string.
    """
    abs_path = os.path.abspath(xlsx_path)
    return xlsx_to_markdown_string(
        input_path=abs_path,
        image_dir=image_dir,
        include_images=not no_images,
        sheet_filter=sheet if sheet else None,
    )


if __name__ == "__main__":
    mcp.run()
