"""
Editor Context Menu Component for MDEV
"""

from PyQt5.QtWidgets import QMenu, QAction

import constants
import styles


class EditorContextMenu:
    """Context menu for the editor pane"""
    
    def __init__(self, parent=None):
        self.parent_window = parent
    
    def show(self, position):
        """Show the context menu at the given position"""
        if not self.parent_window:
            return
        
        context_menu = QMenu(self.parent_window)
        self.apply_style(context_menu)
        
        # Cut action
        cut_action = QAction('✂️ Cut', self.parent_window)
        cut_action.setShortcut(constants.SHORTCUTS['cut'])
        cut_action.triggered.connect(self.on_cut)
        cut_action.setEnabled(self.parent_window.editor.textCursor().hasSelection())
        context_menu.addAction(cut_action)
        
        # Copy action
        copy_action = QAction('📋 Copy', self.parent_window)
        copy_action.setShortcut(constants.SHORTCUTS['copy'])
        copy_action.triggered.connect(self.on_copy)
        copy_action.setEnabled(self.parent_window.editor.textCursor().hasSelection())
        context_menu.addAction(copy_action)
        
        # Paste action
        paste_action = QAction('📌 Paste', self.parent_window)
        paste_action.setShortcut(constants.SHORTCUTS['paste'])
        paste_action.triggered.connect(self.on_paste)
        context_menu.addAction(paste_action)
        
        context_menu.addSeparator()
        
        # Select All action
        select_all_action = QAction('☑️ Select All', self.parent_window)
        select_all_action.setShortcut('Ctrl+A')
        select_all_action.triggered.connect(self.on_select_all)
        context_menu.addAction(select_all_action)
        
        context_menu.exec_(self.parent_window.editor.mapToGlobal(position))
    
    def apply_style(self, menu):
        """Apply theme-appropriate style to menu"""
        if self.parent_window and hasattr(self.parent_window, 'current_theme'):
            if self.parent_window.current_theme == 'dark':
                menu.setStyleSheet(styles.DARK_CONTEXT_MENU_STYLE)
            else:
                menu.setStyleSheet(styles.LIGHT_CONTEXT_MENU_STYLE)
        else:
            menu.setStyleSheet(styles.DARK_CONTEXT_MENU_STYLE)
    
    def on_cut(self):
        """Handle cut action"""
        if self.parent_window and self.parent_window.editor.textCursor().hasSelection():
            self.parent_window.editor.textCursor().removeSelectedText()
    
    def on_copy(self):
        """Handle copy action"""
        if self.parent_window:
            self.parent_window.editor.copy()
    
    def on_paste(self):
        """Handle paste action"""
        if self.parent_window:
            self.parent_window.editor.paste()
    
    def on_select_all(self):
        """Handle select all action"""
        if self.parent_window:
            self.parent_window.editor.selectAll()
