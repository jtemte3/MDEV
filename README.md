# Markdown Editor

A native desktop markdown editor and viewer built with Python and PyQt5.

## Features

- ✅ **Live Preview** - See your markdown rendered in real-time
- ✅ **Syntax Highlighting** - Dark theme editor with markdown syntax support
- ✅ **Full Markdown Support** - Headings, lists, tables, code blocks, images, links, and more
- ✅ **Toolbar** - Quick formatting buttons for common markdown elements
- ✅ **File Management** - Open, save, and create new markdown files
- ✅ **Auto-Save** - Automatically saves your work after every edit (2 second delay)
- ✅ **Status Bar** - Character count, word count, and line count
- ✅ **Dark Theme Preview** - Toggle between light and dark preview themes
- ✅ **Independent Pane Toggling** - Show/hide editor or preview pane independently
- ✅ **Settings Persistence** - Remembers your preferences between sessions
- ✅ **Keyboard Shortcuts** - Common shortcuts for formatting and file operations

## Requirements

- Python 3.7 or higher
- PyQt5
- PyQtWebEngine (for markdown preview rendering)
- markdown
- Pygments

## Installation

1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python markdown_editor.py
   ```

## Sample File

A sample markdown file (`sample.md`) is included in the application directory showcasing all markdown features. Open it via **File → Open** to see:
- Text formatting (bold, italic, strikethrough)
- Lists (ordered, unordered, task lists)
- Code blocks with syntax highlighting
- Tables
- Links and images
- Blockquotes
- And more!

## Usage

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+B` | Bold |
| `Ctrl+I` | Italic |
| `Ctrl+K` | Insert Link |
| `Ctrl+Shift+K` | Inline Code |
| `Ctrl+Alt+S` | Auto-Save Now |
| `Ctrl+S` | Save File |
| `Ctrl+O` | Open File |
| `Ctrl+N` | New File |
| `Ctrl+P` | Toggle Preview Pane |
| `Ctrl+E` | Toggle Editor Pane |
| `Ctrl+D` | Toggle Dark Preview |
| `Tab` | Indent |

### Toolbar Buttons

- **B** - Bold
- **I** - Italic
- **H** - Heading
- **🔗** - Link
- **🖼️** - Image
- **<>** - Inline Code
- **{ }** - Code Block
- **❝** - Blockquote
- **☰** - List
- **▦** - Table
- **—** - Horizontal Rule
- **🌙** - Toggle Dark Preview (right side)
- **📝** - Toggle Editor Pane (right side)
- **👁️** - Toggle Preview Pane (right side)

### Auto-Save Behavior

**When Auto-save is ON** (file is open):
- Automatically saves after 2 seconds of inactivity
- Silently saves when closing, opening, or creating new files
- Status bar shows "✓ Auto-saved: filename"

**When Auto-save is OFF** (no file open):
- Shows save confirmation dialog when closing
- Shows save confirmation dialog when creating new file
- Shows save confirmation dialog when opening a file
- Status bar shows "Auto-save: OFF" in gray

### Status Bar Indicators

- **Characters**: Character count
- **Words**: Word count
- **Lines**: Line count
- **Auto-save**: Shows ON (green) when file is open, OFF (gray) when no file is open

## Markdown Features Supported

- Headings (H1-H6)
- Bold and italic text
- Strikethrough
- Links and images
- Ordered and unordered lists
- Code blocks with syntax highlighting
- Inline code
- Tables
- Blockquotes
- Horizontal rules
- Task lists
- And more!

## Screenshots

The application features a split-pane interface with:
- Left side: Editor with dark theme
- Right side: Live preview with GitHub-flavored markdown styling

## License

MIT License
