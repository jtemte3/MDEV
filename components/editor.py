"""
Markdown Editor Text Edit Component
"""

from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

import constants
import styles


class MarkdownEditorTextEdit(QTextEdit):
    """Custom text editor with markdown syntax highlighting and text insertion"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFont(QFont(constants.EDITOR_FONT_FAMILY, constants.EDITOR_FONT_SIZE))
        self.setPlaceholderText("Type your markdown here...")
        self.setLineWrapMode(QTextEdit.WidgetWidth)
        
        # Set up initial colors (dark theme by default)
        self.setStyleSheet(styles.DARK_EDITOR_STYLE)
        
        # Connect signals
        self.document().contentsChanged.connect(self.update_syntax_highlighting)
        self.selectionChanged.connect(self.update_syntax_highlighting)
        
    def update_syntax_highlighting(self):
        """Update syntax highlighting when text changes"""
        # This is a placeholder - full implementation would use Pygments
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
    
    # ========================================================================
    # Text Insertion Methods
    # ========================================================================
    
    def insert_heading(self):
        """Insert a heading at current cursor position"""
        cursor = self.textCursor()
        cursor.insertText('### Heading\n')
        self.setTextCursor(cursor)
    
    def insert_image(self):
        """Insert image markdown syntax"""
        cursor = self.textCursor()
        cursor.insertText('![alt text](image_url)\n')
        self.setTextCursor(cursor)
    
    def insert_code_block(self):
        """Insert a code block"""
        cursor = self.textCursor()
        cursor.insertText('```\ncode here\n```\n')
        self.setTextCursor(cursor)
    
    def insert_quote(self):
        """Insert a blockquote"""
        cursor = self.textCursor()
        cursor.insertText('> Quote text\n')
        self.setTextCursor(cursor)
    
    def insert_list(self):
        """Insert an unordered list"""
        cursor = self.textCursor()
        cursor.insertText('- Item 1\n- Item 2\n- Item 3\n')
        self.setTextCursor(cursor)
    
    def insert_table(self):
        """Insert a table"""
        cursor = self.textCursor()
        cursor.insertText('| Header 1 | Header 2 |\n|----------|----------|\n| Cell 1   | Cell 2   |\n| Cell 3   | Cell 4   |\n')
        self.setTextCursor(cursor)
    
    def insert_hr(self):
        """Insert a horizontal rule"""
        cursor = self.textCursor()
        cursor.insertText('\n---\n\n')
        self.setTextCursor(cursor)
    
    def set_theme(self, theme):
        """Apply theme to editor"""
        if theme == 'dark':
            self.setStyleSheet(styles.DARK_EDITOR_STYLE)
        else:
            self.setStyleSheet(styles.LIGHT_EDITOR_STYLE)
