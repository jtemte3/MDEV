"""
File Operations Utility
"""

import os
from PyQt5.QtWidgets import QFileDialog, QMessageBox

import constants


def open_file_dialog(parent):
    """Open a file dialog and return the selected file path"""
    file_path, _ = QFileDialog.getOpenFileName(
        parent,
        'Open Markdown File',
        '',
        'Markdown Files (*.md *.markdown *.txt);;All Files (*)'
    )
    return file_path


def save_file_dialog(parent):
    """Open a save file dialog and return the selected file path"""
    file_path, _ = QFileDialog.getSaveFileName(
        parent,
        'Save Markdown File',
        '',
        'Markdown Files (*.md);;All Files (*)'
    )
    if file_path and not file_path.endswith('.md'):
        file_path += '.md'
    return file_path


def open_directory_dialog(parent):
    """Open a directory dialog and return the selected directory path"""
    directory = QFileDialog.getExistingDirectory(
        parent,
        'Open Directory',
        '',
        QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
    )
    return directory


def read_file_content(file_path):
    """Read content from a file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read(), None
    except Exception as e:
        return None, str(e)


def write_file_content(file_path, content):
    """Write content to a file"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True, None
    except Exception as e:
        return False, str(e)


def show_error_message(parent, title, message):
    """Show an error message box"""
    QMessageBox.critical(parent, title, message)


def show_unsaved_changes_dialog(parent, message='You have unsaved changes. Do you want to save them?'):
    """Show dialog for unsaved changes"""
    reply = QMessageBox.question(
        parent, 'Unsaved Changes',
        message,
        QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
        QMessageBox.Save
    )
    return reply


def ensure_markdown_extension(file_name):
    """Ensure the file name has a markdown extension"""
    if not file_name.endswith(constants.MARKDOWN_EXTENSIONS):
        file_name += '.md'
    return file_name


# ========================================================================
# File Manager Class - Handles file operation business logic
# ========================================================================

class FileManager:
    """Manages file operations for the markdown editor"""
    
    def __init__(self, editor, main_window=None):
        """
        Initialize FileManager
        
        Args:
            editor: The QTextEdit editor widget
            main_window: The MainWindow instance for status/title updates
        """
        self.editor = editor
        self.main_window = main_window
        self.current_file = main_window.current_file if main_window else None
    
    def _show_status(self, message, duration=3000):
        """Show status message if main_window is available"""
        if self.main_window and hasattr(self.main_window, 'status_bar'):
            self.main_window.status_bar.showMessage(message, duration)
    
    def _update_title(self, filename=None):
        """Update window title"""
        if self.main_window:
            if filename:
                self.main_window.setWindowTitle(f'{constants.APP_NAME} - {os.path.basename(filename)}')
            else:
                self.main_window.setWindowTitle(constants.APP_NAME)
    
    def _update_auto_save_status(self):
        """Update auto-save status indicator"""
        if self.main_window and hasattr(self.main_window, 'update_auto_save_status'):
            self.main_window.update_auto_save_status()
    
    def handle_unsaved_changes(self, parent, action_description=''):
        """
        Handle unsaved changes before performing an action.
        
        Returns:
            bool: True if we should proceed, False if we should cancel
        """
        if not self.editor.document().isModified():
            return True
        
        action_text = f' before {action_description}' if action_description else ''
        reply = show_unsaved_changes_dialog(
            parent,
            f'You have unsaved changes. Do you want to save them{action_text}?'
        )
        
        if reply == QMessageBox.Save:
            # This will be handled by the caller
            return 'save'
        elif reply == QMessageBox.Cancel:
            return False
        else:  # Discard
            return True
    
    def auto_save_current_file(self):
        """
        Auto-save the current file if one is open and modified.
        
        Returns:
            bool: True if successful or nothing to save, False on error
        """
        if not self.current_file:
            return True
        
        if not self.editor.document().isModified():
            return True
        
        success, error = write_file_content(self.current_file, self.editor.toPlainText())
        if success:
            self.editor.document().setModified(False)
            return True
        else:
            return False
    
    def save_to_file(self, file_path):
        """
        Save content to the specified file.
        
        Args:
            file_path: Path to save the file to
            
        Returns:
            tuple: (success: bool, error_message: str or None)
        """
        success, error = write_file_content(file_path, self.editor.toPlainText())
        if success:
            self.editor.document().setModified(False)
            self.current_file = file_path
        return success, error
    
    def open_file(self, file_path):
        """
        Open a file in the editor.
        
        Args:
            file_path: Path to the file to open
            
        Returns:
            tuple: (success: bool, content: str or None, error: str or None)
        """
        content, error = read_file_content(file_path)
        if content is not None:
            self.editor.blockSignals(True)
            self.editor.setPlainText(content)
            self.editor.blockSignals(False)
            self.editor.document().setModified(False)
            self.current_file = file_path
            return True, content, None
        return False, None, error
    
    def create_new_file(self):
        """Clear the editor for a new file"""
        self.editor.clear()
        self.editor.document().setModified(False)
        self.current_file = None
    
    # ========================================================================
    # High-level file operations (used by menus)
    # ========================================================================
    
    def new_file(self, parent):
        """Create a new file with proper unsaved changes handling"""
        result = self.handle_unsaved_changes(parent, 'creating a new file')
        
        if result == 'save':
            if not self.save_file_as(parent):
                return
        elif not result:
            return
        
        if self.current_file and self.editor.document().isModified():
            if not self.auto_save_current_file():
                show_error_message(parent, 'Error', 'Could not auto-save file.')
                return
        
        self.create_new_file()
        self._update_title()
        self._show_status('New file created')
        self._update_auto_save_status()
    
    def open_file_dialog(self, parent):
        """Open a file with proper unsaved changes handling"""
        result = self.handle_unsaved_changes(parent, 'opening a new file')
        
        if result == 'save':
            if not self.save_file_as(parent):
                return
        elif not result:
            return
        
        if self.current_file and self.editor.document().isModified():
            if not self.auto_save_current_file():
                show_error_message(parent, 'Error', 'Could not auto-save file.')
                return
        
        file_path = open_file_dialog(parent)
        
        if file_path:
            success, content, error = self.open_file(file_path)
            if success:
                self._update_title(file_path)
                self._show_status(f'Opened: {file_path} (Auto-save enabled)')
                self._update_auto_save_status()
            else:
                show_error_message(parent, 'Error', f'Could not open file:\n{error}')
    
    def save_file(self, parent):
        """Save the current file"""
        if self.current_file:
            return self._save_to_file(parent, self.current_file)
        else:
            return self.save_file_as(parent)
    
    def save_file_as(self, parent):
        """Save the file with a new name"""
        file_path = save_file_dialog(parent)
        
        if file_path:
            success = self._save_to_file(parent, file_path)
            if success:
                self._update_title(file_path)
                self._show_status(f'Saved: {file_path}')
            return success
        return False
    
    def _save_to_file(self, parent, file_path):
        """Save content to file"""
        success, error = self.save_to_file(file_path)
        if success:
            self._update_auto_save_status()
            return True
        else:
            show_error_message(parent, 'Error', f'Could not save file:\n{error}')
            return False
