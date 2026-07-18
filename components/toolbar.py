"""
Editor Toolbar Component for MDEV

Handles its own events and delegates to main_window only for state changes.
"""

from PyQt5.QtWidgets import QToolBar, QAction, QWidget
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QSize

import constants
import styles


class EditorToolbar(QToolBar):
    """Toolbar with formatting buttons and view controls."""

    def __init__(self, parent=None):
        super().__init__('Formatting', parent)
        self.parent_window = parent
        self.setup_ui()

    def setup_ui(self):
        """Setup the toolbar UI."""
        self.setMovable(False)
        self.setIconSize(QSize(24, 24))
        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.setStyleSheet(styles.DARK_TOOLBAR_STYLE)

        # Formatting buttons only (view controls moved to menu/activity bar)
        self._setup_formatting_actions()

    def _setup_formatting_actions(self):
        """Setup formatting action buttons."""
        # Bold
        bold_action = QAction('B', self)
        bold_action.setToolTip(f'Bold ({constants.SHORTCUTS["bold"]})')
        bold_action.setFont(QFont('Arial', 12, QFont.Bold))
        bold_action.triggered.connect(self._on_bold)
        self.addAction(bold_action)

        # Italic
        italic_action = QAction('I', self)
        italic_action.setToolTip(f'Italic ({constants.SHORTCUTS["italic"]})')
        italic_action.setFont(QFont('Arial', 12, QFont.StyleItalic))
        italic_action.triggered.connect(self._on_italic)
        self.addAction(italic_action)

        # Heading
        heading_action = QAction('H', self)
        heading_action.setToolTip('Heading')
        heading_action.setFont(QFont('Arial', 12, QFont.Bold))
        heading_action.triggered.connect(self._on_insert_heading)
        self.addAction(heading_action)

        # Link
        link_action = QAction('🔗', self)
        link_action.setToolTip(f'Link ({constants.SHORTCUTS["link"]})')
        link_action.triggered.connect(self._on_link)
        self.addAction(link_action)

        # Image
        image_action = QAction('🖼️', self)
        image_action.setToolTip('Image')
        image_action.triggered.connect(self._on_insert_image)
        self.addAction(image_action)

        # Code
        code_action = QAction('<>', self)
        code_action.setToolTip(f'Inline Code ({constants.SHORTCUTS["inline_code"]})')
        code_action.triggered.connect(self._on_inline_code)
        self.addAction(code_action)

        # Code Block
        code_block_action = QAction('{ }', self)
        code_block_action.setToolTip('Code Block')
        code_block_action.triggered.connect(self._on_insert_code_block)
        self.addAction(code_block_action)

        # Quote
        quote_action = QAction('❝', self)
        quote_action.setToolTip('Blockquote')
        quote_action.triggered.connect(self._on_insert_quote)
        self.addAction(quote_action)

        # List
        list_action = QAction('☰', self)
        list_action.setToolTip('Unordered List')
        list_action.triggered.connect(self._on_insert_list)
        self.addAction(list_action)

        # Table
        table_action = QAction('▦', self)
        table_action.setToolTip('Table')
        table_action.triggered.connect(self._on_insert_table)
        self.addAction(table_action)

        # Horizontal Rule
        hr_action = QAction('—', self)
        hr_action.setToolTip('Horizontal Rule')
        hr_action.triggered.connect(self._on_insert_hr)
        self.addAction(hr_action)



    # ========================================================================
    # Private Event Handlers - handle events directly
    # ========================================================================

    def _on_bold(self):
        """Wrap selection with bold markers."""
        if self.parent_window and hasattr(self.parent_window, 'editor'):
            self.parent_window.editor.wrap_selection('**', '**')

    def _on_italic(self):
        """Wrap selection with italic markers."""
        if self.parent_window and hasattr(self.parent_window, 'editor'):
            self.parent_window.editor.wrap_selection('*', '*')

    def _on_link(self):
        """Wrap selection with link markers."""
        if self.parent_window and hasattr(self.parent_window, 'editor'):
            self.parent_window.editor.wrap_selection('[', '](url)')

    def _on_inline_code(self):
        """Wrap selection with code markers."""
        if self.parent_window and hasattr(self.parent_window, 'editor'):
            self.parent_window.editor.wrap_selection('`', '`')

    def _on_insert_heading(self):
        """Insert heading."""
        if self.parent_window and hasattr(self.parent_window, 'editor'):
            self.parent_window.editor.insert_heading()

    def _on_insert_image(self):
        """Insert image."""
        if self.parent_window and hasattr(self.parent_window, 'editor'):
            self.parent_window.editor.insert_image()

    def _on_insert_code_block(self):
        """Insert code block."""
        if self.parent_window and hasattr(self.parent_window, 'editor'):
            self.parent_window.editor.insert_code_block()

    def _on_insert_quote(self):
        """Insert quote."""
        if self.parent_window and hasattr(self.parent_window, 'editor'):
            self.parent_window.editor.insert_quote()

    def _on_insert_list(self):
        """Insert list."""
        if self.parent_window and hasattr(self.parent_window, 'editor'):
            self.parent_window.editor.insert_list()

    def _on_insert_table(self):
        """Insert table."""
        if self.parent_window and hasattr(self.parent_window, 'editor'):
            self.parent_window.editor.insert_table()

    def _on_insert_hr(self):
        """Insert horizontal rule."""
        if self.parent_window and hasattr(self.parent_window, 'editor'):
            self.parent_window.editor.insert_hr()



    # ========================================================================
    # Theme Management
    # ========================================================================

    def set_theme(self, theme):
        """Apply theme to toolbar."""
        if theme == 'dark':
            self.setStyleSheet(styles.DARK_TOOLBAR_STYLE)
        else:
            self.setStyleSheet(styles.LIGHT_TOOLBAR_STYLE)
