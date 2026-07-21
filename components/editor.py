"""
Markdown Editor Text Edit Component
"""

from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QFont

import constants
import styles
from utils.spell_checker import SpellCheckEngine, SpellCheckHighlighter


class MarkdownEditorTextEdit(QTextEdit):
    """Custom text editor with markdown syntax highlighting and text insertion"""
    
    # Signal emitted when editor scroll position changes
    scroll_position_changed = pyqtSignal(int)
    
    # Scroll change tolerance (pixels) - ignore small changes to prevent drift
    SCROLL_TOLERANCE = 3
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFont(QFont(constants.EDITOR_FONT_FAMILY, constants.EDITOR_FONT_SIZE))
        self.setPlaceholderText("Type your markdown here...")
        self.setLineWrapMode(QTextEdit.WidgetWidth)
        
        # Set up initial colors (dark theme by default)
        self.setStyleSheet(styles.DARK_EDITOR_STYLE)
        
        # Initialize spell checker
        self.spell_engine = SpellCheckEngine(language='en')
        self.spell_highlighter = SpellCheckHighlighter(self, self.spell_engine)
        
        # Connect signals
        self.document().contentsChanged.connect(self.update_syntax_highlighting)
        self.selectionChanged.connect(self.update_syntax_highlighting)
        
        # Track scroll synchronization state
        self._is_syncing_scroll = False  # Flag to prevent infinite scroll sync loops
        self._scroll_ratio = 0.0  # Current scroll ratio (0.0 to 1.0)
        self._last_scroll_value = 0  # Track last scroll value for change detection
        self._pending_sync_value = None  # Track expected scroll value after sync
        
        # Connect vertical scrollbar valueChanged signal
        self.verticalScrollBar().valueChanged.connect(self._on_scroll_changed)
        
    def update_syntax_highlighting(self):
        """Update syntax highlighting when text changes"""
        # This is a placeholder - full implementation would use Pygments
        pass
    
    def _on_scroll_changed(self, value):
        """Handle scroll position changes in the editor"""
        # If we're waiting for a sync to complete, check if we're close enough
        if self._pending_sync_value is not None:
            if abs(value - self._pending_sync_value) <= self.SCROLL_TOLERANCE:
                # We've reached the target scroll position, clear pending sync
                self._pending_sync_value = None
                self._last_scroll_value = value
                self._is_syncing_scroll = False
            return
        
        if self._is_syncing_scroll:
            return
        
        # Check if scroll position changed significantly (with tolerance)
        if abs(value - self._last_scroll_value) < self.SCROLL_TOLERANCE:
            return  # Ignore small changes to prevent drift
        
        self._last_scroll_value = value
        
        # Calculate scroll ratio
        max_scroll = self.verticalScrollBar().maximum()
        if max_scroll > 0:
            self._scroll_ratio = value / max_scroll
        else:
            self._scroll_ratio = 0.0
        
        # Emit signal with scroll ratio (scaled to 1000 for precision)
        self.scroll_position_changed.emit(int(self._scroll_ratio * 1000))
    
    def sync_scroll_from_preview(self, scroll_ratio_1000):
        """
        Synchronize editor scroll position based on preview scroll ratio.
        
        Args:
            scroll_ratio_1000: Scroll ratio from preview (0-1000 scale)
        """
        if self._is_syncing_scroll:
            return
        
        self._is_syncing_scroll = True
        
        # Convert ratio back to 0.0-1.0 range
        ratio = scroll_ratio_1000 / 1000.0
        self._scroll_ratio = ratio
        
        # Set editor scroll position based on ratio
        max_scroll = self.verticalScrollBar().maximum()
        new_value = int(ratio * max_scroll)
        self.verticalScrollBar().setValue(new_value)
        
        # Set pending sync target so scrollbar handler knows to wait for this scroll
        self._pending_sync_value = new_value
        
        # Reset the flag after a delay as a fallback (in case sync completes quickly)
        QTimer.singleShot(100, self._reset_syncing_flag)
    
    def _reset_syncing_flag(self):
        """Reset the syncing flag after scroll operation completes."""
        self._is_syncing_scroll = False
        self._pending_sync_value = None
    
    def get_scroll_ratio(self):
        """Get the current scroll ratio (0.0 to 1.0)"""
        return self._scroll_ratio
    
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
