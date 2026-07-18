"""
Menu Bar Component for MDEV

Handles its own events and delegates to main_window/file_manager only for state changes.
"""

from PyQt5.QtWidgets import QMenuBar, QAction

import constants
import styles
from components.dialogs import show_about_dialog, show_license_dialog


class MenuBar(QMenuBar):
    """Application menu bar."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.setup_ui()

    def setup_ui(self):
        """Setup the menu bar."""
        self._setup_file_menu()
        self._setup_edit_menu()
        self._setup_view_menu()
        self._setup_help_menu()
        self.setStyleSheet(styles.DARK_MENU_BAR_STYLE)

    def _setup_file_menu(self):
        """Setup File menu."""
        file_menu = self.addMenu('File')

        new_action = QAction('New', self)
        new_action.setShortcut(constants.SHORTCUTS['new'])
        new_action.triggered.connect(self._on_new_file)
        file_menu.addAction(new_action)

        open_action = QAction('Open', self)
        open_action.setShortcut(constants.SHORTCUTS['open'])
        open_action.triggered.connect(self._on_open_file)
        file_menu.addAction(open_action)

        save_action = QAction('Save', self)
        save_action.setShortcut(constants.SHORTCUTS['save'])
        save_action.triggered.connect(self._on_save_file)
        file_menu.addAction(save_action)

        save_as_action = QAction('Save As', self)
        save_as_action.setShortcut(constants.SHORTCUTS['save_as'])
        save_as_action.triggered.connect(self._on_save_file_as)
        file_menu.addAction(save_as_action)

        file_menu.addSeparator()

        # Project explorer actions
        open_dir_action = QAction('Open Directory...', self)
        open_dir_action.setShortcut(constants.SHORTCUTS['open_directory'])
        open_dir_action.triggered.connect(self._on_open_directory)
        file_menu.addAction(open_dir_action)

        new_file_action = QAction('New File in Directory', self)
        new_file_action.setShortcut(constants.SHORTCUTS['new_file_in_dir'])
        new_file_action.triggered.connect(self._on_new_file_in_dir)
        file_menu.addAction(new_file_action)

        new_folder_action = QAction('New Folder in Directory', self)
        new_folder_action.setShortcut(constants.SHORTCUTS['new_folder_in_dir'])
        new_folder_action.triggered.connect(self._on_new_folder_in_dir)
        file_menu.addAction(new_folder_action)

        file_menu.addSeparator()

        # Manual auto-save trigger
        auto_save_now_action = QAction('Auto-Save Now', self)
        auto_save_now_action.setShortcut(constants.SHORTCUTS['auto_save_now'])
        auto_save_now_action.triggered.connect(self._on_auto_save_now)
        file_menu.addAction(auto_save_now_action)

        file_menu.addSeparator()

        exit_action = QAction('Exit', self)
        exit_action.setShortcut(constants.SHORTCUTS['exit'])
        exit_action.triggered.connect(self._on_exit)
        file_menu.addAction(exit_action)

    def _setup_edit_menu(self):
        """Setup Edit menu."""
        edit_menu = self.addMenu('Edit')

        undo_action = QAction('Undo', self)
        undo_action.setShortcut(constants.SHORTCUTS['undo'])
        undo_action.triggered.connect(self._on_undo)
        edit_menu.addAction(undo_action)

        redo_action = QAction('Redo', self)
        redo_action.setShortcut(constants.SHORTCUTS['redo'])
        redo_action.triggered.connect(self._on_redo)
        edit_menu.addAction(redo_action)

        edit_menu.addSeparator()

        cut_action = QAction('Cut', self)
        cut_action.setShortcut(constants.SHORTCUTS['cut'])
        cut_action.triggered.connect(self._on_cut)
        edit_menu.addAction(cut_action)

        copy_action = QAction('Copy', self)
        copy_action.setShortcut(constants.SHORTCUTS['copy'])
        copy_action.triggered.connect(self._on_copy)
        edit_menu.addAction(copy_action)

        paste_action = QAction('Paste', self)
        paste_action.setShortcut(constants.SHORTCUTS['paste'])
        paste_action.triggered.connect(self._on_paste)
        edit_menu.addAction(paste_action)

    def _setup_view_menu(self):
        """Setup View menu."""
        view_menu = self.addMenu('View')

        toggle_preview_action = QAction('Toggle Preview Pane', self)
        toggle_preview_action.setShortcut(constants.SHORTCUTS['toggle_preview'])
        toggle_preview_action.triggered.connect(self._on_toggle_preview)
        view_menu.addAction(toggle_preview_action)

        toggle_editor_action = QAction('Toggle Editor Pane', self)
        toggle_editor_action.setShortcut(constants.SHORTCUTS['toggle_editor'])
        toggle_editor_action.triggered.connect(self._on_toggle_editor)
        view_menu.addAction(toggle_editor_action)

        toggle_dark_mode_action = QAction('Toggle Dark Preview', self)
        toggle_dark_mode_action.setShortcut(constants.SHORTCUTS['toggle_dark_mode'])
        toggle_dark_mode_action.triggered.connect(self._on_toggle_dark_mode)
        view_menu.addAction(toggle_dark_mode_action)

        toggle_app_theme_action = QAction('Toggle App Theme (Light/Dark)', self)
        toggle_app_theme_action.setShortcut(constants.SHORTCUTS['toggle_app_theme'])
        toggle_app_theme_action.triggered.connect(self._on_toggle_app_theme)
        view_menu.addAction(toggle_app_theme_action)

        view_menu.addSeparator()

        toggle_view_toolbar_action = QAction('Toggle View Toolbar', self)
        toggle_view_toolbar_action.setShortcut('Ctrl+T')
        toggle_view_toolbar_action.triggered.connect(self._on_toggle_view_toolbar)
        view_menu.addAction(toggle_view_toolbar_action)

        view_menu.addSeparator()

        toggle_project_explorer_action = QAction('Toggle Project Explorer', self)
        toggle_project_explorer_action.setShortcut(constants.SHORTCUTS['toggle_explorer'])
        toggle_project_explorer_action.triggered.connect(self._on_toggle_explorer)
        view_menu.addAction(toggle_project_explorer_action)

    def _setup_help_menu(self):
        """Setup Help menu."""
        help_menu = self.addMenu('Help')

        about_action = QAction('About MDEV', self)
        about_action.triggered.connect(self._on_show_about)
        help_menu.addAction(about_action)

        license_action = QAction('View License', self)
        license_action.triggered.connect(self._on_show_license)
        help_menu.addAction(license_action)

    # ========================================================================
    # Private Event Handlers - handle events directly
    # ========================================================================

    def _on_new_file(self):
        """Create a new file."""
        if self.parent_window and hasattr(self.parent_window, 'file_manager'):
            self.parent_window.file_manager.new_file(self.parent_window)

    def _on_open_file(self):
        """Open a file."""
        if self.parent_window and hasattr(self.parent_window, 'file_manager'):
            self.parent_window.file_manager.open_file_dialog(self.parent_window)

    def _on_save_file(self):
        """Save the current file."""
        if self.parent_window and hasattr(self.parent_window, 'file_manager'):
            self.parent_window.file_manager.save_file(self.parent_window)

    def _on_save_file_as(self):
        """Save the file with a new name."""
        if self.parent_window and hasattr(self.parent_window, 'file_manager'):
            self.parent_window.file_manager.save_file_as(self.parent_window)

    def _on_open_directory(self):
        """Open a directory in the explorer."""
        if self.parent_window:
            self._open_directory_dialog()

    def _open_directory_dialog(self):
        """Show directory dialog and open selected directory."""
        from utils.file_ops import open_directory_dialog
        directory = open_directory_dialog(self.parent_window)
        if directory:
            self.parent_window.open_directory(directory)

    def _on_new_file_in_dir(self):
        """Create a new file in the current directory."""
        if self.parent_window and hasattr(self.parent_window, 'project_explorer'):
            self.parent_window.project_explorer.on_new_file()

    def _on_new_folder_in_dir(self):
        """Create a new folder in the current directory."""
        if self.parent_window and hasattr(self.parent_window, 'project_explorer'):
            self.parent_window.project_explorer.on_new_folder()

    def _on_auto_save_now(self):
        """Trigger auto-save now."""
        if self.parent_window:
            self.parent_window._auto_save()

    def _on_exit(self):
        """Close the application."""
        if self.parent_window:
            self.parent_window.close()

    def _on_undo(self):
        """Undo in editor."""
        if self.parent_window and hasattr(self.parent_window, 'editor'):
            self.parent_window.editor.undo()

    def _on_redo(self):
        """Redo in editor."""
        if self.parent_window and hasattr(self.parent_window, 'editor'):
            self.parent_window.editor.redo()

    def _on_cut(self):
        """Cut from editor."""
        if self.parent_window and hasattr(self.parent_window, 'editor'):
            self.parent_window.editor.cut()

    def _on_copy(self):
        """Copy from editor."""
        if self.parent_window and hasattr(self.parent_window, 'editor'):
            self.parent_window.editor.copy()

    def _on_paste(self):
        """Paste into editor."""
        if self.parent_window and hasattr(self.parent_window, 'editor'):
            self.parent_window.editor.paste()

    def _on_toggle_preview(self):
        """Toggle preview pane."""
        if self.parent_window:
            self.parent_window.toggle_preview_pane(not self.parent_window.preview.isVisible())

    def _on_toggle_editor(self):
        """Toggle editor pane."""
        if self.parent_window:
            self.parent_window.toggle_editor_pane(not self.parent_window.editor_pane.isVisible())

    def _on_toggle_dark_mode(self):
        """Toggle dark mode."""
        if self.parent_window:
            dark_mode = not self.parent_window.preview.dark_mode
            self.parent_window.toggle_dark_mode(dark_mode)

    def _on_toggle_app_theme(self):
        """Toggle app theme."""
        if self.parent_window:
            is_dark = self.parent_window.current_theme == 'dark'
            self.parent_window.toggle_app_theme(not is_dark)

    def _on_toggle_explorer(self):
        """Toggle project explorer."""
        if self.parent_window:
            self.parent_window.toggle_project_explorer()

    def _on_toggle_view_toolbar(self):
        """Toggle view toolbar visibility."""
        if self.parent_window:
            self.parent_window.toggle_view_toolbar()

    def _on_show_about(self):
        """Show about dialog."""
        if self.parent_window:
            show_about_dialog(self.parent_window)

    def _on_show_license(self):
        """Show license dialog."""
        if self.parent_window:
            show_license_dialog(self.parent_window)

    # ========================================================================
    # Theme Management
    # ========================================================================

    def set_theme(self, theme):
        """Apply theme to menu bar."""
        if theme == 'dark':
            self.setStyleSheet(styles.DARK_MENU_BAR_STYLE)
        else:
            self.setStyleSheet(styles.LIGHT_MENU_BAR_STYLE)
