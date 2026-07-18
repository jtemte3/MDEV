"""
Activity Bar Component for MDEV
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt

import constants
import styles


class ActivityBar(QWidget):
    """VS Code-style vertical activity bar on the left edge"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the activity bar UI"""
        self.setFixedWidth(constants.ACTIVITY_BAR_WIDTH)
        self.setStyleSheet(styles.DARK_ACTIVITY_BAR_STYLE)
        
        activity_layout = QVBoxLayout(self)
        activity_layout.setContentsMargins(0, 0, 0, 0)
        activity_layout.setSpacing(0)
        
        # Project Explorer button at the top
        self.explorer_toggle_btn = QPushButton('📁')
        self.explorer_toggle_btn.setFixedSize(48, 48)
        self.explorer_toggle_btn.setToolTip('Project Explorer')
        self.explorer_toggle_btn.setCheckable(True)
        self.explorer_toggle_btn.setChecked(False)
        self.explorer_toggle_btn.setStyleSheet(styles.DARK_EXPLORER_TOGGLE_BTN_STYLE)
        self.explorer_toggle_btn.clicked.connect(self.on_explorer_toggle)
        activity_layout.addWidget(self.explorer_toggle_btn)
        activity_layout.addStretch()
        
        # Theme toggle button at the bottom
        self.theme_toggle_btn = QPushButton('🔆')
        self.theme_toggle_btn.setFixedSize(48, 48)
        self.theme_toggle_btn.setToolTip('Toggle App Theme (Light/Dark)')
        self.theme_toggle_btn.setCheckable(True)
        self.theme_toggle_btn.setChecked(True)  # True = dark theme
        self.theme_toggle_btn.setStyleSheet(styles.DARK_THEME_TOGGLE_BTN_STYLE)
        self.theme_toggle_btn.clicked.connect(self.on_theme_toggle)
        activity_layout.addWidget(self.theme_toggle_btn)
    
    def on_explorer_toggle(self):
        """Handle explorer toggle button click"""
        if self.parent_window:
            self.parent_window.toggle_project_explorer()
    
    def on_theme_toggle(self):
        """Handle theme toggle button click"""
        if self.parent_window:
            is_dark = self.theme_toggle_btn.isChecked()
            self.parent_window.toggle_app_theme(is_dark)
    
    def set_checked(self, checked):
        """Set the checked state of the explorer button"""
        self.explorer_toggle_btn.setChecked(checked)
    
    def is_checked(self):
        """Get the checked state of the explorer button"""
        return self.explorer_toggle_btn.isChecked()
    
    def set_theme(self, theme):
        """Apply theme to activity bar"""
        if theme == 'dark':
            self.setStyleSheet(styles.DARK_ACTIVITY_BAR_STYLE)
            self.explorer_toggle_btn.setStyleSheet(styles.DARK_EXPLORER_TOGGLE_BTN_STYLE)
            self.theme_toggle_btn.setStyleSheet(styles.DARK_THEME_TOGGLE_BTN_STYLE)
            self.theme_toggle_btn.setChecked(True)
        else:
            self.setStyleSheet(styles.LIGHT_ACTIVITY_BAR_STYLE)
            self.explorer_toggle_btn.setStyleSheet(styles.LIGHT_EXPLORER_TOGGLE_BTN_STYLE)
            self.theme_toggle_btn.setStyleSheet(styles.LIGHT_THEME_TOGGLE_BTN_STYLE)
            self.theme_toggle_btn.setChecked(False)
