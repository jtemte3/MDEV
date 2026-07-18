"""
Dialogs for MDEV (About, License)
"""

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt

import constants


def show_about_dialog(parent=None):
    """Show the About MDEV dialog"""
    about_text = (
        f'<h2 style="color: #007acc;">{constants.APP_NAME}</h2>'
        '<p>A native desktop markdown editor and viewer built with Python and PyQt5.</p>'
        '<hr>'
        '<p><b>Features:</b></p>'
        '<ul>'
        '<li>✅ Live markdown preview</li>'
        '<li>✅ Syntax highlighting with dark theme</li>'
        '<li>✅ Dark/Light theme preview toggle</li>'
        '<li>✅ App theme toggle (Light/Dark) for all panels</li>'
        '<li>✅ Toggle editor/preview panes independently</li>'
        '<li>✅ Auto-save after every edit (2 second delay)</li>'
        '<li>✅ Full markdown support (headings, lists, tables, code blocks, etc.)</li>'
        '<li>✅ File explorer with project management</li>'
        '<li>✅ Toolbar with quick formatting buttons</li>'
        '<li>✅ Status bar with character/word/line counts</li>'
        '</ul>'
        '<hr>'
        '<p><b>Keyboard Shortcuts:</b></p>'
        '<ul>'
        '<li>Ctrl+B - Bold | Ctrl+I - Italic | Ctrl+K - Link</li>'
        '<li>Ctrl+Shift+K - Inline Code | Ctrl+D - Toggle Dark Preview</li>'
        '<li>Ctrl+Shift+T - Toggle App Theme | Ctrl+E - Toggle Editor Pane</li>'
        '<li>Ctrl+P - Toggle Preview Pane | Ctrl+S - Save | Ctrl+O - Open</li>'
        '<li>Ctrl+N - New File | Ctrl+Q - Exit</li>'
        '</ul>'
        '<hr>'
        f'<p><b>Version:</b> {constants.APP_VERSION}</p>'
        '<p><b>Created by:</b> Joe Temte</p>'
        '<p><b>License:</b> MIT License</p>'
        '<hr>'
        '<p style="font-size: small; color: #666;">'
        'Built with Python, PyQt5, PyQtWebEngine, Markdown, and Pygments</p>'
    )
    
    msg_box = QMessageBox(parent)
    msg_box.setWindowTitle('About MDEV')
    msg_box.setTextFormat(Qt.RichText)
    msg_box.setText(about_text)
    msg_box.setInformativeText('Click "View License" to see the full MIT License text.')
    msg_box.setStandardButtons(QMessageBox.Ok)
    
    # Add a "View License" button
    view_license_btn = msg_box.addButton('View License', QMessageBox.ActionRole)
    view_license_btn.clicked.connect(lambda: show_license_dialog(parent))
    
    msg_box.exec_()


def show_license_dialog(parent=None):
    """Show the MIT License dialog"""
    license_text = """MIT License

Copyright (c) 2026 Joe Temte

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""
    
    msg_box = QMessageBox(parent)
    msg_box.setWindowTitle('MIT License')
    msg_box.setTextFormat(Qt.RichText)
    msg_box.setText(
        '<h3>MIT License</h3>'
        '<p><b>Copyright (c) 2026 Joe Temte</b></p>'
        '<hr>'
    )
    msg_box.setInformativeText(license_text)
    msg_box.setStandardButtons(QMessageBox.Ok)
    msg_box.exec_()
