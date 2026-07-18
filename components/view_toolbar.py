"""
View Toolbar Component for MDEV

Handles view-related controls like pane toggles and pane swapping.
"""

from PyQt5.QtWidgets import QToolBar, QAction, QWidget, QSizePolicy
from PyQt5.QtCore import Qt, QSize

import constants
import styles


class ViewToolbar(QToolBar):
    """Toolbar with view control buttons."""

    def __init__(self, parent=None):
        super().__init__('View', parent)
        self.parent_window = parent
        self.setup_ui()

    def setup_ui(self):
        """Setup the view toolbar UI."""
        self.setMovable(False)
        self.setIconSize(QSize(20, 20))
        self.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.setStyleSheet(styles.DARK_VIEW_TOOLBAR_STYLE)

        # Swap panes
        self.swap_panes_action = QAction('⇄ Swap', self)
        self.swap_panes_action.setToolTip('Swap Editor and Preview Positions')
        self.swap_panes_action.triggered.connect(self._on_swap_panes)
        self.addAction(self.swap_panes_action)

        # Toggle editor pane
        self.toggle_editor_action = QAction('📝 Editor', self)
        self.toggle_editor_action.setToolTip('Toggle Editor Pane')
        self.toggle_editor_action.setCheckable(True)
        self.toggle_editor_action.setChecked(True)
        self.toggle_editor_action.triggered.connect(self._on_toggle_editor)
        self.addAction(self.toggle_editor_action)

        # Toggle preview pane
        self.toggle_preview_action = QAction('👁️ Preview', self)
        self.toggle_preview_action.setToolTip('Toggle Preview Pane')
        self.toggle_preview_action.setCheckable(True)
        self.toggle_preview_action.setChecked(True)
        self.toggle_preview_action.triggered.connect(self._on_toggle_preview)
        self.addAction(self.toggle_preview_action)

        # Add expanding spacer at the beginning to push buttons to the right
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.insertWidget(self.swap_panes_action, spacer)

    # ========================================================================
    # Private Event Handlers
    # ========================================================================

    def _on_toggle_editor(self):
        """Toggle editor pane visibility."""
        if self.parent_window:
            editor_visible = self.toggle_editor_action.isChecked()
            self.parent_window.toggle_editor_pane(editor_visible)

    def _on_toggle_preview(self):
        """Toggle preview pane visibility."""
        if self.parent_window:
            preview_visible = self.toggle_preview_action.isChecked()
            self.parent_window.toggle_preview_pane(preview_visible)

    def _on_swap_panes(self):
        """Swap editor and preview pane positions."""
        if self.parent_window:
            self.parent_window.swap_pane_positions()

    # ========================================================================
    # Public API
    # ========================================================================

    def sync_editor_state(self, editor_visible):
        """Sync the editor toggle button state."""
        self.toggle_editor_action.blockSignals(True)
        self.toggle_editor_action.setChecked(editor_visible)
        self.toggle_editor_action.blockSignals(False)

    def sync_preview_state(self, preview_visible):
        """Sync the preview toggle button state."""
        self.toggle_preview_action.blockSignals(True)
        self.toggle_preview_action.setChecked(preview_visible)
        self.toggle_preview_action.blockSignals(False)

    # ========================================================================
    # Theme Management
    # ========================================================================

    def set_theme(self, theme):
        """Apply theme to view toolbar."""
        if theme == 'dark':
            self.setStyleSheet(styles.DARK_VIEW_TOOLBAR_STYLE)
        else:
            self.setStyleSheet(styles.LIGHT_VIEW_TOOLBAR_STYLE)
