// @ts-check
"use strict";

const vscode = require("vscode");
const path = require("path");
const cp = require("child_process");
const fs = require("fs");

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

/**
 * Resolve the path to xlsx2md.py.
 * Priority: user setting → bundled script next to this extension.
 * @returns {string}
 */
function resolveScriptPath() {
  const cfg = vscode.workspace.getConfiguration("xlsx2md");
  const custom = cfg.get("scriptPath", "");
  if (custom && fs.existsSync(custom)) {
    return custom;
  }
  // Bundled: the script lives at ../xlsx2md/xlsx2md.py relative to this file
  return path.join(__dirname, "..", "xlsx2md", "xlsx2md.py");
}

/**
 * Run xlsx2md.py on the given XLSX file and return the output path + content.
 * @param {string} xlsxPath Absolute path to the .xlsx file
 * @param {{noImages?: boolean, sheet?: string, imageDir?: string, outputPath?: string}} [options]
 * @returns {Promise<{outputPath: string, content: string}>}
 */
function runXlsx2md(xlsxPath, options = {}) {
  return new Promise((resolve, reject) => {
    const cfg = vscode.workspace.getConfiguration("xlsx2md");
    const python = cfg.get("pythonPath", "python3");
    const script = resolveScriptPath();
    const imageDir = options.imageDir || cfg.get("imageDir", "images");
    const timeoutMs = cfg.get("conversionTimeout", 120) * 1000;
    const outputPath =
      options.outputPath ||
      xlsxPath.replace(/\.xlsx$/i, ".md");

    const args = [script, xlsxPath, "-o", outputPath, "-i", imageDir];
    if (options.noImages) args.push("--no-images");
    if (options.sheet) args.push("--sheet", options.sheet);

    cp.execFile(python, args, { timeout: timeoutMs }, (err, _stdout, stderr) => {
      if (err) {
        reject(new Error(stderr || err.message));
        return;
      }
      try {
        const content = fs.readFileSync(outputPath, "utf8");
        resolve({ outputPath, content });
      } catch (readErr) {
        reject(readErr);
      }
    });
  });
}

/**
 * Show an error message that also includes install instructions.
 * @param {string} message
 */
function showConversionError(message) {
  vscode.window
    .showErrorMessage(
      `xlsx2md: ${message}`,
      "Show setup instructions"
    )
    .then((choice) => {
      if (choice === "Show setup instructions") {
        vscode.env.openExternal(
          vscode.Uri.parse(
            "https://github.com/eternityman/EaseTools/tree/main/vscode-xlsx2md#setup"
          )
        );
      }
    });
}

// ---------------------------------------------------------------------------
// Extension entry point
// ---------------------------------------------------------------------------

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
  // ── Command: Convert XLSX → Markdown (with images) ──────────────────────
  context.subscriptions.push(
    vscode.commands.registerCommand(
      "xlsx2md.convertFile",
      (uri) => convertCommand(uri, false)
    )
  );

  // ── Command: Convert XLSX → Markdown (text only) ────────────────────────
  context.subscriptions.push(
    vscode.commands.registerCommand(
      "xlsx2md.convertFileNoImages",
      (uri) => convertCommand(uri, true)
    )
  );

  // ── Copilot Chat Participant ─────────────────────────────────────────────
  if (vscode.chat) {
    const participant = vscode.chat.createChatParticipant(
      "xlsx2md",
      chatHandler
    );
    participant.iconPath = new vscode.ThemeIcon("table");
    context.subscriptions.push(participant);
  }
}

// ---------------------------------------------------------------------------
// Convert command implementation
// ---------------------------------------------------------------------------

/**
 * @param {vscode.Uri | undefined} uri
 * @param {boolean} noImages
 */
async function convertCommand(uri, noImages) {
  // Resolve XLSX URI
  if (!uri) {
    const active = vscode.window.activeTextEditor;
    if (active && /\.xlsx$/i.test(active.document.fileName)) {
      uri = active.document.uri;
    } else {
      const picked = await vscode.window.showOpenDialog({
        canSelectMany: false,
        filters: { "Excel Workbooks": ["xlsx"] },
        title: "Select an XLSX file to convert",
      });
      if (!picked || picked.length === 0) return;
      uri = picked[0];
    }
  }

  const xlsxPath = uri.fsPath;
  const label = path.basename(xlsxPath);

  await vscode.window.withProgress(
    {
      location: vscode.ProgressLocation.Notification,
      title: `Converting ${label} to Markdown…`,
      cancellable: false,
    },
    async () => {
      try {
        const { outputPath } = await runXlsx2md(xlsxPath, { noImages });
        const doc = await vscode.workspace.openTextDocument(outputPath);
        await vscode.window.showTextDocument(doc, { preview: false });
        vscode.window.showInformationMessage(
          `✅ xlsx2md: ${label} → ${path.basename(outputPath)}`
        );
      } catch (err) {
        showConversionError(/** @type {Error} */ (err).message);
      }
    }
  );
}

// ---------------------------------------------------------------------------
// Copilot Chat handler
// ---------------------------------------------------------------------------

/**
 * @param {vscode.ChatRequest} request
 * @param {vscode.ChatContext} _context
 * @param {vscode.ChatResponseStream} stream
 * @param {vscode.CancellationToken} _token
 */
async function chatHandler(request, _context, stream, _token) {
  // ── /help command ────────────────────────────────────────────────────────
  if (request.command === "help") {
    stream.markdown(
      "## xlsx2md — usage\n\n" +
        "**Attach an XLSX file** using the paperclip / `#file` picker:\n\n" +
        "```\n@xlsx2md #yourfile.xlsx\n```\n\n" +
        "Or mention the filename in your message:\n\n" +
        "```\n@xlsx2md convert report.xlsx to markdown\n```\n\n" +
        "**Available slash commands**\n\n" +
        "| Command | Description |\n" +
        "| --- | --- |\n" +
        "| `/convert` | Convert the referenced XLSX (default) |\n" +
        "| `/help` | Show this help |\n\n" +
        "**Tip:** Right-click any `.xlsx` file in the Explorer and choose " +
        "**Convert XLSX to Markdown** for a one-click conversion.\n"
    );
    return;
  }

  // ── Resolve XLSX file ────────────────────────────────────────────────────
  let xlsxUri = null;

  // 1. File references attached with #file
  for (const ref of request.references || []) {
    const val = ref.value;
    if (val instanceof vscode.Uri && /\.xlsx$/i.test(val.fsPath)) {
      xlsxUri = val;
      break;
    }
  }

  // 2. Path mentioned in the prompt text
  if (!xlsxUri) {
    const match = request.prompt.match(/["']?([^\s"'*?<>|]+\.xlsx)["']?/i);
    if (match) {
      // Normalise separators so path.resolve works on both Windows and POSIX
      const mentioned = match[1].replace(/\\/g, path.sep).replace(/\//g, path.sep);
      const workspaceFolders = vscode.workspace.workspaceFolders || [];
      for (const wf of workspaceFolders) {
        const candidate = path.resolve(wf.uri.fsPath, mentioned);
        if (fs.existsSync(candidate)) {
          xlsxUri = vscode.Uri.file(candidate);
          break;
        }
      }
      if (!xlsxUri && fs.existsSync(mentioned)) {
        xlsxUri = vscode.Uri.file(path.resolve(mentioned));
      }
    }
  }

  if (!xlsxUri) {
    stream.markdown(
      "❓ **No XLSX file found.**\n\n" +
        "Please attach the file using the **#file** picker or mention its name:\n\n" +
        "```\n@xlsx2md #yourfile.xlsx\n```\n\n" +
        "Type `@xlsx2md /help` for full usage instructions."
    );
    return;
  }

  // ── Convert ──────────────────────────────────────────────────────────────
  const xlsxPath = xlsxUri.fsPath;
  const baseName = path.basename(xlsxPath);

  stream.progress(`Converting ${baseName}…`);

  try {
    const noImages = /no.?image/i.test(request.prompt);
    const { outputPath, content } = await runXlsx2md(xlsxPath, { noImages });

    stream.markdown(
      `✅ **Converted** \`${baseName}\` → \`${path.basename(outputPath)}\`\n\n` +
        "---\n\n"
    );
    stream.markdown(content);
    stream.button({
      command: "vscode.open",
      arguments: [vscode.Uri.file(outputPath)],
      title: "📄 Open Markdown file",
    });
  } catch (err) {
    stream.markdown(
      `❌ **Conversion failed:** ${/** @type {Error} */ (err).message}\n\n` +
        "Make sure Python 3 and the required packages are installed:\n\n" +
        "```bash\npip install openpyxl Pillow\n```\n\n" +
        "Then check **Settings → xlsx2md.pythonPath** if Python is not on your `PATH`."
    );
  }
}

function deactivate() {}

module.exports = { activate, deactivate };
