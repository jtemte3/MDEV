# 🎉 MDEV v1.4 - Release Notes

## Initial Release

**Release Date:** [Insert Date]  
**Version:** 1.4.0  
**Platform:** Windows (Desktop Application)  
**License:** MIT

---

## 📝 Overview

We're excited to announce the first release of **MDEV (Markdown Editor/Viewer)** — a native desktop markdown editor and viewer built with Python and PyQt5. MDEV provides a seamless writing experience with real-time preview, syntax highlighting, and a clean, intuitive interface.

Whether you're writing documentation, creating README files, or composing markdown content, MDEV is designed to make the process smooth and efficient.

---

## ✨ What's New

### Core Features

#### 🖥️ Split-Pane Interface
- **Editor Pane**: Dark-themed text editor on the left with markdown syntax support
- **Preview Pane**: Live rendered markdown preview on the right with GitHub-flavored styling
- **Independent Toggling**: Show/hide editor or preview pane independently using toolbar buttons or keyboard shortcuts

#### 📖 Live Preview
- Real-time rendering of your markdown as you type
- Supports all standard markdown features plus extensions:
  - Fenced code blocks with syntax highlighting
  - Tables
  - Task lists
  - Table of contents
  - And more!

#### ✏️ Rich Editing Experience
- **Syntax Highlighting**: Dark theme editor with markdown syntax support
- **Toolbar**: Quick formatting buttons for common markdown elements:
  - **B** - Bold
  - **I** - Italic
  - **H** - Heading
  - 🔗 - Link
  - 🖼️ - Image
  - `<>` - Inline Code
  - `{ }` - Code Block
  - ❝ - Blockquote
  - ☰ - List
  - ▦ - Table
  - — - Horizontal Rule

#### 💾 Smart File Management
- **Auto-Save**: Automatically saves your work after 2 seconds of inactivity
  - Status bar shows "✓ Auto-saved: filename" when active
  - Silently saves when closing, opening, or creating new files
- **Manual Save**: Traditional save functionality with `Ctrl+S`
- **File Operations**: Open, save, and create new markdown files with ease

#### 🎨 Theme Support
- **Light Theme**: Clean, bright preview with GitHub-style rendering
- **Dark Theme**: Easy on the eyes with dark background and optimized colors
- **Toggle**: Switch between themes using the 🌙 button or `Ctrl+D`

#### 📊 Status Bar
- Real-time character count
- Word count tracking
- Line count display
- Auto-save status indicator (ON/OFF)

#### ⌨️ Keyboard Shortcuts

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

#### ⚙️ Settings Persistence
- Remembers your preferences between sessions
- Saves window position and size
- Remembers splitter positions
- Persists theme choices
- Tracks last opened directory

---

## 🛠️ Technical Details

### Built With
- **Python 3.7+** (Application runtime)
- **PyQt5** (GUI Framework)
- **PyQtWebEngine** (Markdown rendering engine)
- **Markdown** (Markdown processing library)
- **Pygments** (Syntax highlighting)

### Packaging
- Standalone Windows executable created with PyInstaller
- No Python installation required for end users
- Portable application with embedded dependencies

### System Requirements
- Windows 7 or later (32-bit or 64-bit)
- 2 GB RAM recommended
- Modern display with at least 1280x720 resolution

---

## 📦 Installation

### For End Users
1. Download `MDEV-v1.4.exe` from the releases page
2. Run the executable - no installation required!
3. Start writing markdown!

### For Developers
```bash
# Clone the repository
git clone https://github.com/your-username/MarkdownEditor.git

# Navigate to the project directory
cd MarkdownEditor/MDEV

# Install dependencies
pip install -r requirements.txt

# Run the application
python mdev.py
```

---

## 📚 Sample Content

A sample markdown file (`sample.md`) is included with the application, showcasing:
- Text formatting (bold, italic, strikethrough)
- Lists (ordered, unordered, task lists)
- Code blocks with syntax highlighting
- Tables
- Links and images
- Blockquotes
- And more!

Open it via **File → Open** to explore all supported markdown features.

---

## 🐛 Known Issues

- [Add any known issues here, or remove this section if none]

---

## 🔄 What's Next

We're planning the following features for upcoming releases:
- Export to PDF/HTML
- Multi-file support with tabs
- Custom theme editor
- Spell checking
- Plugin system
- Cross-platform support (macOS, Linux)

---

## 🙏 Acknowledgments

Special thanks to:
- The PyQt5 community for the excellent GUI framework
- The Python markdown library maintainers
- All contributors and early testers

---

## 📞 Support & Feedback

Have questions, suggestions, or found a bug? We'd love to hear from you!

- **GitHub Issues**: [Link to issue tracker]
- **Email**: [Your contact email]
- **Discussions**: [Link to discussions if applicable]

---

## 📜 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🎊 Thank You!

Thank you for trying MDEV! We hope it makes your markdown writing experience more enjoyable and productive. Happy writing! ✍️

---

*© 2024 MDEV Project. All rights reserved.*
