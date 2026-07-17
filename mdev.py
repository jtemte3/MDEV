"""
MDEV (MarkDown Editor/Viewer) - A native desktop markdown viewer and editor
Built with PyQt5 for proper HTML rendering and markdown support
"""

import sys
import os
import json
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QSplitter, QFileDialog, QMessageBox, QToolBar,
    QAction, QLabel, QStatusBar, QMenuBar, QMenu, QSizePolicy,
    QTreeView, QFileSystemModel, QHeaderView, QDockWidget, QDialog,
    QLineEdit, QPushButton, QFormLayout, QInputDialog
)
from PyQt5.QtCore import Qt, QUrl, QTimer, QSize, QDir
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtGui import QFont, QIcon, QColor, QTextCharFormat
import markdown
import pygments
from pygments.lexers import MarkdownLexer
from pygments.formatters import HtmlFormatter


class MarkdownSyntaxHighlighter:
    """Provides syntax highlighting for markdown text"""
    
    def __init__(self):
        self.lexer = MarkdownLexer()
        self.formatter = HtmlFormatter(style='default')
    
    def highlight(self, text):
        """Highlight markdown syntax and return colored HTML"""
        if not text:
            return "<span style='color: #666;'>Start typing...</span>"
        
        # Use Pygments to highlight markdown
        highlighted = pygments.highlight(text, self.lexer, self.formatter)
        return highlighted


class MarkdownEditorTextEdit(QTextEdit):
    """Custom text editor with markdown syntax highlighting"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFont(QFont('Consolas', 11))
        self.setPlaceholderText("Type your markdown here...")
        self.setLineWrapMode(QTextEdit.WidgetWidth)
        
        # Set up colors
        self.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                border: none;
                selection-background-color: #264f78;
            }
        """)
        
        # Syntax highlighter
        self.highlighter = MarkdownSyntaxHighlighter()
        self.document().contentsChanged.connect(self.update_syntax_highlighting)
        self.selectionChanged.connect(self.update_syntax_highlighting)
        
    def update_syntax_highlighting(self):
        """Update syntax highlighting when text changes"""
        text = self.toPlainText()
        # Simple syntax highlighting - highlight common markdown patterns
        self.apply_simple_highlighting(text)
    
    def apply_simple_highlighting(self, text):
        """Apply simple syntax highlighting based on markdown patterns"""
        # This is a simplified approach - for full highlighting we'd need
        # a more sophisticated highlighter
        pass
    
    def keyPressEvent(self, event):
        """Handle keyboard shortcuts"""
        # Tab key for indentation
        if event.key() == Qt.Key_Tab:
            self.insertPlainText("    ")
            return
        
        # Ctrl+B for bold
        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_B:
            self.wrap_selection("**", "**")
            return
        
        # Ctrl+I for italic
        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_I:
            self.wrap_selection("*", "*")
            return
        
        # Ctrl+K for link
        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_K:
            self.wrap_selection("[", "](url)")
            return
        
        # Ctrl+Shift+K for code
        if event.modifiers() == (Qt.ControlModifier | Qt.ShiftModifier) and event.key() == Qt.Key_K:
            self.wrap_selection("`", "`")
            return
        
        super().keyPressEvent(event)
    
    def wrap_selection(self, prefix, suffix):
        """Wrap selected text with prefix and suffix"""
        cursor = self.textCursor()
        selected = cursor.selectedText()
        
        if selected:
            cursor.insertText(prefix + selected + suffix)
        else:
            cursor.insertText(prefix + suffix)
            # Move cursor between the markers
            cursor.movePosition(cursor.Left, cursor.KeepAnchor, len(suffix))
            cursor.movePosition(cursor.Left)
            self.setTextCursor(cursor)


class MarkdownPreview(QWebEngineView):
    """Web view for rendering markdown preview"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.dark_mode = False
        self._scroll_position = 0  # Store scroll position to restore on next update
        self._restore_timer = QTimer(self)
        self._restore_timer.setSingleShot(True)
        self._restore_timer.timeout.connect(self._restore_scroll)
        self.loadFinished.connect(self._on_load_finished)
        # Monitor scroll position changes
        self.page().runJavaScript(
            '''
            (function() {
                window.addEventListener('scroll', function() {
                    window._mdevScrollPosition = window.scrollY || document.documentElement.scrollTop || document.body.scrollTop || 0;
                });
                window._mdevScrollPosition = 0;
            })()
            '''
        )
        self.setHtml(self.get_default_html())
        
    def toggle_dark_mode(self):
        """Toggle between light and dark theme"""
        self.dark_mode = not self.dark_mode
        # Update preview with current content
        markdown_text = self.parent().editor.toPlainText()
        self.update_preview(markdown_text)
        
    def get_default_html(self):
        """Return default HTML when no markdown is present"""
        if self.dark_mode:
            return self.get_dark_default_html()
        return self.get_light_default_html()
    
    def get_light_default_html(self):
        """Return light theme default HTML"""
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #ffffff;
                }
                h1, h2, h3, h4, h5, h6 {
                    color: #2c3e50;
                    margin-top: 24px;
                    margin-bottom: 16px;
                    font-weight: 600;
                }
                h1 { font-size: 2em; border-bottom: 1px solid #eaecef; padding-bottom: 0.3em; }
                h2 { font-size: 1.5em; border-bottom: 1px solid #eaecef; padding-bottom: 0.3em; }
                h3 { font-size: 1.25em; }
                p { margin-bottom: 16px; }
                code {
                    background-color: #f6f8fa;
                    padding: 0.2em 0.4em;
                    border-radius: 3px;
                    font-size: 85%;
                    color: #e83e8c;
                }
                pre {
                    background-color: #f6f8fa;
                    padding: 16px;
                    border-radius: 6px;
                    overflow: auto;
                    line-height: 1.45;
                }
                pre code {
                    background-color: transparent;
                    padding: 0;
                }
                blockquote {
                    border-left: 4px solid #dfe2e5;
                    padding-left: 16px;
                    color: #6a737d;
                    margin: 16px 0;
                }
                ul, ol {
                    padding-left: 2em;
                    margin-bottom: 16px;
                }
                li { margin-bottom: 4px; }
                table {
                    border-collapse: collapse;
                    width: 100%;
                    margin-bottom: 16px;
                }
                th, td {
                    border: 1px solid #dfe2e5;
                    padding: 6px 13px;
                }
                th { background-color: #f6f8fa; }
                a {
                    color: #0366d6;
                    text-decoration: none;
                }
                a:hover { text-decoration: underline; }
                img { max-width: 100%; }
                hr {
                    height: 2px;
                    padding: 0;
                    margin: 24px 0;
                    background-color: #eaecef;
                    border: 0;
                }
                .emoji { font-size: 1.2em; }
            </style>
        </head>
        <body>
            <div style="text-align: center; color: #999; margin-top: 50px;">
                <p>Markdown preview will appear here</p>
            </div>
        </body>
        </html>
        """
    
    def get_dark_default_html(self):
        """Return dark theme default HTML"""
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
                    line-height: 1.6;
                    color: #d4d4d4;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #1e1e1e;
                }
                h1, h2, h3, h4, h5, h6 {
                    color: #ffffff;
                    margin-top: 24px;
                    margin-bottom: 16px;
                    font-weight: 600;
                }
                h1 { font-size: 2em; border-bottom: 1px solid #404040; padding-bottom: 0.3em; }
                h2 { font-size: 1.5em; border-bottom: 1px solid #404040; padding-bottom: 0.3em; }
                h3 { font-size: 1.25em; }
                p { margin-bottom: 16px; }
                code {
                    background-color: #2d2d2d;
                    padding: 0.2em 0.4em;
                    border-radius: 3px;
                    font-size: 85%;
                    color: #9cdcfe;
                }
                pre {
                    background-color: #2d2d2d;
                    padding: 16px;
                    border-radius: 6px;
                    overflow: auto;
                    line-height: 1.45;
                }
                pre code {
                    background-color: transparent;
                    padding: 0;
                }
                blockquote {
                    border-left: 4px solid #404040;
                    padding-left: 16px;
                    color: #858585;
                    margin: 16px 0;
                }
                ul, ol {
                    padding-left: 2em;
                    margin-bottom: 16px;
                }
                li { margin-bottom: 4px; }
                table {
                    border-collapse: collapse;
                    width: 100%;
                    margin-bottom: 16px;
                }
                th, td {
                    border: 1px solid #404040;
                    padding: 6px 13px;
                }
                th { background-color: #2d2d2d; }
                a {
                    color: #3794ff;
                    text-decoration: none;
                }
                a:hover { text-decoration: underline; }
                img { max-width: 100%; }
                hr {
                    height: 2px;
                    padding: 0;
                    margin: 24px 0;
                    background-color: #404040;
                    border: 0;
                }
                .emoji { font-size: 1.2em; }
            </style>
        </head>
        <body>
            <div style="text-align: center; color: #858585; margin-top: 50px;">
                <p>Markdown preview will appear here</p>
            </div>
        </body>
        </html>
        """
    
    def update_preview(self, markdown_text):
        """Update the preview with rendered markdown"""
        # Read the current scroll position from JavaScript before updating
        self.page().runJavaScript(
            'window._mdevScrollPosition || 0',
            self._update_scroll_position
        )
        
        if not markdown_text.strip():
            self.setHtml(self.get_default_html())
            return
        
        # Convert markdown to HTML with extensions
        html_content = markdown.markdown(
            markdown_text,
            extensions=[
                'fenced_code',      # Code blocks with ```
                'codehilite',       # Syntax highlighting for code
                'tables',           # Tables
                'toc',              # Table of contents
                'nl2br',            # New lines to breaks
                'sane_lists',       # Better list handling
                'attr_list',        # Attribute lists
                'md_in_html',       # Markdown in HTML
            ]
        )
        
        # Choose theme based on dark_mode setting
        if self.dark_mode:
            full_html = self.get_dark_theme_html(html_content)
        else:
            full_html = self.get_light_theme_html(html_content)
        
        self.setHtml(full_html)
    
    def _on_load_finished(self, success):
        """Called when the page finishes loading"""
        if success:
            # Re-inject scroll tracking script
            self.page().runJavaScript(
                '''
                (function() {
                    window.addEventListener('scroll', function() {
                        window._mdevScrollPosition = window.scrollY || document.documentElement.scrollTop || document.body.scrollTop || 0;
                    });
                    if (typeof window._mdevScrollPosition === 'undefined') {
                        window._mdevScrollPosition = 0;
                    }
                })()
                '''
            )
            # Delay restoration slightly to ensure page is fully rendered
            self._restore_timer.start(50)
    
    def _restore_scroll(self):
        """Restore the scroll position after a brief delay"""
        if hasattr(self, '_scroll_position') and self._scroll_position > 0:
            self.page().runJavaScript(
                f'window.scrollTo(0, {self._scroll_position});'
            )
    
    def _update_scroll_position(self, result):
        """Update stored scroll position"""
        if result is not None:
            self._scroll_position = result
    
    def get_light_theme_html(self, content):
        """Return light themed HTML"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #ffffff;
                }}
                h1, h2, h3, h4, h5, h6 {{
                    color: #2c3e50;
                    margin-top: 24px;
                    margin-bottom: 16px;
                    font-weight: 600;
                }}
                h1 {{ font-size: 2em; border-bottom: 1px solid #eaecef; padding-bottom: 0.3em; }}
                h2 {{ font-size: 1.5em; border-bottom: 1px solid #eaecef; padding-bottom: 0.3em; }}
                h3 {{ font-size: 1.25em; }}
                p {{ margin-bottom: 16px; }}
                code {{
                    background-color: #f6f8fa;
                    padding: 0.2em 0.4em;
                    border-radius: 3px;
                    font-size: 85%;
                    color: #e83e8c;
                }}
                pre {{
                    background-color: #f6f8fa;
                    padding: 16px;
                    border-radius: 6px;
                    overflow: auto;
                    line-height: 1.45;
                }}
                pre code {{
                    background-color: transparent;
                    padding: 0;
                }}
                blockquote {{
                    border-left: 4px solid #dfe2e5;
                    padding-left: 16px;
                    color: #6a737d;
                    margin: 16px 0;
                }}
                ul, ol {{
                    padding-left: 2em;
                    margin-bottom: 16px;
                }}
                li {{ margin-bottom: 4px; }}
                table {{
                    border-collapse: collapse;
                    width: 100%;
                    margin-bottom: 16px;
                }}
                th, td {{
                    border: 1px solid #dfe2e5;
                    padding: 6px 13px;
                }}
                th {{ background-color: #f6f8fa; }}
                a {{
                    color: #0366d6;
                    text-decoration: none;
                }}
                a:hover {{ text-decoration: underline; }}
                img {{ max-width: 100%; }}
                hr {{
                    height: 2px;
                    padding: 0;
                    margin: 24px 0;
                    background-color: #eaecef;
                    border: 0;
                }}
                .emoji {{ font-size: 1.2em; }}
                /* Task lists */
                input[type="checkbox"] {{
                    margin-right: 8px;
                }}
            </style>
        </head>
        <body>
            {content}
        </body>
        </html>
        """
    
    def get_dark_theme_html(self, content):
        """Return dark themed HTML"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
                    line-height: 1.6;
                    color: #d4d4d4;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #1e1e1e;
                }}
                h1, h2, h3, h4, h5, h6 {{
                    color: #ffffff;
                    margin-top: 24px;
                    margin-bottom: 16px;
                    font-weight: 600;
                }}
                h1 {{ font-size: 2em; border-bottom: 1px solid #404040; padding-bottom: 0.3em; }}
                h2 {{ font-size: 1.5em; border-bottom: 1px solid #404040; padding-bottom: 0.3em; }}
                h3 {{ font-size: 1.25em; }}
                p {{ margin-bottom: 16px; }}
                code {{
                    background-color: #2d2d2d;
                    padding: 0.2em 0.4em;
                    border-radius: 3px;
                    font-size: 85%;
                    color: #9cdcfe;
                }}
                pre {{
                    background-color: #2d2d2d;
                    padding: 16px;
                    border-radius: 6px;
                    overflow: auto;
                    line-height: 1.45;
                }}
                pre code {{
                    background-color: transparent;
                    padding: 0;
                }}
                blockquote {{
                    border-left: 4px solid #404040;
                    padding-left: 16px;
                    color: #858585;
                    margin: 16px 0;
                }}
                ul, ol {{
                    padding-left: 2em;
                    margin-bottom: 16px;
                }}
                li {{ margin-bottom: 4px; }}
                table {{
                    border-collapse: collapse;
                    width: 100%;
                    margin-bottom: 16px;
                }}
                th, td {{
                    border: 1px solid #404040;
                    padding: 6px 13px;
                }}
                th {{ background-color: #2d2d2d; }}
                a {{
                    color: #3794ff;
                    text-decoration: none;
                }}
                a:hover {{ text-decoration: underline; }}
                img {{ max-width: 100%; }}
                hr {{
                    height: 2px;
                    padding: 0;
                    margin: 24px 0;
                    background-color: #404040;
                    border: 0;
                }}
                .emoji {{ font-size: 1.2em; }}
                /* Task lists */
                input[type="checkbox"] {{
                    margin-right: 8px;
                }}
            </style>
        </head>
        <body>
            {content}
        </body>
        </html>
        """


class SettingsManager:
    """Manages application settings persistence"""
    
    def __init__(self):
        # Use a settings file in the same directory as the script
        self.settings_file = os.path.join(os.path.dirname(__file__), 'settings.json')
        self.settings = self.load_settings()
    
    def load_settings(self):
        """Load settings from file, return defaults if not found"""
        default_settings = {
            'dark_mode': False,
            'app_theme': 'dark',  # 'dark' or 'light' - controls all panels except preview
            'editor_visible': True,
            'preview_visible': True,
            'window_width': 1200,
            'window_height': 800,
            'window_x': 100,
            'window_y': 100,
            'splitter_sizes': [600, 600],
            'explorer_splitter_sizes': [250, 1100],
            'last_directory': None
        }
        
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    loaded_settings = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    default_settings.update(loaded_settings)
            except (json.JSONDecodeError, IOError):
                pass
        
        return default_settings
    
    def save_settings(self):
        """Save settings to file"""
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=4)
        except IOError as e:
            print(f"Warning: Could not save settings: {e}")
    
    def get(self, key, default=None):
        """Get a setting value"""
        return self.settings.get(key, default)
    
    def set(self, key, value):
        """Set a setting value"""
        self.settings[key] = value


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.current_file = None
        self.current_directory = None
        self.settings = SettingsManager()
        
        # Auto-save timer (must be created before init_ui)
        self.auto_save_timer = QTimer(self)
        self.auto_save_timer.setSingleShot(True)
        self.auto_save_timer.timeout.connect(self.auto_save)
        self.auto_save_delay = 2000  # 2 seconds delay
        
        self.init_ui()
        self.apply_saved_settings()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle('MDEV (MarkDown Editor/Viewer)')
        self.setGeometry(100, 100, 1200, 800)
        
        # Set application icon
        # Determine the base path for resources (handles both script and .exe environments)
        base_path = sys._MEIPASS if hasattr(sys, '_MEIPASS') else os.path.abspath(".")
        icon_path = os.path.join(base_path, "Mdev-icon.png")
        
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout with horizontal split for activity bar and explorer
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create project explorer panel (this creates the activity bar)
        self.create_project_explorer()
        
        # Add activity bar to the left
        main_layout.addWidget(self.activity_bar)
        
        # Create splitter for project explorer and main content
        self.explorer_splitter = QSplitter(Qt.Horizontal)
        self.explorer_splitter.setHandleWidth(4)
        self.explorer_splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: #444444;
            }
            QSplitter::handle:hover {
                background-color: #007acc;
            }
        """)
        
        # Connect splitter moved signal to save explorer width (debounced)
        self.explorer_splitter.splitterMoved.connect(self.on_explorer_splitter_moved)
        
        # Add project explorer panel to splitter (hidden by default)
        self.explorer_splitter.addWidget(self.project_explorer_panel)
        
        # Create inner container for toolbar and splitter
        inner_container = QWidget()
        inner_layout = QVBoxLayout(inner_container)
        inner_layout.setContentsMargins(0, 0, 0, 0)
        inner_layout.setSpacing(0)
        
        # Create toolbar
        self.create_toolbar()
        inner_layout.addWidget(self.toolbar)
        
        # Create splitter for editor and preview
        splitter = QSplitter(Qt.Horizontal)
        self.splitter = splitter  # Store reference for saving sizes
        
        # Editor pane
        self.editor = MarkdownEditorTextEdit()
        self.editor.document().contentsChanged.connect(self.on_editor_changed)
        self.editor.setContextMenuPolicy(Qt.CustomContextMenu)
        self.editor.customContextMenuRequested.connect(self.show_editor_context_menu)
        
        # Preview pane
        self.preview = MarkdownPreview()
        self.preview.setContextMenuPolicy(Qt.CustomContextMenu)
        self.preview.customContextMenuRequested.connect(self.show_preview_context_menu)
        
        # Add to splitter
        splitter.addWidget(self.editor)
        splitter.addWidget(self.preview)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 1)
        splitter.setSizes([600, 600])
        
        inner_layout.addWidget(splitter)
        
        # Add inner container to explorer splitter
        self.explorer_splitter.addWidget(inner_container)
        
        # Add explorer splitter to main layout
        main_layout.addWidget(self.explorer_splitter)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage('Ready')
        
        # Character count label
        self.char_count = QLabel('Characters: 0')
        self.status_bar.addPermanentWidget(self.char_count)
        
        # Word count label
        self.word_count = QLabel('Words: 0')
        self.status_bar.addPermanentWidget(self.word_count)
        
        # Line count label
        self.line_count = QLabel('Lines: 1')
        self.status_bar.addPermanentWidget(self.line_count)
        
        # Auto-save status label
        self.auto_save_label = QLabel('Auto-save: OFF')
        self.auto_save_label.setStyleSheet('color: #999; font-weight: bold;')
        self.status_bar.addPermanentWidget(self.auto_save_label)
        
        # Create menu bar
        self.create_menu_bar()
    
    def apply_saved_settings(self):
        """Apply saved settings from previous session"""
        # Apply app theme setting (all panels except preview)
        app_theme = self.settings.get('app_theme', 'dark')
        self.apply_app_theme(app_theme)
        self.theme_toggle_action.setChecked(app_theme == 'dark')
        
        # Apply dark mode setting (preview only)
        dark_mode = self.settings.get('dark_mode', False)
        self.preview.dark_mode = dark_mode
        self.dark_mode_action.setChecked(dark_mode)
        
        # Apply pane visibility settings
        editor_visible = self.settings.get('editor_visible', True)
        preview_visible = self.settings.get('preview_visible', True)
        
        # Ensure at least one pane is visible
        if not editor_visible and not preview_visible:
            editor_visible = True
            preview_visible = True
        
        self.editor.setVisible(editor_visible)
        self.preview.setVisible(preview_visible)
        self.toggle_editor_action.setChecked(editor_visible)
        self.toggle_preview_pane_action.setChecked(preview_visible)
        
        # Apply window geometry
        window_width = self.settings.get('window_width', 1200)
        window_height = self.settings.get('window_height', 800)
        window_x = self.settings.get('window_x', 100)
        window_y = self.settings.get('window_y', 100)
        self.setGeometry(window_x, window_y, window_width, window_height)
        
        # Apply splitter sizes
        splitter_sizes = self.settings.get('splitter_sizes', [600, 600])
        if len(splitter_sizes) == 2:
            self.splitter.setSizes(splitter_sizes)
        
        # Apply explorer splitter sizes (project explorer width)
        explorer_splitter_sizes = self.settings.get('explorer_splitter_sizes', [250, 1100])
        if len(explorer_splitter_sizes) == 2:
            self.explorer_splitter.setSizes(explorer_splitter_sizes)
        
        # Load last opened directory
        last_directory = self.settings.get('last_directory', None)
        if last_directory and os.path.isdir(last_directory):
            self.current_directory = last_directory
            self.file_model.setRootPath(last_directory)
            self.file_tree.setRootIndex(self.file_model.index(last_directory))
            self.project_explorer_panel.show()
            self.project_explorer_panel.raise_()
            self.toggle_project_explorer_action.setChecked(True)
            self.explorer_toggle_btn.setChecked(True)
            self.status_bar.showMessage(f'Restored directory: {last_directory}')
        
        # Update preview with dark mode applied
        self.update_preview()
    
    def create_project_explorer(self):
        """Create the project explorer panel with VS Code-style vertical sidebar"""
        # Create vertical sidebar on the left edge
        self.activity_bar = QWidget()
        self.activity_bar.setFixedWidth(48)
        self.activity_bar.setStyleSheet("""
            QWidget {
                background-color: #333333;
                border-right: 1px solid #444444;
            }
        """)
        activity_layout = QVBoxLayout(self.activity_bar)
        activity_layout.setContentsMargins(0, 0, 0, 0)
        activity_layout.setSpacing(0)
        
        # Project Explorer button at the top
        self.explorer_toggle_btn = QPushButton('📁')
        self.explorer_toggle_btn.setFixedSize(48, 48)
        self.explorer_toggle_btn.setToolTip('Project Explorer')
        self.explorer_toggle_btn.setCheckable(True)
        self.explorer_toggle_btn.setChecked(False)
        self.explorer_toggle_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                color: #858585;
                font-size: 20px;
            }
            QPushButton:hover {
                color: #ffffff;
                background-color: #444444;
            }
            QPushButton:checked {
                color: #ffffff;
                border-left: 2px solid #007acc;
                background-color: #3c3c3c;
            }
        """)
        self.explorer_toggle_btn.clicked.connect(self.toggle_project_explorer)
        activity_layout.addWidget(self.explorer_toggle_btn)
        activity_layout.addStretch()
        
        # Create project explorer panel (not a dock widget)
        self.project_explorer_panel = QWidget()
        self.project_explorer_panel.setMinimumWidth(200)
        self.project_explorer_panel.setMaximumWidth(500)
        self.project_explorer_panel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.project_explorer_panel.setStyleSheet("""
            QWidget {
                background-color: #252526;
                border-right: 1px solid #444444;
            }
        """)
        explorer_layout = QVBoxLayout(self.project_explorer_panel)
        explorer_layout.setContentsMargins(0, 0, 0, 0)
        explorer_layout.setSpacing(0)
        
        # Create toolbar for project explorer
        self.explorer_toolbar = QToolBar('Explorer', self)
        self.explorer_toolbar.setMovable(False)
        self.explorer_toolbar.setIconSize(QSize(16, 16))
        self.explorer_toolbar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.explorer_toolbar.setStyleSheet("""
            QToolBar {
                spacing: 4px;
                padding: 8px 4px;
                background-color: #252526;
                border-bottom: 1px solid #444444;
            }
            QToolBar QToolButton {
                background: transparent;
                border: none;
                color: #cccccc;
                padding: 4px 8px;
            }
            QToolBar QToolButton:hover {
                background-color: #444444;
            }
        """)
        
        # Open Directory action
        open_dir_action = QAction('📂', self)
        open_dir_action.setToolTip('Open a directory in the explorer')
        open_dir_action.triggered.connect(self.open_directory)
        self.explorer_toolbar.addAction(open_dir_action)
        
        # New File action
        new_file_action = QAction('📄', self)
        new_file_action.setToolTip('Create a new file in the current directory')
        new_file_action.triggered.connect(self.on_toolbar_new_file)
        self.explorer_toolbar.addAction(new_file_action)
        
        # New Folder action
        new_folder_action = QAction('📁', self)
        new_folder_action.setToolTip('Create a new folder in the current directory')
        new_folder_action.triggered.connect(self.on_toolbar_new_folder)
        self.explorer_toolbar.addAction(new_folder_action)
        
        # Find Current File action
        find_file_action = QAction('🔍', self)
        find_file_action.setToolTip('Locate the currently opened file in the tree')
        find_file_action.triggered.connect(self.find_current_file_in_tree)
        self.explorer_toolbar.addAction(find_file_action)
        
        # Rename action
        rename_action = QAction('✏️', self)
        rename_action.setToolTip('Rename selected file or folder')
        rename_action.triggered.connect(self.rename_selected_item)
        self.explorer_toolbar.addAction(rename_action)
        
        # Delete action
        delete_action = QAction('🗑️', self)
        delete_action.setToolTip('Delete selected file or folder')
        delete_action.triggered.connect(self.delete_selected_item)
        self.explorer_toolbar.addAction(delete_action)
        
        # Create tree view
        self.file_tree = QTreeView()
        self.file_model = QFileSystemModel(self)
        self.file_model.setFilter(QDir.AllEntries | QDir.NoDotAndDotDot)
        
        self.file_tree.setModel(self.file_model)
        self.file_tree.setHeaderHidden(True)
        self.file_tree.setAnimated(True)
        self.file_tree.setIndentation(20)
        self.file_tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.file_tree.customContextMenuRequested.connect(self.show_context_menu)
        self.file_tree.setStyleSheet("""
            QTreeView {
                background-color: #1e1e1e;
                color: #cccccc;
                border: none;
                selection-background-color: #094771;
                selection-color: #ffffff;
            }
            QTreeView::item {
                padding: 4px;
            }
            QTreeView::item:hover {
                background-color: #2a2d2e;
            }
        """)
        
        # Show only the first column (file names)
        self.file_tree.setColumnHidden(1, True)  # Size
        self.file_tree.setColumnHidden(2, True)  # Type
        self.file_tree.setColumnHidden(3, True)  # Date Modified
        
        # Expand to 2 levels by default
        self.file_tree.expandToDepth(2)
        
        # Connect double-click to open file
        self.file_tree.doubleClicked.connect(self.on_file_double_clicked)
        
        # Add toolbar and tree view to layout
        explorer_layout.addWidget(self.explorer_toolbar)
        explorer_layout.addWidget(self.file_tree)
        
        # Hide by default
        self.project_explorer_panel.hide()
    
    def on_file_double_clicked(self, index):
        """Handle double-click on a file in the project explorer"""
        file_path = self.file_model.fileInfo(index).absoluteFilePath()
        
        # Only open files, not directories
        if os.path.isfile(file_path):
            # Auto-save current file if there are changes
            if self.current_file and self.editor.document().isModified():
                try:
                    content = self.editor.toPlainText()
                    with open(self.current_file, 'w', encoding='utf-8') as f:
                        f.write(content)
                    self.editor.document().setModified(False)
                except Exception as e:
                    QMessageBox.critical(self, 'Error', f'Could not auto-save file:\n{str(e)}')
                    return
            
            # Open the selected file
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Block signals to prevent triggering auto-save during load
                self.editor.blockSignals(True)
                self.editor.setPlainText(content)
                self.editor.blockSignals(False)
                
                # Mark document as not modified after loading
                self.editor.document().setModified(False)
                
                self.current_file = file_path
                self.current_directory = os.path.dirname(file_path)
                self.setWindowTitle(f'MDEV (MarkDown Editor/Viewer) - {os.path.basename(file_path)}')
                self.status_bar.showMessage(f'Opened: {file_path}')
                self.update_auto_save_status()
                self.update_preview()
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Could not open file:\n{str(e)}')
    
    def open_directory(self):
        """Open a directory in the project explorer"""
        directory = QFileDialog.getExistingDirectory(
            self,
            'Open Directory',
            '',
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        )
        
        if directory:
            self.current_directory = directory
            self.file_model.setRootPath(directory)
            self.file_tree.setRootIndex(self.file_model.index(directory))
            self.project_explorer_panel.show()
            self.project_explorer_panel.raise_()
            self.toggle_project_explorer_action.setChecked(True)
            self.explorer_toggle_btn.setChecked(True)
            self.status_bar.showMessage(f'Opened directory: {directory}')
            # Save the last opened directory
            self.settings.set('last_directory', directory)
            self.settings.save_settings()
    
    def new_file_in_directory(self, target_directory=None):
        """Create a new file in the specified directory or current directory"""
        if target_directory is None:
            target_directory = self.get_target_directory_for_new_item()
        
        if not target_directory:
            QMessageBox.information(self, 'No Directory Open', 'Please open a directory first using File → Open Directory')
            return
        
        file_name, ok = QInputDialog.getText(self, 'New File', 'Enter file name:', text='untitled.md')
        
        if ok and file_name:
            # Ensure .md extension
            if not file_name.endswith('.md') and not file_name.endswith('.markdown'):
                file_name += '.md'
            
            file_path = os.path.join(target_directory, file_name)
            
            try:
                # Create the file
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write('')
                
                # Refresh the file model
                self.file_model.setRootPath(self.current_directory)
                
                # Open the new file
                self.current_file = file_path
                self.editor.clear()
                self.editor.document().setModified(False)
                self.setWindowTitle(f'MDEV (MarkDown Editor/Viewer) - {file_name}')
                self.status_bar.showMessage(f'Created new file: {file_name}')
                self.update_auto_save_status()
                
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Could not create file:\n{str(e)}')
    
    def new_folder_in_directory(self, target_directory=None):
        """Create a new folder in the specified directory or current directory"""
        if target_directory is None:
            target_directory = self.get_target_directory_for_new_item()
        
        if not target_directory:
            QMessageBox.information(self, 'No Directory Open', 'Please open a directory first using File → Open Directory')
            return
        
        folder_name, ok = QInputDialog.getText(self, 'New Folder', 'Enter folder name:')
        
        if ok and folder_name:
            folder_path = os.path.join(target_directory, folder_name)
            
            try:
                # Create the folder
                os.makedirs(folder_path, exist_ok=True)
                
                # Refresh the file model
                self.file_model.setRootPath(self.current_directory)
                
                self.status_bar.showMessage(f'Created folder: {folder_name}')
                
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Could not create folder:\n{str(e)}')
    
    def get_target_directory_for_new_item(self):
        """Get the target directory for creating new items based on selection"""
        if not self.current_directory:
            return None
        
        # Try to get the selected index - use selectedIndexes() for better reliability
        # when the tree doesn't have focus (e.g., when clicking toolbar buttons)
        selected_indexes = self.file_tree.selectedIndexes()
        
        if selected_indexes:
            selected_index = selected_indexes[0]  # Use first selected column
            file_path = self.file_model.fileInfo(selected_index).absoluteFilePath()
            if file_path:
                # If it's a directory, create inside it
                if os.path.isdir(file_path):
                    return file_path
                # If it's a file, create in its parent directory (sibling)
                return os.path.dirname(file_path)
        
        # Fallback to currentIndex if no selection
        selected_index = self.file_tree.currentIndex()
        if selected_index.isValid():
            file_path = self.file_model.fileInfo(selected_index).absoluteFilePath()
            if file_path:
                if os.path.isdir(file_path):
                    return file_path
                return os.path.dirname(file_path)
        
        # Fall back to current_directory (root)
        return self.current_directory
    
    def on_toolbar_new_file(self):
        """Handler for toolbar New File button - calculates target directory like context menu"""
        if not self.current_directory:
            QMessageBox.information(self, 'No Directory Open', 'Please open a directory first using File → Open Directory')
            return
        
        # Get current index (same logic as context menu)
        index = self.file_tree.currentIndex()
        if not index.isValid():
            root_index = self.file_model.index(self.current_directory)
            self.file_tree.setCurrentIndex(root_index)
            index = root_index
        
        # Get the file path and determine if it's a directory
        file_path = self.file_model.fileInfo(index).absoluteFilePath()
        is_directory = os.path.isdir(file_path) if file_path else False
        
        # Calculate target directory (same logic as context menu lambda)
        target_directory = file_path if is_directory else os.path.dirname(file_path) if file_path else self.current_directory
        
        # Call the new file method with calculated target
        self.new_file_in_directory(target_directory)
    
    def on_toolbar_new_folder(self):
        """Handler for toolbar New Folder button - calculates target directory like context menu"""
        if not self.current_directory:
            QMessageBox.information(self, 'No Directory Open', 'Please open a directory first using File → Open Directory')
            return
        
        # Get current index (same logic as context menu)
        index = self.file_tree.currentIndex()
        if not index.isValid():
            root_index = self.file_model.index(self.current_directory)
            self.file_tree.setCurrentIndex(root_index)
            index = root_index
        
        # Get the file path and determine if it's a directory
        file_path = self.file_model.fileInfo(index).absoluteFilePath()
        is_directory = os.path.isdir(file_path) if file_path else False
        
        # Calculate target directory (same logic as context menu lambda)
        target_directory = file_path if is_directory else os.path.dirname(file_path) if file_path else self.current_directory
        
        # Call the new folder method with calculated target
        self.new_folder_in_directory(target_directory)
    
    def show_context_menu(self, position):
        """Show context menu for the project explorer tree"""
        if not self.current_directory:
            return
        
        # Get the index at the clicked position
        index = self.file_tree.indexAt(position)
        
        # If no valid index, select the root
        if not index.isValid():
            root_index = self.file_model.index(self.current_directory)
            self.file_tree.setCurrentIndex(root_index)
            index = root_index
        else:
            # Set the clicked item as current
            self.file_tree.setCurrentIndex(index)
        
        # Get the file path
        file_path = self.file_model.fileInfo(index).absoluteFilePath()
        
        # Determine if it's a directory
        is_directory = os.path.isdir(file_path) if file_path else False
        
        # Create context menu with theme-appropriate styling
        context_menu = QMenu(self)
        self.apply_context_menu_style(context_menu)
        
        # New File action
        new_file_action = QAction('📄 New File', self)
        new_file_action.triggered.connect(lambda: self.new_file_in_directory(file_path if is_directory else os.path.dirname(file_path) if file_path else self.current_directory))
        context_menu.addAction(new_file_action)
        
        # New Folder action
        new_folder_action = QAction('📁 New Folder', self)
        new_folder_action.triggered.connect(lambda: self.new_folder_in_directory(file_path if is_directory else os.path.dirname(file_path) if file_path else self.current_directory))
        context_menu.addAction(new_folder_action)
        
        context_menu.addSeparator()
        
        # Rename action
        rename_action = QAction('✏️ Rename', self)
        rename_action.triggered.connect(self.rename_selected_item)
        context_menu.addAction(rename_action)
        
        # Delete action
        delete_action = QAction('🗑️ Delete', self)
        delete_action.triggered.connect(self.delete_selected_item)
        context_menu.addAction(delete_action)
        
        # Show the menu at the cursor position
        context_menu.exec_(self.file_tree.viewport().mapToGlobal(position))
    
    def rename_selected_item(self):
        """Rename the selected file or folder in the project explorer"""
        # Get the currently selected index
        selected_index = self.file_tree.currentIndex()
        
        if not selected_index.isValid():
            QMessageBox.information(self, 'No Selection', 'Please select a file or folder to rename.')
            return
        
        # Get the file path
        file_path = self.file_model.fileInfo(selected_index).absoluteFilePath()
        
        if not file_path:
            QMessageBox.warning(self, 'Error', 'Could not get the selected item path.')
            return
        
        # Get the current name
        current_name = os.path.basename(file_path)
        
        # Prompt for new name
        new_name, ok = QInputDialog.getText(self, 'Rename', 'Enter new name:', text=current_name)
        
        if ok and new_name and new_name != current_name:
            # Get the parent directory
            parent_dir = os.path.dirname(file_path)
            new_path = os.path.join(parent_dir, new_name)
            
            try:
                # Check if new name already exists
                if os.path.exists(new_path):
                    QMessageBox.warning(self, 'Error', f'A file or folder with the name "{new_name}" already exists.')
                    return
                
                # Rename the file/folder
                os.rename(file_path, new_path)
                
                # Refresh the file model
                self.file_model.setRootPath(self.current_directory)
                
                # Update current file if it was renamed
                if self.current_file == file_path:
                    self.current_file = new_path
                    self.setWindowTitle(f'MDEV (MarkDown Editor/Viewer) - {new_name}')
                
                self.status_bar.showMessage(f'Renamed to: {new_name}')
                
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Could not rename:\n{str(e)}')
    
    def delete_selected_item(self):
        """Delete the selected file or folder in the project explorer"""
        # Get the currently selected index
        selected_index = self.file_tree.currentIndex()
        
        if not selected_index.isValid():
            QMessageBox.information(self, 'No Selection', 'Please select a file or folder to delete.')
            return
        
        # Get the file path
        file_path = self.file_model.fileInfo(selected_index).absoluteFilePath()
        
        if not file_path:
            QMessageBox.warning(self, 'Error', 'Could not get the selected item path.')
            return
        
        # Get the name
        item_name = os.path.basename(file_path)
        
        # Determine if it's a file or directory
        is_directory = os.path.isdir(file_path)
        item_type = 'folder' if is_directory else 'file'
        
        # Confirm deletion
        reply = QMessageBox.question(
            self, 
            'Confirm Delete', 
            f'Are you sure you want to delete the {item_type} "{item_name}"?\n\nThis action cannot be undone.',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                # Delete the file/folder
                if is_directory:
                    import shutil
                    shutil.rmtree(file_path)
                else:
                    os.remove(file_path)
                
                # Refresh the file model
                self.file_model.setRootPath(self.current_directory)
                
                # Clear current file if it was deleted
                if self.current_file == file_path:
                    self.current_file = None
                    self.editor.clear()
                    self.editor.document().setModified(False)
                    self.setWindowTitle('MDEV (MarkDown Editor/Viewer)')
                
                self.status_bar.showMessage(f'Deleted: {item_name}')
                
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Could not delete:\n{str(e)}')
    
    def find_current_file_in_tree(self):
        """Find and select the currently opened file in the project explorer tree"""
        if not self.current_file:
            QMessageBox.information(self, 'No File Open', 'No file is currently open.')
            return
        
        if not self.current_directory:
            QMessageBox.information(self, 'No Directory Open', 'No directory is currently open in the explorer.')
            return
        
        # Get the index for the current file
        file_index = self.file_model.index(self.current_file)
        
        if not file_index.isValid():
            QMessageBox.warning(self, 'File Not Found', 'The current file is not in the opened directory.')
            return
        
        # Expand all parent directories
        parent = file_index.parent()
        while parent.isValid():
            self.file_tree.expand(parent)
            parent = parent.parent()
        
        # Set the file as the current index and scroll to it
        self.file_tree.setCurrentIndex(file_index)
        self.file_tree.scrollTo(file_index)
        
        self.status_bar.showMessage(f'Located: {os.path.basename(self.current_file)}')
    
    def toggle_project_explorer(self):
        """Toggle the project explorer panel visibility"""
        if self.project_explorer_panel.isVisible():
            self.project_explorer_panel.hide()
            self.toggle_project_explorer_action.setChecked(False)
            self.explorer_toggle_btn.setChecked(False)
        else:
            self.project_explorer_panel.show()
            self.project_explorer_panel.raise_()
            self.toggle_project_explorer_action.setChecked(True)
            self.explorer_toggle_btn.setChecked(True)
            # Set initial splitter sizes if not already set
            if not self.explorer_splitter.sizes():
                self.explorer_splitter.setSizes([250, 1100])
    
    def save_current_settings(self):
        """Save current settings"""
        # Save app theme (all panels except preview)
        self.settings.set('app_theme', 'dark' if self.theme_toggle_action.isChecked() else 'light')
        
        # Save dark mode (preview only)
        self.settings.set('dark_mode', self.preview.dark_mode)
        
        # Save pane visibility
        self.settings.set('editor_visible', self.editor.isVisible())
        self.settings.set('preview_visible', self.preview.isVisible())
        
        # Save window geometry
        geometry = self.geometry()
        self.settings.set('window_width', geometry.width())
        self.settings.set('window_height', geometry.height())
        self.settings.set('window_x', geometry.x())
        self.settings.set('window_y', geometry.y())
        
        # Save splitter sizes
        if self.splitter.sizes():
            self.settings.set('splitter_sizes', self.splitter.sizes())
        
        # Save explorer splitter sizes (project explorer width)
        if self.explorer_splitter.sizes():
            self.settings.set('explorer_splitter_sizes', self.explorer_splitter.sizes())
        
        # Save to file
        self.settings.save_settings()
    
    def on_explorer_splitter_moved(self, positions, orientation):
        """Handle explorer splitter resize with debounced save"""
        # Use a debounced save to avoid excessive file writes while dragging
        if hasattr(self, '_explorer_save_timer'):
            self._explorer_save_timer.stop()
        else:
            self._explorer_save_timer = QTimer(self)
            self._explorer_save_timer.setSingleShot(True)
            self._explorer_save_timer.timeout.connect(self.save_current_settings)
        
        self._explorer_save_timer.start(500)  # 500ms delay after user stops resizing
    
    def update_auto_save_status(self):
        """Update the auto-save status indicator"""
        if self.current_file:
            self.auto_save_label.setText('Auto-save: ON')
            self.auto_save_label.setStyleSheet('color: #4CAF50; font-weight: bold;')
        else:
            self.auto_save_label.setText('Auto-save: OFF')
            self.auto_save_label.setStyleSheet('color: #999; font-weight: bold;')
    
    def create_toolbar(self):
        """Create the toolbar with formatting buttons"""
        self.toolbar = QToolBar('Formatting')
        self.toolbar.setMovable(False)
        self.toolbar.setIconSize(QSize(24, 24))
        self.toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        
        # Bold
        bold_action = QAction('B', self)
        bold_action.setToolTip('Bold (Ctrl+B)')
        bold_action.setFont(QFont('Arial', 12, QFont.Bold))
        bold_action.triggered.connect(lambda: self.editor.wrap_selection('**', '**'))
        self.toolbar.addAction(bold_action)
        
        # Italic
        italic_action = QAction('I', self)
        italic_action.setToolTip('Italic (Ctrl+I)')
        italic_action.setFont(QFont('Arial', 12, QFont.StyleItalic))
        italic_action.triggered.connect(lambda: self.editor.wrap_selection('*', '*'))
        self.toolbar.addAction(italic_action)
        
        # Heading
        heading_action = QAction('H', self)
        heading_action.setToolTip('Heading')
        heading_action.setFont(QFont('Arial', 12, QFont.Bold))
        heading_action.triggered.connect(self.insert_heading)
        self.toolbar.addAction(heading_action)
        
        # Link
        link_action = QAction('🔗', self)
        link_action.setToolTip('Link (Ctrl+K)')
        link_action.triggered.connect(lambda: self.editor.wrap_selection('[', '](url)'))
        self.toolbar.addAction(link_action)
        
        # Image
        image_action = QAction('🖼️', self)
        image_action.setToolTip('Image')
        image_action.triggered.connect(self.insert_image)
        self.toolbar.addAction(image_action)
        
        # Code
        code_action = QAction('<>', self)
        code_action.setToolTip('Inline Code (Ctrl+Shift+K)')
        code_action.triggered.connect(lambda: self.editor.wrap_selection('`', '`'))
        self.toolbar.addAction(code_action)
        
        # Code Block
        code_block_action = QAction('{ }', self)
        code_block_action.setToolTip('Code Block')
        code_block_action.triggered.connect(self.insert_code_block)
        self.toolbar.addAction(code_block_action)
        
        # Quote
        quote_action = QAction('❝', self)
        quote_action.setToolTip('Blockquote')
        quote_action.triggered.connect(self.insert_quote)
        self.toolbar.addAction(quote_action)
        
        # List
        list_action = QAction('☰', self)
        list_action.setToolTip('Unordered List')
        list_action.triggered.connect(self.insert_list)
        self.toolbar.addAction(list_action)
        
        # Table
        table_action = QAction('▦', self)
        table_action.setToolTip('Table')
        table_action.triggered.connect(self.insert_table)
        self.toolbar.addAction(table_action)
        
        # Horizontal Rule
        hr_action = QAction('—', self)
        hr_action.setToolTip('Horizontal Rule')
        hr_action.triggered.connect(self.insert_hr)
        self.toolbar.addAction(hr_action)
        
        # Add spacer to push view controls to the right
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.toolbar.addWidget(spacer)
        
        # Keep action for menu compatibility but don't add to toolbar
        self.toggle_project_explorer_action = QAction('📁', self)
        self.toggle_project_explorer_action.setToolTip('Toggle Project Explorer')
        self.toggle_project_explorer_action.setCheckable(True)
        self.toggle_project_explorer_action.setChecked(False)
        self.toggle_project_explorer_action.triggered.connect(self.toggle_project_explorer)
        
        # Dark mode toggle (preview only)
        self.dark_mode_action = QAction('🌙', self)
        self.dark_mode_action.setToolTip('Toggle Dark Preview')
        self.dark_mode_action.setCheckable(True)
        self.dark_mode_action.setChecked(False)
        self.dark_mode_action.triggered.connect(self.toggle_dark_mode)
        self.toolbar.addAction(self.dark_mode_action)
        
        # App theme toggle (all panels except preview)
        self.theme_toggle_action = QAction('🎨', self)
        self.theme_toggle_action.setToolTip('Toggle App Theme (Light/Dark)')
        self.theme_toggle_action.setCheckable(True)
        self.theme_toggle_action.setChecked(True)  # True = dark theme
        self.theme_toggle_action.triggered.connect(self.toggle_app_theme)
        self.toolbar.addAction(self.theme_toggle_action)
        
        # Toggle editor pane
        self.toggle_editor_action = QAction('📝', self)
        self.toggle_editor_action.setToolTip('Toggle Editor Pane')
        self.toggle_editor_action.setCheckable(True)
        self.toggle_editor_action.setChecked(True)
        self.toggle_editor_action.triggered.connect(self.toggle_editor_pane)
        self.toolbar.addAction(self.toggle_editor_action)
        
        # Toggle preview pane
        self.toggle_preview_pane_action = QAction('👁️', self)
        self.toggle_preview_pane_action.setToolTip('Toggle Preview Pane')
        self.toggle_preview_pane_action.setCheckable(True)
        self.toggle_preview_pane_action.setChecked(True)
        self.toggle_preview_pane_action.triggered.connect(self.toggle_preview_pane)
        self.toolbar.addAction(self.toggle_preview_pane_action)
    
    def create_menu_bar(self):
        """Create the menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('File')
        
        new_action = QAction('New', self)
        new_action.setShortcut('Ctrl+N')
        new_action.triggered.connect(self.new_file)
        file_menu.addAction(new_action)
        
        open_action = QAction('Open', self)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)
        
        save_action = QAction('Save', self)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)
        
        save_as_action = QAction('Save As', self)
        save_as_action.setShortcut('Ctrl+Shift+S')
        save_as_action.triggered.connect(self.save_file_as)
        file_menu.addAction(save_as_action)
        
        file_menu.addSeparator()
        
        # Project explorer actions
        open_dir_action = QAction('Open Directory...', self)
        open_dir_action.setShortcut('Ctrl+Shift+O')
        open_dir_action.triggered.connect(self.open_directory)
        file_menu.addAction(open_dir_action)
        
        new_file_action = QAction('New File in Directory', self)
        new_file_action.setShortcut('Ctrl+Shift+N')
        new_file_action.triggered.connect(self.on_toolbar_new_file)
        file_menu.addAction(new_file_action)
        
        new_folder_action = QAction('New Folder in Directory', self)
        new_folder_action.setShortcut('Ctrl+Shift+F')
        new_folder_action.triggered.connect(self.on_toolbar_new_folder)
        file_menu.addAction(new_folder_action)
        
        file_menu.addSeparator()
        
        # Manual auto-save trigger for testing
        auto_save_now_action = QAction('Auto-Save Now', self)
        auto_save_now_action.setShortcut('Ctrl+Alt+S')
        auto_save_now_action.triggered.connect(self.auto_save)
        file_menu.addAction(auto_save_now_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = menubar.addMenu('Edit')
        
        undo_action = QAction('Undo', self)
        undo_action.setShortcut('Ctrl+Z')
        undo_action.triggered.connect(self.editor.undo)
        edit_menu.addAction(undo_action)
        
        redo_action = QAction('Redo', self)
        redo_action.setShortcut('Ctrl+Y')
        redo_action.triggered.connect(self.editor.redo)
        edit_menu.addAction(redo_action)
        
        edit_menu.addSeparator()
        
        cut_action = QAction('Cut', self)
        cut_action.setShortcut('Ctrl+X')
        cut_action.triggered.connect(self.editor.cut)
        edit_menu.addAction(cut_action)
        
        copy_action = QAction('Copy', self)
        copy_action.setShortcut('Ctrl+C')
        copy_action.triggered.connect(self.editor.copy)
        edit_menu.addAction(copy_action)
        
        paste_action = QAction('Paste', self)
        paste_action.setShortcut('Ctrl+V')
        paste_action.triggered.connect(self.editor.paste)
        edit_menu.addAction(paste_action)
        
        # View menu
        view_menu = menubar.addMenu('View')
        
        toggle_preview_action = QAction('Toggle Preview Pane', self)
        toggle_preview_action.setShortcut('Ctrl+P')
        toggle_preview_action.triggered.connect(self.toggle_preview_pane)
        view_menu.addAction(toggle_preview_action)
        
        toggle_editor_action = QAction('Toggle Editor Pane', self)
        toggle_editor_action.setShortcut('Ctrl+E')
        toggle_editor_action.triggered.connect(self.toggle_editor_pane)
        view_menu.addAction(toggle_editor_action)
        
        toggle_dark_mode_action = QAction('Toggle Dark Preview', self)
        toggle_dark_mode_action.setShortcut('Ctrl+D')
        toggle_dark_mode_action.triggered.connect(self.toggle_dark_mode)
        view_menu.addAction(toggle_dark_mode_action)
        
        # App theme toggle (all panels except preview)
        toggle_app_theme_action = QAction('Toggle App Theme (Light/Dark)', self)
        toggle_app_theme_action.setShortcut('Ctrl+Shift+T')
        toggle_app_theme_action.triggered.connect(self.toggle_app_theme)
        view_menu.addAction(toggle_app_theme_action)
        
        view_menu.addSeparator()
        
        toggle_project_explorer_action = QAction('Toggle Project Explorer', self)
        toggle_project_explorer_action.setShortcut('Ctrl+Shift+E')
        toggle_project_explorer_action.triggered.connect(self.toggle_project_explorer)
        view_menu.addAction(toggle_project_explorer_action)
        
        # Help menu
        help_menu = menubar.addMenu('Help')
        
        about_action = QAction('About MDEV', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
        license_action = QAction('View License', self)
        license_action.triggered.connect(self.show_license)
        help_menu.addAction(license_action)
    
    def on_editor_changed(self):
        """Called when editor content changes"""
        # Debounce the preview update
        if hasattr(self, '_update_timer'):
            self._update_timer.stop()
        else:
            self._update_timer = QTimer(self)
            self._update_timer.setSingleShot(True)
            self._update_timer.timeout.connect(self.update_preview)
        
        self._update_timer.start(300)  # 300ms delay
        
        # Trigger auto-save after delay (only if we have a file open)
        if self.current_file:
            self.auto_save_timer.start(self.auto_save_delay)
        else:
            # Show hint that file needs to be saved first
            if self.editor.toPlainText().strip():
                self.status_bar.showMessage('Tip: Save file first (Ctrl+S) to enable auto-save', 5000)
        
        # Update status bar
        text = self.editor.toPlainText()
        self.char_count.setText(f'Characters: {len(text)}')
        self.word_count.setText(f'Words: {len(text.split())}')
        self.line_count.setText(f'Lines: {text.count(chr(10)) + 1}')
    
    def auto_save(self):
        """Auto-save the current file if one is open"""
        if not self.current_file:
            # Check if there's content to save
            if self.editor.toPlainText().strip():
                # Prompt user to save the file first
                self.status_bar.showMessage('Please save the file first (Ctrl+S)', 3000)
            else:
                self.status_bar.showMessage('No content to save', 3000)
            return
            
        if not self.editor.document().isModified():
            self.status_bar.showMessage('No changes to save', 3000)
            return
            
        try:
            content = self.editor.toPlainText()
            with open(self.current_file, 'w', encoding='utf-8') as f:
                f.write(content)
            # Mark document as not modified
            self.editor.document().setModified(False)
            self.status_bar.showMessage('✓ Auto-saved: ' + os.path.basename(self.current_file), 3000)
        except Exception as e:
            self.status_bar.showMessage(f'✗ Auto-save failed: {str(e)}', 5000)
    
    def update_preview(self):
        """Update the markdown preview"""
        markdown_text = self.editor.toPlainText()
        self.preview.update_preview(markdown_text)
    
    def insert_heading(self):
        """Insert a heading at current cursor position"""
        cursor = self.editor.textCursor()
        cursor.insertText('### Heading\n')
        self.editor.setTextCursor(cursor)
    
    def insert_image(self):
        """Insert image markdown syntax"""
        cursor = self.editor.textCursor()
        cursor.insertText('![alt text](image_url)\n')
        self.editor.setTextCursor(cursor)
    
    def insert_code_block(self):
        """Insert a code block"""
        cursor = self.editor.textCursor()
        cursor.insertText('```\ncode here\n```\n')
        self.editor.setTextCursor(cursor)
    
    def insert_quote(self):
        """Insert a blockquote"""
        cursor = self.editor.textCursor()
        cursor.insertText('> Quote text\n')
        self.editor.setTextCursor(cursor)
    
    def insert_list(self):
        """Insert an unordered list"""
        cursor = self.editor.textCursor()
        cursor.insertText('- Item 1\n- Item 2\n- Item 3\n')
        self.editor.setTextCursor(cursor)
    
    def insert_table(self):
        """Insert a table"""
        cursor = self.editor.textCursor()
        cursor.insertText('| Header 1 | Header 2 |\n|----------|----------|\n| Cell 1   | Cell 2   |\n| Cell 3   | Cell 4   |\n')
        self.editor.setTextCursor(cursor)
    
    def insert_hr(self):
        """Insert a horizontal rule"""
        cursor = self.editor.textCursor()
        cursor.insertText('\n---\n\n')
        self.editor.setTextCursor(cursor)
    
    def toggle_editor_pane(self):
        """Toggle the editor pane visibility"""
        editor_visible = self.toggle_editor_action.isChecked()
        self.editor.setVisible(editor_visible)
        self.status_bar.showMessage('Editor pane: ' + ('Visible' if editor_visible else 'Hidden'))
        
        # Ensure at least one pane is visible
        if not editor_visible and not self.toggle_preview_pane_action.isChecked():
            self.toggle_preview_pane_action.setChecked(True)
            self.preview.setVisible(True)
        
        # Save settings
        self.save_current_settings()
    
    def toggle_preview_pane(self):
        """Toggle the preview pane visibility"""
        preview_visible = self.toggle_preview_pane_action.isChecked()
        self.preview.setVisible(preview_visible)
        self.status_bar.showMessage('Preview pane: ' + ('Visible' if preview_visible else 'Hidden'))
        
        # Ensure at least one pane is visible
        if not preview_visible and not self.toggle_editor_action.isChecked():
            self.toggle_editor_action.setChecked(True)
            self.editor.setVisible(True)
        
        # Save settings
        self.save_current_settings()
    
    def toggle_dark_mode(self):
        """Toggle dark mode for preview"""
        dark_mode = self.dark_mode_action.isChecked()
        self.preview.dark_mode = dark_mode
        # Update preview with current content
        markdown_text = self.editor.toPlainText()
        self.preview.update_preview(markdown_text)
        self.status_bar.showMessage('Dark mode: ' + ('ON' if dark_mode else 'OFF'))
        
        # Save settings
        self.save_current_settings()
    
    def toggle_app_theme(self):
        """Toggle app theme between light and dark for all panels except preview"""
        is_dark = self.theme_toggle_action.isChecked()
        self.apply_app_theme('dark' if is_dark else 'light')
        theme_name = 'Dark' if is_dark else 'Light'
        self.status_bar.showMessage(f'App theme: {theme_name}')
        
        # Save settings
        self.save_current_settings()
    
    def apply_app_theme(self, theme):
        """Apply theme to all panels and window bars except preview pane"""
        if theme == 'dark':
            self.apply_dark_theme()
        else:
            self.apply_light_theme()
    
    def apply_dark_theme(self):
        """Apply dark theme to all UI elements except preview"""
        # Editor dark theme
        self.editor.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                border: none;
                selection-background-color: #264f78;
            }
        """)
        
        # Activity bar dark theme
        self.activity_bar.setStyleSheet("""
            QWidget {
                background-color: #333333;
                border-right: 1px solid #444444;
            }
        """)
        
        # Activity bar button dark theme
        self.explorer_toggle_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                color: #858585;
                font-size: 20px;
            }
            QPushButton:hover {
                color: #ffffff;
                background-color: #444444;
            }
            QPushButton:checked {
                color: #ffffff;
                border-left: 2px solid #007acc;
                background-color: #3c3c3c;
            }
        """)
        
        # Explorer splitter dark theme
        self.explorer_splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: #444444;
            }
            QSplitter::handle:hover {
                background-color: #007acc;
            }
        """)
        
        # Main splitter dark theme
        self.splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: #444444;
            }
            QSplitter::handle:hover {
                background-color: #007acc;
            }
        """)
        
        # Project explorer panel dark theme
        self.project_explorer_panel.setStyleSheet("""
            QWidget {
                background-color: #252526;
                border-right: 1px solid #444444;
            }
        """)
        
        # Explorer toolbar dark theme
        self.explorer_toolbar.setStyleSheet("""
            QToolBar {
                spacing: 4px;
                padding: 8px 4px;
                background-color: #252526;
                border-bottom: 1px solid #444444;
            }
            QToolBar QToolButton {
                background: transparent;
                border: none;
                color: #cccccc;
                padding: 4px 8px;
            }
            QToolBar QToolButton:hover {
                background-color: #444444;
            }
        """)
        
        # File tree dark theme
        self.file_tree.setStyleSheet("""
            QTreeView {
                background-color: #1e1e1e;
                color: #cccccc;
                border: none;
                selection-background-color: #094771;
                selection-color: #ffffff;
            }
            QTreeView::item {
                padding: 4px;
            }
            QTreeView::item:hover {
                background-color: #2a2d2e;
            }
        """)
        
        # Toolbar dark theme
        self.toolbar.setStyleSheet("""
            QToolBar {
                background-color: #2d2d30;
                border-bottom: 1px solid #444444;
                spacing: 4px;
                padding: 4px;
            }
            QToolBar QToolButton {
                background: transparent;
                border: none;
                color: #cccccc;
                padding: 4px 8px;
            }
            QToolBar QToolButton:hover {
                background-color: #444444;
            }
            QToolBar QToolButton:checked {
                background-color: #094771;
            }
        """)
        
        # Menu bar dark theme
        self.menuBar().setStyleSheet("""
            QMenuBar {
                background-color: #323233;
                color: #cccccc;
                border-bottom: 1px solid #444444;
            }
            QMenuBar::item {
                padding: 4px 8px;
                background: transparent;
            }
            QMenuBar::item:selected {
                background-color: #444444;
            }
            QMenu {
                background-color: #252526;
                color: #cccccc;
                border: 1px solid #444444;
            }
            QMenu::item {
                padding: 6px 24px 6px 12px;
            }
            QMenu::item:selected {
                background-color: #094771;
            }
            QMenu::separator {
                height: 1px;
                background-color: #444444;
                margin: 4px 12px;
            }
        """)
        
        # Status bar dark theme
        self.status_bar.setStyleSheet("""
            QStatusBar {
                background-color: #007acc;
                color: #ffffff;
                border-top: 1px solid #444444;
            }
        """)
        
        # Main window dark theme
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
            }
        """)
    
    def apply_light_theme(self):
        """Apply light theme to all UI elements except preview"""
        # Editor light theme
        self.editor.setStyleSheet("""
            QTextEdit {
                background-color: #ffffff;
                color: #333333;
                border: none;
                selection-background-color: #add6ff;
            }
        """)
        
        # Activity bar light theme
        self.activity_bar.setStyleSheet("""
            QWidget {
                background-color: #f8f8f8;
                border-right: 1px solid #e0e0e0;
            }
        """)
        
        # Activity bar button light theme
        self.explorer_toggle_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                color: #666666;
                font-size: 20px;
            }
            QPushButton:hover {
                color: #333333;
                background-color: #e8e8e8;
            }
            QPushButton:checked {
                color: #333333;
                border-left: 2px solid #007acc;
                background-color: #e0e0e0;
            }
        """)
        
        # Explorer splitter light theme
        self.explorer_splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: #cccccc;
            }
            QSplitter::handle:hover {
                background-color: #007acc;
            }
        """)
        
        # Main splitter light theme
        self.splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: #cccccc;
            }
            QSplitter::handle:hover {
                background-color: #007acc;
            }
        """)
        
        # Project explorer panel light theme
        self.project_explorer_panel.setStyleSheet("""
            QWidget {
                background-color: #f3f3f3;
                border-right: 1px solid #e0e0e0;
            }
        """)
        
        # Explorer toolbar light theme
        self.explorer_toolbar.setStyleSheet("""
            QToolBar {
                spacing: 4px;
                padding: 8px 4px;
                background-color: #f3f3f3;
                border-bottom: 1px solid #e0e0e0;
            }
            QToolBar QToolButton {
                background: transparent;
                border: none;
                color: #333333;
                padding: 4px 8px;
            }
            QToolBar QToolButton:hover {
                background-color: #e0e0e0;
            }
        """)
        
        # File tree light theme
        self.file_tree.setStyleSheet("""
            QTreeView {
                background-color: #ffffff;
                color: #333333;
                border: none;
                selection-background-color: #0078d4;
                selection-color: #ffffff;
            }
            QTreeView::item {
                padding: 4px;
            }
            QTreeView::item:hover {
                background-color: #e8e8e8;
            }
        """)
        
        # Toolbar light theme
        self.toolbar.setStyleSheet("""
            QToolBar {
                background-color: #f8f8f8;
                border-bottom: 1px solid #e0e0e0;
                spacing: 4px;
                padding: 4px;
            }
            QToolBar QToolButton {
                background: transparent;
                border: none;
                color: #333333;
                padding: 4px 8px;
            }
            QToolBar QToolButton:hover {
                background-color: #e0e0e0;
            }
            QToolBar QToolButton:checked {
                background-color: #0078d4;
            }
        """)
        
        # Menu bar light theme
        self.menuBar().setStyleSheet("""
            QMenuBar {
                background-color: #f8f8f8;
                color: #333333;
                border-bottom: 1px solid #e0e0e0;
            }
            QMenuBar::item {
                padding: 4px 8px;
                background: transparent;
            }
            QMenuBar::item:selected {
                background-color: #e0e0e0;
            }
            QMenu {
                background-color: #ffffff;
                color: #333333;
                border: 1px solid #cccccc;
            }
            QMenu::item {
                padding: 6px 24px 6px 12px;
            }
            QMenu::item:selected {
                background-color: #e8e8e8;
            }
            QMenu::separator {
                height: 1px;
                background-color: #e0e0e0;
                margin: 4px 12px;
            }
        """)
        
        # Status bar light theme
        self.status_bar.setStyleSheet("""
            QStatusBar {
                background-color: #007acc;
                color: #ffffff;
                border-top: 1px solid #e0e0e0;
            }
        """)
        
        # Main window light theme
        self.setStyleSheet("""
            QMainWindow {
                background-color: #ffffff;
            }
        """)
    
    def apply_context_menu_style(self, menu):
        """Apply theme-appropriate style to a context menu"""
        if self.theme_toggle_action.isChecked():  # Dark theme
            menu.setStyleSheet("""
                QMenu {
                    background-color: #252526;
                    color: #cccccc;
                    border: 1px solid #444444;
                }
                QMenu::item {
                    padding: 6px 24px 6px 12px;
                }
                QMenu::item:selected {
                    background-color: #094771;
                }
                QMenu::separator {
                    height: 1px;
                    background-color: #444444;
                    margin: 4px 12px;
                }
            """)
        else:  # Light theme
            menu.setStyleSheet("""
                QMenu {
                    background-color: #ffffff;
                    color: #333333;
                    border: 1px solid #cccccc;
                }
                QMenu::item {
                    padding: 6px 24px 6px 12px;
                }
                QMenu::item:selected {
                    background-color: #e8e8e8;
                }
                QMenu::separator {
                    height: 1px;
                    background-color: #e0e0e0;
                    margin: 4px 12px;
                }
            """)
    
    def show_editor_context_menu(self, position):
        """Show context menu for the editor pane"""
        context_menu = QMenu(self)
        self.apply_context_menu_style(context_menu)
        
        # Add standard text editing actions
        cut_action = QAction('✂️ Cut', self)
        cut_action.setShortcut('Ctrl+X')
        cut_action.triggered.connect(lambda: self.editor.textCursor().removeSelectedText() if self.editor.textCursor().hasSelection() else None)
        cut_action.setEnabled(self.editor.textCursor().hasSelection())
        context_menu.addAction(cut_action)
        
        copy_action = QAction('📋 Copy', self)
        copy_action.setShortcut('Ctrl+C')
        copy_action.triggered.connect(self.editor.copy)
        copy_action.setEnabled(self.editor.textCursor().hasSelection())
        context_menu.addAction(copy_action)
        
        paste_action = QAction('📌 Paste', self)
        paste_action.setShortcut('Ctrl+V')
        paste_action.triggered.connect(self.editor.paste)
        context_menu.addAction(paste_action)
        
        context_menu.addSeparator()
        
        select_all_action = QAction('☑️ Select All', self)
        select_all_action.setShortcut('Ctrl+A')
        select_all_action.triggered.connect(self.editor.selectAll)
        context_menu.addAction(select_all_action)
        
        # Show the menu at the cursor position
        context_menu.exec_(self.editor.mapToGlobal(position))
    
    def show_preview_context_menu(self, position):
        """Show context menu for the preview pane"""
        context_menu = QMenu(self)
        self.apply_context_menu_style(context_menu)
        
        # Add standard web view actions
        back_action = QAction('← Back', self)
        back_action.setEnabled(self.preview.page().action(QWebEnginePage.Back).isEnabled())
        back_action.triggered.connect(self.preview.page().action(QWebEnginePage.Back).trigger)
        context_menu.addAction(back_action)
        
        forward_action = QAction('→ Forward', self)
        forward_action.setEnabled(self.preview.page().action(QWebEnginePage.Forward).isEnabled())
        forward_action.triggered.connect(self.preview.page().action(QWebEnginePage.Forward).trigger)
        context_menu.addAction(forward_action)
        
        reload_action = QAction('↻ Reload', self)
        reload_action.triggered.connect(self.preview.reload)
        context_menu.addAction(reload_action)
        
        context_menu.addSeparator()
        
        # Show the menu at the cursor position
        context_menu.exec_(self.preview.mapToGlobal(position))
    
    def new_file(self):
        """Create a new file"""
        # If auto-save is OFF and there are unsaved changes, prompt to save
        if not self.current_file and self.editor.document().isModified():
            reply = QMessageBox.question(
                self, 'Unsaved Changes',
                'You have unsaved changes. Do you want to save them before creating a new file?',
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
                QMessageBox.Save
            )
            
            if reply == QMessageBox.Save:
                if not self.save_file_as():
                    return
            elif reply == QMessageBox.Cancel:
                return
        
        # Auto-save current file if there are changes and a file is open
        if self.current_file and self.editor.document().isModified():
            try:
                content = self.editor.toPlainText()
                with open(self.current_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.editor.document().setModified(False)
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Could not auto-save file:\n{str(e)}')
                return
        
        self.editor.clear()
        self.current_file = None
        self.setWindowTitle('MDEV (MarkDown Editor/Viewer)')
        self.status_bar.showMessage('New file created')
        self.update_auto_save_status()
    
    def open_file(self):
        """Open a markdown file"""
        # If auto-save is OFF and there are unsaved changes, prompt to save
        if not self.current_file and self.editor.document().isModified():
            reply = QMessageBox.question(
                self, 'Unsaved Changes',
                'You have unsaved changes. Do you want to save them before opening a new file?',
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
                QMessageBox.Save
            )
            
            if reply == QMessageBox.Save:
                if not self.save_file_as():
                    return
            elif reply == QMessageBox.Cancel:
                return
        
        # Auto-save current file if there are changes and a file is open
        if self.current_file and self.editor.document().isModified():
            try:
                content = self.editor.toPlainText()
                with open(self.current_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.editor.document().setModified(False)
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Could not auto-save file:\n{str(e)}')
                return
        
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            'Open Markdown File',
            '',
            'Markdown Files (*.md *.markdown *.txt);;All Files (*)'
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Block signals to prevent triggering auto-save during load
                self.editor.blockSignals(True)
                self.editor.setPlainText(content)
                self.editor.blockSignals(False)
                
                # Mark document as not modified after loading
                self.editor.document().setModified(False)
                
                self.current_file = file_path
                self.setWindowTitle(f'MDEV (MarkDown Editor/Viewer) - {os.path.basename(file_path)}')
                self.status_bar.showMessage(f'Opened: {file_path} (Auto-save enabled)')
                self.update_auto_save_status()
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Could not open file:\n{str(e)}')
    
    def save_file(self):
        """Save the current file"""
        if self.current_file:
            return self._save_to_file(self.current_file)
        else:
            return self.save_file_as()
    
    def save_file_as(self):
        """Save the file with a new name"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            'Save Markdown File',
            '',
            'Markdown Files (*.md);;All Files (*)'
        )
        
        if file_path:
            if not file_path.endswith('.md'):
                file_path += '.md'
            
            success = self._save_to_file(file_path)
            if success:
                self.current_file = file_path
                self.setWindowTitle(f'MDEV (MarkDown Editor/Viewer) - {os.path.basename(file_path)}')
                self.status_bar.showMessage(f'Saved: {file_path}')
            return success
        return False
    
    def _save_to_file(self, file_path):
        """Save content to file"""
        try:
            content = self.editor.toPlainText()
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            self.current_file = file_path
            self.editor.document().setModified(False)
            self.update_auto_save_status()
            return True
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Could not save file:\n{str(e)}')
            return False
    
    def show_about(self):
        """Show about dialog"""
        about_text = (
            '<h2 style="color: #007acc;">MDEV (MarkDown Editor/Viewer)</h2>'
            '<p>A native desktop markdown editor and viewer built with Python and PyQt5.</p>'
            '<hr>'
            '<p><b>Features:</b></p>'
            '<ul>'
            '<li>✅ Live markdown preview</li>'
            '<li>✅ Syntax highlighting with dark theme</li>'
            '<li>✅ Dark/Light theme preview toggle</li>'
            '<li>✅ App theme toggle (Light/Dark) for all panels</li>'
            '<li>✅ Toggle editor/preview panes independently</li>'
            '<li>✅ Auto-save after every edit (2 second delay)</li>'
            '<li>✅ Full markdown support (headings, lists, tables, code blocks, etc.)</li>'
            '<li>✅ File explorer with project management</li>'
            '<li>✅ Toolbar with quick formatting buttons</li>'
            '<li>✅ Status bar with character/word/line counts</li>'
            '</ul>'
            '<hr>'
            '<p><b>Keyboard Shortcuts:</b></p>'
            '<ul>'
            '<li>Ctrl+B - Bold | Ctrl+I - Italic | Ctrl+K - Link</li>'
            '<li>Ctrl+Shift+K - Inline Code | Ctrl+D - Toggle Dark Preview</li>'
            '<li>Ctrl+Shift+T - Toggle App Theme | Ctrl+E - Toggle Editor Pane</li>'
            '<li>Ctrl+P - Toggle Preview Pane | Ctrl+S - Save | Ctrl+O - Open</li>'
            '<li>Ctrl+N - New File | Ctrl+Q - Exit</li>'
            '</ul>'
            '<hr>'
            '<p><b>Version:</b> 1.4.0</p>'
            '<p><b>Created by:</b> Joe Temte</p>'
            '<p><b>License:</b> MIT License</p>'
            '<hr>'
            '<p style="font-size: small; color: #666;">' 
            'Built with Python, PyQt5, PyQtWebEngine, Markdown, and Pygments</p>'
        )
        
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle('About MDEV')
        msg_box.setTextFormat(Qt.RichText)
        msg_box.setText(about_text)
        msg_box.setInformativeText('Click "View License" to see the full MIT License text.')
        msg_box.setStandardButtons(QMessageBox.Ok)
        
        # Add a "View License" button
        view_license_btn = msg_box.addButton('View License', QMessageBox.ActionRole)
        view_license_btn.clicked.connect(self.show_license)
        
        msg_box.exec_()
    
    def show_license(self):
        """Show the MIT License dialog"""
        license_text = """MIT License

Copyright (c) 2026 Joe Temte

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""
        
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle('MIT License')
        msg_box.setTextFormat(Qt.RichText)
        msg_box.setText(
            '<h3>MIT License</h3>'
            '<p><b>Copyright (c) 2026 Joe Temte</b></p>'
            '<hr>'
        )
        msg_box.setInformativeText(license_text)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()
    
    def closeEvent(self, event):
        """Handle window close event"""
        # If auto-save is OFF and there are unsaved changes, prompt to save
        if not self.current_file and self.editor.document().isModified():
            reply = QMessageBox.question(
                self, 'Unsaved Changes',
                'You have unsaved changes. Do you want to save them before closing?',
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
                QMessageBox.Save
            )
            
            if reply == QMessageBox.Save:
                if not self.save_file_as():
                    event.ignore()
                    return
            elif reply == QMessageBox.Cancel:
                event.ignore()
                return
        
        # Auto-save if there are changes and a file is open
        if self.current_file and self.editor.document().isModified():
            try:
                content = self.editor.toPlainText()
                with open(self.current_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.editor.document().setModified(False)
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Could not auto-save file:\n{str(e)}\n\nYour changes may be lost.')
                event.ignore()
                return
        
        # Save settings before closing
        self.save_current_settings()
        
        event.accept()


def main():
    """Main entry point"""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Cross-platform style
    
    # Set application-wide font
    font = QFont('Segoe UI', 10)
    app.setFont(font)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
