"""
Preview Toolbar Component for MDEV

Handles preview-specific controls like dark mode toggle.
"""

from PyQt5.QtWidgets import QToolBar, QAction, QWidget
from PyQt5.QtCore import Qt, QSize

import constants
import styles


class PreviewToolbar(QToolBar):
    """Toolbar with preview control buttons."""

    def __init__(self, parent=None):
        super().__init__('Preview', parent)
        self.parent_window = parent
        self.setup_ui()

    def setup_ui(self):
        """Setup the preview toolbar UI."""
        self.setMovable(False)
        self.setIconSize(QSize(20, 20))
        self.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.setStyleSheet(styles.DARK_PREVIEW_TOOLBAR_STYLE)

        # Add spacer to push dark mode button to the right
        spacer = QWidget()
        spacer.setSizePolicy(spacer.sizePolicy().Expanding, spacer.sizePolicy().Expanding)
        self.addWidget(spacer)

        # Toggle dark mode for preview
        self.dark_mode_action = QAction('🌙 Dark Preview', self)
        self.dark_mode_action.setToolTip('Toggle Dark Preview Mode')
        self.dark_mode_action.setCheckable(True)
        self.dark_mode_action.setChecked(False)
        self.dark_mode_action.triggered.connect(self._on_toggle_dark_mode)
        self.addAction(self.dark_mode_action)

    # ========================================================================
    # Private Event Handlers
    # ========================================================================

    def _on_toggle_dark_mode(self):
        """Toggle dark mode for preview."""
        if self.parent_window:
            dark_mode = self.dark_mode_action.isChecked()
            self.parent_window.toggle_dark_mode(dark_mode)

    # ========================================================================
    # Public API
    # ========================================================================

    def sync_dark_mode_state(self, dark_mode):
        """Sync the dark mode toggle button state."""
        self.dark_mode_action.blockSignals(True)
        self.dark_mode_action.setChecked(dark_mode)
        self.dark_mode_action.blockSignals(False)

    # ========================================================================
    # Theme Management
    # ========================================================================

    def set_theme(self, theme):
        """Apply theme to preview toolbar."""
        if theme == 'dark':
            self.setStyleSheet(styles.DARK_PREVIEW_TOOLBAR_STYLE)
        else:
            self.setStyleSheet(styles.LIGHT_PREVIEW_TOOLBAR_STYLE)
