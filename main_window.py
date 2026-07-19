"""
Main Window for MDEV (MarkDown Editor/Viewer)

Minimal main window focused on layout and component orchestration only.
Components handle their own events.
"""

import sys
import os
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QSplitter, QLabel, QStatusBar
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon

import constants
import styles
from components.editor import MarkdownEditorTextEdit
from components.preview import MarkdownPreview
from components.activity_bar import ActivityBar
from components.explorer import ProjectExplorer
from components.toolbar import EditorToolbar
from components.app_toolbar import AppToolbar
from components.preview_toolbar import PreviewToolbar
from components.menus import MenuBar
from components.editor_context_menu import EditorContextMenu
from components.preview_context_menu import PreviewContextMenu
from utils.settings import SettingsManager
from utils.file_ops import FileManager


class MainWindow(QMainWindow):
    """Main application window - handles layout and component orchestration only."""

    def __init__(self):
        super().__init__()
        self.current_file = None
        self.current_directory = None
        self.current_theme = 'dark'  # Track current theme
        self.settings = SettingsManager()

        # Auto-save timer
        self.auto_save_timer = QTimer(self)
        self.auto_save_timer.setSingleShot(True)
        self.auto_save_timer.timeout.connect(self._auto_save)
        self.auto_save_delay = constants.AUTO_SAVE_DELAY_MS

        # Initialize components
        self.activity_bar = ActivityBar(self)
        self.project_explorer = ProjectExplorer(self)
        self.toolbar = EditorToolbar(self)
        self.app_toolbar = AppToolbar(self)
        self.preview_toolbar = PreviewToolbar(self)
        self.menu_bar = MenuBar(self)
        self.editor = MarkdownEditorTextEdit()
        self.preview = MarkdownPreview()
        self.splitter = QSplitter(Qt.Horizontal)
        self.explorer_splitter = QSplitter(Qt.Horizontal)
        self.status_bar = QStatusBar()
        self.char_count = QLabel('Characters: 0')
        self.word_count = QLabel('Words: 0')
        self.line_count = QLabel('Lines: 1')
        self.auto_save_label = QLabel('Auto-save: OFF')

        # Context menus
        self.editor_context_menu = EditorContextMenu(self)
        self.preview_context_menu = PreviewContextMenu(self)

        # File manager (initialized after editor)
        self.file_manager = None

        self._init_ui()
        self.file_manager = FileManager(self.editor, self)
        self._apply_saved_settings()

    def _init_ui(self):
        """Initialize the user interface layout."""
        self.setWindowTitle(constants.APP_NAME)
        self.setGeometry(
            constants.DEFAULT_WINDOW_X,
            constants.DEFAULT_WINDOW_Y,
            constants.DEFAULT_WINDOW_WIDTH,
            constants.DEFAULT_WINDOW_HEIGHT
        )

        # Set application icon
        base_path = sys._MEIPASS if hasattr(sys, '_MEIPASS') else os.path.abspath(".")
        icon_path = os.path.join(base_path, "Mdev-icon.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Activity bar
        main_layout.addWidget(self.activity_bar)

        # Explorer splitter
        self.explorer_splitter.setHandleWidth(4)
        self.explorer_splitter.setStyleSheet(styles.DARK_SPLITTER_STYLE)
        self.explorer_splitter.splitterMoved.connect(self._on_explorer_splitter_moved)
        self.explorer_splitter.addWidget(self.project_explorer)

        # Inner container for toolbar and editor/preview splitter
        inner_container = self._create_inner_container()
        self.explorer_splitter.addWidget(inner_container)

        main_layout.addWidget(self.explorer_splitter)

        # Status bar
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage('Ready')
        self.status_bar.addPermanentWidget(self.char_count)
        self.status_bar.addPermanentWidget(self.word_count)
        self.status_bar.addPermanentWidget(self.line_count)
        self.auto_save_label.setStyleSheet('color: #999; font-weight: bold;')
        self.status_bar.addPermanentWidget(self.auto_save_label)

        # Menu bar
        self.setMenuBar(self.menu_bar)

        # Connect editor signals
        self.editor.document().contentsChanged.connect(self._on_editor_changed)
        self.editor.setContextMenuPolicy(Qt.CustomContextMenu)
        self.editor.customContextMenuRequested.connect(self.editor_context_menu.show)
        self.preview.setContextMenuPolicy(Qt.CustomContextMenu)
        self.preview.customContextMenuRequested.connect(self.preview_context_menu.show)
        
        # Connect scroll synchronization signals
        self._setup_scroll_sync()

    def _create_inner_container(self):
        """Create the inner container with view toolbar and editor/preview splitter."""
        inner_container = QWidget()
        inner_layout = QVBoxLayout(inner_container)
        inner_layout.setContentsMargins(0, 0, 0, 0)
        inner_layout.setSpacing(0)

        # Add view toolbar at the top
        inner_layout.addWidget(self.app_toolbar)

        # Create editor pane container with toolbar
        self.editor_pane = self._create_editor_pane()

        # Create preview pane container with toolbar
        self.preview_pane = self._create_preview_pane()

        # Editor/preview splitter
        self.splitter.addWidget(self.editor_pane)
        self.splitter.addWidget(self.preview_pane)
        self.splitter.setStretchFactor(0, 1)
        self.splitter.setStretchFactor(1, 1)
        self.splitter.setSizes(constants.DEFAULT_SPLITTER_SIZES)

        inner_layout.addWidget(self.splitter)

        return inner_container

    def _create_editor_pane(self):
        """Create the editor pane container with toolbar inside."""
        editor_pane = QWidget()
        editor_pane_layout = QVBoxLayout(editor_pane)
        editor_pane_layout.setContentsMargins(0, 0, 0, 0)
        editor_pane_layout.setSpacing(0)

        # Add formatting toolbar to the editor pane
        editor_pane_layout.addWidget(self.toolbar)

        # Add editor to the editor pane
        editor_pane_layout.addWidget(self.editor)

        return editor_pane

    def _create_preview_pane(self):
        """Create the preview pane container with toolbar inside."""
        preview_pane = QWidget()
        preview_pane_layout = QVBoxLayout(preview_pane)
        preview_pane_layout.setContentsMargins(0, 0, 0, 0)
        preview_pane_layout.setSpacing(0)

        # Add preview toolbar to the preview pane
        preview_pane_layout.addWidget(self.preview_toolbar)

        # Add preview to the preview pane
        preview_pane_layout.addWidget(self.preview)

        return preview_pane

    def _apply_saved_settings(self):
        """Apply saved settings from previous session."""
        # Apply app theme setting
        app_theme = self.settings.get('app_theme', 'dark')
        self._apply_app_theme(app_theme)

        # Apply dark mode setting (preview only)
        dark_mode = self.settings.get('dark_mode', False)
        self.preview.dark_mode = dark_mode
        self.preview_toolbar.sync_dark_mode_state(dark_mode)

        # Apply pane visibility settings
        editor_visible = self.settings.get('editor_visible', True)
        preview_visible = self.settings.get('preview_visible', True)

        # Ensure at least one pane is visible
        if not editor_visible and not preview_visible:
            editor_visible = True
            preview_visible = True

        self.editor_pane.setVisible(editor_visible)
        self.preview_pane.setVisible(preview_visible)
        self.app_toolbar.sync_editor_state(editor_visible)
        self.app_toolbar.sync_preview_state(preview_visible)

        # Apply window geometry
        window_width = self.settings.get('window_width', constants.DEFAULT_WINDOW_WIDTH)
        window_height = self.settings.get('window_height', constants.DEFAULT_WINDOW_HEIGHT)
        window_x = self.settings.get('window_x', constants.DEFAULT_WINDOW_X)
        window_y = self.settings.get('window_y', constants.DEFAULT_WINDOW_Y)
        self.setGeometry(window_x, window_y, window_width, window_height)

        # Apply splitter sizes
        splitter_sizes = self.settings.get('splitter_sizes', constants.DEFAULT_SPLITTER_SIZES)
        if len(splitter_sizes) == 2:
            self.splitter.setSizes(splitter_sizes)

        # Apply explorer splitter sizes
        explorer_splitter_sizes = self.settings.get(
            'explorer_splitter_sizes',
            constants.DEFAULT_EXPLORER_SPLITTER_SIZES
        )
        if len(explorer_splitter_sizes) == 2:
            self.explorer_splitter.setSizes(explorer_splitter_sizes)

        # Load last opened directory
        last_directory = self.settings.get('last_directory', None)
        if last_directory and os.path.isdir(last_directory):
            self.current_directory = last_directory
            self.project_explorer.set_root_path(last_directory)
            self.project_explorer.show()
            self.project_explorer.raise_()
            self.activity_bar.set_checked(True)
            self.status_bar.showMessage(f'Restored directory: {last_directory}')

        # Update preview
        self._update_preview()

    # ========================================================================
    # Private Event Handlers (internal orchestration only)
    # ========================================================================

    def _on_editor_changed(self):
        """Called when editor content changes."""
        # Debounce the preview update
        if hasattr(self, '_update_timer'):
            self._update_timer.stop()
        else:
            self._update_timer = QTimer(self)
            self._update_timer.setSingleShot(True)
            self._update_timer.timeout.connect(self._update_preview)

        self._update_timer.start(constants.PREVIEW_UPDATE_DELAY_MS)

        # Trigger auto-save after delay
        if self.file_manager.current_file:
            self.auto_save_timer.start(self.auto_save_delay)
        else:
            if self.editor.toPlainText().strip():
                self.status_bar.showMessage('Tip: Save file first (Ctrl+S) to enable auto-save', 5000)

        # Update status bar counts
        text = self.editor.toPlainText()
        self.char_count.setText(f'Characters: {len(text)}')
        self.word_count.setText(f'Words: {len(text.split())}')
        self.line_count.setText(f'Lines: {text.count(chr(10)) + 1}')

    def _auto_save(self):
        """Auto-save the current file if one is open."""
        if not self.file_manager.current_file:
            if self.editor.toPlainText().strip():
                self.status_bar.showMessage('Please save the file first (Ctrl+S)', 3000)
            else:
                self.status_bar.showMessage('No content to save', 3000)
            return

        if not self.file_manager.auto_save_current_file():
            self.status_bar.showMessage('✗ Auto-save failed', 5000)
            return

        self.status_bar.showMessage('✓ Auto-saved: ' + os.path.basename(self.file_manager.current_file), 3000)

    def _update_preview(self):
        """Update the markdown preview."""
        markdown_text = self.editor.toPlainText()
        self.preview.update_preview(markdown_text)

    def _setup_scroll_sync(self):
        """Set up synchronous scrolling between editor and preview panes."""
        # Connect editor scroll changes to preview
        self.editor.scroll_position_changed.connect(self._on_editor_scrolled)
        
        # Connect preview scroll changes to editor
        self.preview.scroll_position_changed.connect(self._on_preview_scrolled)
        
        # Connect editor vertical scrollbar directly for real-time sync
        self.editor.verticalScrollBar().valueChanged.connect(self._sync_preview_from_editor)
    
    def _on_editor_scrolled(self, scroll_ratio_1000):
        """Handle editor scroll position changes - sync to preview."""
        # Get current editor scroll info
        max_scroll = self.editor.verticalScrollBar().maximum()
        current_value = self.editor.verticalScrollBar().value()
        
        # Sync preview to match
        self.preview.sync_scroll_from_editor(current_value, max_scroll)
    
    def _sync_preview_from_editor(self, scroll_value):
        """Real-time sync of preview when editor scrollbar changes."""
        max_scroll = self.editor.verticalScrollBar().maximum()
        self.preview.sync_scroll_from_editor(scroll_value, max_scroll)
    
    def _on_preview_scrolled(self, scroll_ratio_1000):
        """Handle preview scroll position changes - sync to editor."""
        # Sync editor to match preview scroll ratio
        self.editor.sync_scroll_from_preview(scroll_ratio_1000)

    def update_auto_save_status(self):
        """Update the auto-save status indicator."""
        if self.file_manager.current_file:
            self.auto_save_label.setText('Auto-save: ON')
            self.auto_save_label.setStyleSheet('color: #4CAF50; font-weight: bold;')
        else:
            self.auto_save_label.setText('Auto-save: OFF')
            self.auto_save_label.setStyleSheet('color: #999; font-weight: bold;')

    def _save_current_settings(self):
        """Save current settings."""
        self.settings.set('app_theme', self.current_theme)
        self.settings.set('dark_mode', self.preview.dark_mode)
        self.settings.set('editor_visible', self.editor_pane.isVisible())
        self.settings.set('preview_visible', self.preview_pane.isVisible())

        geometry = self.geometry()
        self.settings.set('window_width', geometry.width())
        self.settings.set('window_height', geometry.height())
        self.settings.set('window_x', geometry.x())
        self.settings.set('window_y', geometry.y())

        if self.splitter.sizes():
            self.settings.set('splitter_sizes', self.splitter.sizes())

        if self.explorer_splitter.sizes():
            self.settings.set('explorer_splitter_sizes', self.explorer_splitter.sizes())

        self.settings.save_settings()

    def _on_explorer_splitter_moved(self, positions, orientation):
        """Handle explorer splitter resize with debounced save."""
        if hasattr(self, '_explorer_save_timer'):
            self._explorer_save_timer.stop()
        else:
            self._explorer_save_timer = QTimer(self)
            self._explorer_save_timer.setSingleShot(True)
            self._explorer_save_timer.timeout.connect(self._save_current_settings)

        self._explorer_save_timer.start(constants.EXPLORER_SAVE_DELAY_MS)

    def _apply_app_theme(self, theme):
        """Apply theme to all panels and window bars except preview pane."""
        self.current_theme = theme
        if theme == 'dark':
            self.editor.set_theme('dark')
            self.activity_bar.set_theme('dark')
            self.explorer_splitter.setStyleSheet(styles.DARK_SPLITTER_STYLE)
            self.splitter.setStyleSheet(styles.DARK_SPLITTER_STYLE)
            self.project_explorer.set_theme('dark')
            self.toolbar.set_theme('dark')
            self.app_toolbar.set_theme('dark')
            self.preview_toolbar.set_theme('dark')
            self.menu_bar.set_theme('dark')
            self.status_bar.setStyleSheet(styles.DARK_STATUS_BAR_STYLE)
            self.setStyleSheet(styles.DARK_MAIN_WINDOW_STYLE)
        else:
            self.editor.set_theme('light')
            self.activity_bar.set_theme('light')
            self.explorer_splitter.setStyleSheet(styles.LIGHT_SPLITTER_STYLE)
            self.splitter.setStyleSheet(styles.LIGHT_SPLITTER_STYLE)
            self.project_explorer.set_theme('light')
            self.toolbar.set_theme('light')
            self.app_toolbar.set_theme('light')
            self.preview_toolbar.set_theme('light')
            self.menu_bar.set_theme('light')
            self.status_bar.setStyleSheet(styles.LIGHT_STATUS_BAR_STYLE)
            self.setStyleSheet(styles.LIGHT_MAIN_WINDOW_STYLE)

    # ========================================================================
    # Public API (called by components)
    # ========================================================================

    def open_directory(self, directory):
        """Open a directory in the project explorer (called by components)."""
        self.current_directory = directory
        self.project_explorer.set_root_path(directory)
        self.project_explorer.show()
        self.project_explorer.raise_()
        self.activity_bar.set_checked(True)
        self.status_bar.showMessage(f'Opened directory: {directory}')
        self.settings.set('last_directory', directory)
        self.settings.save_settings()

    def toggle_project_explorer(self):
        """Toggle the project explorer panel visibility."""
        if self.project_explorer.isVisible():
            self.project_explorer.hide()
            self.activity_bar.set_checked(False)
        else:
            self.project_explorer.show()
            self.project_explorer.raise_()
            self.activity_bar.set_checked(True)
            if not self.explorer_splitter.sizes():
                self.explorer_splitter.setSizes(constants.DEFAULT_EXPLORER_SPLITTER_SIZES)

    def toggle_view_toolbar(self):
        """Toggle the view toolbar visibility."""
        if self.app_toolbar.isVisible():
            self.app_toolbar.hide()
            self.status_bar.showMessage('View toolbar: Hidden')
        else:
            self.app_toolbar.show()
            self.status_bar.showMessage('View toolbar: Visible')

    def toggle_dark_mode(self, dark_mode):
        """Toggle dark mode for preview."""
        self.preview.dark_mode = dark_mode
        self.preview_toolbar.sync_dark_mode_state(dark_mode)
        markdown_text = self.editor.toPlainText()
        self.preview.update_preview(markdown_text)
        self.status_bar.showMessage('Dark mode: ' + ('ON' if dark_mode else 'OFF'))
        self._save_current_settings()

    def toggle_app_theme(self, is_dark):
        """Toggle app theme between light and dark."""
        self._apply_app_theme('dark' if is_dark else 'light')
        theme_name = 'Dark' if is_dark else 'Light'
        self.status_bar.showMessage(f'App theme: {theme_name}')
        self._save_current_settings()

    def toggle_editor_pane(self, editor_visible):
        """Toggle the editor pane visibility."""
        self.editor_pane.setVisible(editor_visible)
        self.app_toolbar.sync_editor_state(editor_visible)
        self.status_bar.showMessage('Editor pane: ' + ('Visible' if editor_visible else 'Hidden'))

        if not editor_visible and not self.preview_pane.isVisible():
            self.preview_pane.setVisible(True)
            self.app_toolbar.sync_preview_state(True)

        self._save_current_settings()

    def toggle_preview_pane(self, preview_visible):
        """Toggle the preview pane visibility."""
        self.preview_pane.setVisible(preview_visible)
        self.app_toolbar.sync_preview_state(preview_visible)
        self.status_bar.showMessage('Preview pane: ' + ('Visible' if preview_visible else 'Hidden'))

        if not preview_visible and not self.editor_pane.isVisible():
            self.editor_pane.setVisible(True)
            self.app_toolbar.sync_editor_state(True)

        self._save_current_settings()

    def swap_pane_positions(self):
        """Swap editor and preview pane positions."""
        # Get current widgets from splitter
        editor_widget = self.splitter.widget(0)
        preview_widget = self.splitter.widget(1)

        # Get current sizes to restore later
        current_sizes = self.splitter.sizes()

        # We need to swap the widgets. Since they're siblings in the splitter,
        # we use replaceWidget with a temporary intermediate widget.
        # Create a dummy widget to use as an intermediary
        from PyQt5.QtWidgets import QWidget
        dummy = QWidget()

        # Step 1: Replace editor (index 0) with dummy
        self.splitter.replaceWidget(0, dummy)

        # Step 2: Replace preview (index 1) with editor
        self.splitter.replaceWidget(1, editor_widget)

        # Step 3: Replace dummy (index 0) with preview
        self.splitter.replaceWidget(0, preview_widget)

        # Clean up dummy widget
        dummy.deleteLater()

        # Restore sizes (swap them since positions swapped)
        self.splitter.setSizes([current_sizes[1], current_sizes[0]])

        self.status_bar.showMessage('Pane positions swapped')

    def on_file_double_clicked(self, index):
        """Handle double-click on a file in the project explorer."""
        file_path = self.project_explorer.file_model.fileInfo(index).absoluteFilePath()

        if os.path.isfile(file_path):
            # Auto-save current file if there are changes
            if not self.file_manager.auto_save_current_file():
                from PyQt5.QtWidgets import QMessageBox
                QMessageBox.critical(self, 'Error', 'Could not auto-save file.')
                return

            # Open the selected file
            success, content, error = self.file_manager.open_file(file_path)
            if success:
                self.current_directory = os.path.dirname(file_path)
                self._update_preview()
            else:
                from PyQt5.QtWidgets import QMessageBox
                QMessageBox.critical(self, 'Error', f'Could not open file:\n{error}')

    # ========================================================================
    # Window Events
    # ========================================================================

    def closeEvent(self, event):
        """Handle window close event."""
        from PyQt5.QtWidgets import QMessageBox

        result = self.file_manager.handle_unsaved_changes(self, 'closing')

        if result == 'save':
            if not self.file_manager.save_file_as(self):
                event.ignore()
                return
        elif not result:
            event.ignore()
            return

        if self.file_manager.current_file and self.editor.document().isModified():
            if not self.file_manager.auto_save_current_file():
                QMessageBox.critical(
                    self, 'Error',
                    'Could not auto-save file.\n\nYour changes may be lost.'
                )
                event.ignore()
                return

        self._save_current_settings()
