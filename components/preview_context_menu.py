"""
Preview Context Menu Component for MDEV
"""

from PyQt5.QtWidgets import QMenu, QAction
from PyQt5.QtWebEngineWidgets import QWebEnginePage

import styles


class PreviewContextMenu:
    """Context menu for the preview pane"""
    
    def __init__(self, parent=None):
        self.parent_window = parent
    
    def show(self, position):
        """Show the context menu at the given position"""
        if not self.parent_window:
            return
        
        context_menu = QMenu(self.parent_window)
        self.apply_style(context_menu)
        
        # Back action
        back_action = QAction('← Back', self.parent_window)
        back_action.setEnabled(self.parent_window.preview.page().action(QWebEnginePage.Back).isEnabled())
        back_action.triggered.connect(self.parent_window.preview.page().action(QWebEnginePage.Back).trigger)
        context_menu.addAction(back_action)
        
        # Forward action
        forward_action = QAction('→ Forward', self.parent_window)
        forward_action.setEnabled(self.parent_window.preview.page().action(QWebEnginePage.Forward).isEnabled())
        forward_action.triggered.connect(self.parent_window.preview.page().action(QWebEnginePage.Forward).trigger)
        context_menu.addAction(forward_action)
        
        # Reload action
        reload_action = QAction('↻ Reload', self.parent_window)
        reload_action.triggered.connect(self.parent_window.preview.reload)
        context_menu.addAction(reload_action)
        
        context_menu.addSeparator()
        
        context_menu.exec_(self.parent_window.preview.mapToGlobal(position))
    
    def apply_style(self, menu):
        """Apply theme-appropriate style to menu"""
        if self.parent_window and hasattr(self.parent_window, 'current_theme'):
            if self.parent_window.current_theme == 'dark':
                menu.setStyleSheet(styles.DARK_CONTEXT_MENU_STYLE)
            else:
                menu.setStyleSheet(styles.LIGHT_CONTEXT_MENU_STYLE)
        else:
            menu.setStyleSheet(styles.DARK_CONTEXT_MENU_STYLE)
