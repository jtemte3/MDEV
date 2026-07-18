"""
MDEV (MarkDown Editor/Viewer) - Main Entry Point

This is the refactored entry point for the application.
The original monolithic mdev.py has been split into multiple
modules for better maintainability.
"""

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont

import constants
from main_window import MainWindow


def main():
    """Main entry point"""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Cross-platform style
    
    # Set application-wide font
    font = QFont(constants.UI_FONT_FAMILY, constants.UI_FONT_SIZE)
    app.setFont(font)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
