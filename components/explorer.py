"""
Project Explorer Component for MDEV

Handles its own events including file operations and tree interactions.
"""

import os
import shutil
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QToolBar, QAction, QTreeView,
    QFileSystemModel, QMenu, QMessageBox, QInputDialog
)
from PyQt5.QtCore import Qt, QSize, QDir

import constants
import styles


class ProjectExplorer(QWidget):
    """Project explorer panel with file tree and toolbar."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.current_directory = None
        self.file_model = None
        self.file_tree = None
        self.explorer_toolbar = None
        self.setup_ui()

    def setup_ui(self):
        """Setup the project explorer UI."""
        self.setMinimumWidth(constants.EXPLORER_MIN_WIDTH)
        self.setMaximumWidth(constants.EXPLORER_MAX_WIDTH)
        self.setSizePolicy(self.sizePolicy().horizontalPolicy(), self.sizePolicy().verticalPolicy())
        self.setStyleSheet(styles.DARK_EXPLORER_PANEL_STYLE)

        explorer_layout = QVBoxLayout(self)
        explorer_layout.setContentsMargins(0, 0, 0, 0)
        explorer_layout.setSpacing(0)

        # Create toolbar
        self._setup_toolbar()
        explorer_layout.addWidget(self.explorer_toolbar)

        # Create tree view
        self._setup_tree_view()
        explorer_layout.addWidget(self.file_tree)

        # Hide by default
        self.hide()

    def _setup_toolbar(self):
        """Setup the explorer toolbar."""
        self.explorer_toolbar = QToolBar('Explorer', self)
        self.explorer_toolbar.setMovable(False)
        self.explorer_toolbar.setIconSize(QSize(16, 16))
        self.explorer_toolbar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.explorer_toolbar.setStyleSheet(styles.DARK_EXPLORER_TOOLBAR_STYLE)

        # Open Directory action
        open_dir_action = QAction('📂', self)
        open_dir_action.setToolTip('Open a directory in the explorer')
        open_dir_action.triggered.connect(self._on_open_directory)
        self.explorer_toolbar.addAction(open_dir_action)

        # New File action
        new_file_action = QAction('📄', self)
        new_file_action.setToolTip('Create a new file in the current directory')
        new_file_action.triggered.connect(self.on_new_file)
        self.explorer_toolbar.addAction(new_file_action)

        # New Folder action
        new_folder_action = QAction('📁', self)
        new_folder_action.setToolTip('Create a new folder in the current directory')
        new_folder_action.triggered.connect(self.on_new_folder)
        self.explorer_toolbar.addAction(new_folder_action)

        # Find Current File action
        find_file_action = QAction('𖦏', self)
        find_file_action.setToolTip('Locate the currently opened file in the tree')
        find_file_action.triggered.connect(self._on_find_current_file)
        self.explorer_toolbar.addAction(find_file_action)

        # Rename action
        rename_action = QAction('🖋️', self)
        rename_action.setToolTip('Rename selected file or folder')
        rename_action.triggered.connect(self._on_rename)
        self.explorer_toolbar.addAction(rename_action)

        # Delete action
        delete_action = QAction('🗑️', self)
        delete_action.setToolTip('Delete selected file or folder')
        delete_action.triggered.connect(self._on_delete)
        self.explorer_toolbar.addAction(delete_action)

    def _setup_tree_view(self):
        """Setup the file tree view."""
        self.file_tree = QTreeView()
        self.file_model = QFileSystemModel(self)
        self.file_model.setFilter(QDir.AllEntries | QDir.NoDotAndDotDot)

        self.file_tree.setModel(self.file_model)
        self.file_tree.setHeaderHidden(True)
        self.file_tree.setAnimated(True)
        self.file_tree.setIndentation(20)
        self.file_tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.file_tree.customContextMenuRequested.connect(self._show_context_menu)
        self.file_tree.setStyleSheet(styles.DARK_FILE_TREE_STYLE)

        # Show only the first column
        self.file_tree.setColumnHidden(1, True)
        self.file_tree.setColumnHidden(2, True)
        self.file_tree.setColumnHidden(3, True)

        # Expand to 2 levels by default
        self.file_tree.expandToDepth(2)

        # Connect double-click to open file
        self.file_tree.doubleClicked.connect(self._on_file_double_clicked)

    # ========================================================================
    # Toolbar Action Handlers
    # ========================================================================

    def _on_open_directory(self):
        """Handle open directory action."""
        from utils.file_ops import open_directory_dialog
        directory = open_directory_dialog(self)
        if directory and self.parent_window:
            self.parent_window.open_directory(directory)

    def on_new_file(self):
        """Handle new file action (public for menu access)."""
        target_dir = self._get_target_directory_for_new_item()
        self._new_file_in_directory(target_dir)

    def on_new_folder(self):
        """Handle new folder action (public for menu access)."""
        target_dir = self._get_target_directory_for_new_item()
        self._new_folder_in_directory(target_dir)

    def _on_find_current_file(self):
        """Handle find current file action."""
        self._find_current_file_in_tree()

    def _on_rename(self):
        """Handle rename action."""
        self._rename_selected_item()

    def _on_delete(self):
        """Handle delete action."""
        self._delete_selected_item()

    # ========================================================================
    # Tree View Handlers
    # ========================================================================

    def _on_file_double_clicked(self, index):
        """Handle double-click on a file."""
        if self.parent_window:
            self.parent_window.on_file_double_clicked(index)

    # ========================================================================
    # Context Menu
    # ========================================================================

    def _show_context_menu(self, position):
        """Show context menu for the file tree."""
        if not self.current_directory:
            return

        index = self.file_tree.indexAt(position)

        if not index.isValid():
            root_index = self.file_model.index(self.current_directory)
            self.file_tree.setCurrentIndex(root_index)
            index = root_index
        else:
            self.file_tree.setCurrentIndex(index)

        file_path = self.file_model.fileInfo(index).absoluteFilePath()
        is_directory = os.path.isdir(file_path) if file_path else False

        context_menu = QMenu(self)
        self._apply_context_menu_style(context_menu)

        # New File action
        new_file_action = QAction('📄 New File', self)
        target_dir = file_path if is_directory else os.path.dirname(file_path) if file_path else self.current_directory
        new_file_action.triggered.connect(lambda: self._new_file_in_directory(target_dir))
        context_menu.addAction(new_file_action)

        # New Folder action
        new_folder_action = QAction('📁 New Folder', self)
        new_folder_action.triggered.connect(lambda: self._new_folder_in_directory(target_dir))
        context_menu.addAction(new_folder_action)

        context_menu.addSeparator()

        # Rename action
        rename_action = QAction('✏️ Rename', self)
        rename_action.triggered.connect(self._rename_selected_item)
        context_menu.addAction(rename_action)

        # Delete action
        delete_action = QAction('🗑️ Delete', self)
        delete_action.triggered.connect(self._delete_selected_item)
        context_menu.addAction(delete_action)

        context_menu.exec_(self.file_tree.viewport().mapToGlobal(position))

    def _apply_context_menu_style(self, menu):
        """Apply theme-appropriate style to context menu."""
        if self.parent_window and hasattr(self.parent_window, 'current_theme'):
            if self.parent_window.current_theme == 'dark':
                menu.setStyleSheet(styles.DARK_CONTEXT_MENU_STYLE)
            else:
                menu.setStyleSheet(styles.LIGHT_CONTEXT_MENU_STYLE)
        else:
            menu.setStyleSheet(styles.DARK_CONTEXT_MENU_STYLE)

    # ========================================================================
    # File Operations
    # ========================================================================

    def _rename_selected_item(self):
        """Rename the selected file or folder."""
        selected_index = self.file_tree.currentIndex()

        if not selected_index.isValid():
            QMessageBox.information(self, 'No Selection', 'Please select a file or folder to rename.')
            return

        file_path = self.file_model.fileInfo(selected_index).absoluteFilePath()

        if not file_path:
            QMessageBox.warning(self, 'Error', 'Could not get the selected item path.')
            return

        current_name = os.path.basename(file_path)

        new_name, ok = QInputDialog.getText(self, 'Rename', 'Enter new name:', text=current_name)

        if ok and new_name and new_name != current_name:
            parent_dir = os.path.dirname(file_path)
            new_path = os.path.join(parent_dir, new_name)

            try:
                if os.path.exists(new_path):
                    QMessageBox.warning(self, 'Error', f'A file or folder with the name "{new_name}" already exists.')
                    return

                os.rename(file_path, new_path)

                self.file_model.setRootPath(self.current_directory)

                # Update parent window if needed
                if self.parent_window and hasattr(self.parent_window, 'current_file') and self.parent_window.current_file == file_path:
                    self.parent_window.current_file = new_path
                    self.parent_window.setWindowTitle(f'{constants.APP_NAME} - {new_name}')

                if self.parent_window and hasattr(self.parent_window, 'status_bar'):
                    self.parent_window.status_bar.showMessage(f'Renamed to: {new_name}')

            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Could not rename:\n{str(e)}')

    def _delete_selected_item(self):
        """Delete the selected file or folder."""
        selected_index = self.file_tree.currentIndex()

        if not selected_index.isValid():
            QMessageBox.information(self, 'No Selection', 'Please select a file or folder to delete.')
            return

        file_path = self.file_model.fileInfo(selected_index).absoluteFilePath()

        if not file_path:
            QMessageBox.warning(self, 'Error', 'Could not get the selected item path.')
            return

        item_name = os.path.basename(file_path)
        is_directory = os.path.isdir(file_path)
        item_type = 'folder' if is_directory else 'file'

        reply = QMessageBox.question(
            self,
            'Confirm Delete',
            f'Are you sure you want to delete the {item_type} "{item_name}"?\n\nThis action cannot be undone.',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            try:
                if is_directory:
                    shutil.rmtree(file_path)
                else:
                    os.remove(file_path)

                self.file_model.setRootPath(self.current_directory)

                # Clear current file if it was deleted
                if self.parent_window and hasattr(self.parent_window, 'current_file') and self.parent_window.current_file == file_path:
                    self.parent_window.current_file = None
                    if hasattr(self.parent_window, 'editor'):
                        self.parent_window.editor.clear()
                        self.parent_window.editor.document().setModified(False)
                    self.parent_window.setWindowTitle(constants.APP_NAME)

                if self.parent_window and hasattr(self.parent_window, 'status_bar'):
                    self.parent_window.status_bar.showMessage(f'Deleted: {item_name}')

            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Could not delete:\n{str(e)}')

    def _find_current_file_in_tree(self):
        """Find and select the currently opened file."""
        if not self.parent_window:
            return

        if not hasattr(self.parent_window, 'current_file') or not self.parent_window.current_file:
            QMessageBox.information(self, 'No File Open', 'No file is currently open.')
            return

        if not self.current_directory:
            QMessageBox.information(self, 'No Directory Open', 'No directory is currently open in the explorer.')
            return

        file_index = self.file_model.index(self.parent_window.current_file)

        if not file_index.isValid():
            QMessageBox.warning(self, 'File Not Found', 'The current file is not in the opened directory.')
            return

        parent = file_index.parent()
        while parent.isValid():
            self.file_tree.expand(parent)
            parent = parent.parent()

        self.file_tree.setCurrentIndex(file_index)
        self.file_tree.scrollTo(file_index)

        if self.parent_window and hasattr(self.parent_window, 'status_bar'):
            self.parent_window.status_bar.showMessage(f'Located: {os.path.basename(self.parent_window.current_file)}')

    # ========================================================================
    # File Creation Methods
    # ========================================================================

    def _new_file_in_directory(self, target_directory=None):
        """Create a new file in the specified directory."""
        if target_directory is None:
            target_directory = self._get_target_directory_for_new_item()

        if not target_directory:
            QMessageBox.information(self, 'No Directory Open', 'Please open a directory first using File → Open Directory')
            return

        file_name, ok = QInputDialog.getText(self, 'New File', 'Enter file name:', text='untitled.md')

        if ok and file_name:
            # Ensure .md extension
            if not file_name.endswith(('.md', '.markdown')):
                file_name += '.md'

            file_path = os.path.join(target_directory, file_name)

            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write('')

                self.file_model.setRootPath(self.current_directory)

                if self.parent_window:
                    if hasattr(self.parent_window, 'current_file'):
                        self.parent_window.current_file = file_path
                    if hasattr(self.parent_window, 'editor'):
                        self.parent_window.editor.clear()
                        self.parent_window.editor.document().setModified(False)
                    self.parent_window.setWindowTitle(f'{constants.APP_NAME} - {file_name}')
                    if hasattr(self.parent_window, 'status_bar'):
                        self.parent_window.status_bar.showMessage(f'Created new file: {file_name}')
                    if hasattr(self.parent_window, 'update_auto_save_status'):
                        self.parent_window.update_auto_save_status()

            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Could not create file:\n{str(e)}')

    def _new_folder_in_directory(self, target_directory=None):
        """Create a new folder in the specified directory."""
        if target_directory is None:
            target_directory = self._get_target_directory_for_new_item()

        if not target_directory:
            QMessageBox.information(self, 'No Directory Open', 'Please open a directory first using File → Open Directory')
            return

        folder_name, ok = QInputDialog.getText(self, 'New Folder', 'Enter folder name:')

        if ok and folder_name:
            folder_path = os.path.join(target_directory, folder_name)

            try:
                os.makedirs(folder_path, exist_ok=True)

                self.file_model.setRootPath(self.current_directory)

                if self.parent_window and hasattr(self.parent_window, 'status_bar'):
                    self.parent_window.status_bar.showMessage(f'Created folder: {folder_name}')

            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Could not create folder:\n{str(e)}')

    # ========================================================================
    # Theme and State Management
    # ========================================================================

    def set_theme(self, theme):
        """Apply theme to explorer."""
        if theme == 'dark':
            self.setStyleSheet(styles.DARK_EXPLORER_PANEL_STYLE)
            self.explorer_toolbar.setStyleSheet(styles.DARK_EXPLORER_TOOLBAR_STYLE)
            self.file_tree.setStyleSheet(styles.DARK_FILE_TREE_STYLE)
        else:
            self.setStyleSheet(styles.LIGHT_EXPLORER_PANEL_STYLE)
            self.explorer_toolbar.setStyleSheet(styles.LIGHT_EXPLORER_TOOLBAR_STYLE)
            self.file_tree.setStyleSheet(styles.LIGHT_FILE_TREE_STYLE)

    def set_root_path(self, path):
        """Set the root path for the file model."""
        self.current_directory = path
        self.file_model.setRootPath(path)
        self.file_tree.setRootIndex(self.file_model.index(path))

    def _get_target_directory_for_new_item(self):
        """Get the target directory for creating new items."""
        if not self.current_directory:
            return None

        selected_indexes = self.file_tree.selectedIndexes()

        if selected_indexes:
            selected_index = selected_indexes[0]
            file_path = self.file_model.fileInfo(selected_index).absoluteFilePath()
            if file_path:
                if os.path.isdir(file_path):
                    return file_path
                return os.path.dirname(file_path)

        selected_index = self.file_tree.currentIndex()
        if selected_index.isValid():
            file_path = self.file_model.fileInfo(selected_index).absoluteFilePath()
            if file_path:
                if os.path.isdir(file_path):
                    return file_path
                return os.path.dirname(file_path)

        return self.current_directory
