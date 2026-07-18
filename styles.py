"""
Styles and HTML templates for MDEV (MarkDown Editor/Viewer)
"""

# ============================================================================
# QSS Stylesheets for Dark Theme
# ============================================================================

DARK_EDITOR_STYLE = """
    QTextEdit {
        background-color: #1e1e1e;
        color: #d4d4d4;
        border: none;
        selection-background-color: #264f78;
    }
"""

DARK_ACTIVITY_BAR_STYLE = """
    QWidget {
        background-color: #333333;
        border-right: 1px solid #444444;
    }
"""

DARK_EXPLORER_TOGGLE_BTN_STYLE = """
    QPushButton {
        background: transparent;
        border: none;
        color: #858585;
        font-size: 20px;
    }
    QPushButton:hover {
        color: #ffffff;
        background-color: #444444;
    }
    QPushButton:checked {
        color: #ffffff;
        border-left: 2px solid #007acc;
        background-color: #3c3c3c;
    }
"""

DARK_THEME_TOGGLE_BTN_STYLE = """
    QPushButton {
        background: transparent;
        border: none;
        color: #858585;
        font-size: 20px;
    }
    QPushButton:hover {
        color: #ffffff;
        background-color: #444444;
    }
    QPushButton:checked {
        color: #ffffff;
        border-left: 2px solid #007acc;
        background-color: #3c3c3c;
    }
"""

DARK_SPLITTER_STYLE = """
    QSplitter::handle {
        background-color: #444444;
    }
    QSplitter::handle:hover {
        background-color: #007acc;
    }
"""

DARK_EXPLORER_PANEL_STYLE = """
    QWidget {
        background-color: #252526;
        border-right: 1px solid #444444;
    }
"""

DARK_EXPLORER_TOOLBAR_STYLE = """
    QToolBar {
        spacing: 4px;
        padding: 8px 4px;
        background-color: #252526;
        border-bottom: 1px solid #444444;
    }
    QToolBar QToolButton {
        background: transparent;
        border: none;
        color: #cccccc;
        padding: 4px 8px;
    }
    QToolBar QToolButton:hover {
        background-color: #444444;
    }
"""

DARK_FILE_TREE_STYLE = """
    QTreeView {
        background-color: #1e1e1e;
        color: #cccccc;
        border: none;
        selection-background-color: #094771;
        selection-color: #ffffff;
    }
    QTreeView::item {
        padding: 4px;
    }
    QTreeView::item:hover {
        background-color: #2a2d2e;
    }
"""

DARK_TOOLBAR_STYLE = """
    QToolBar {
        background-color: #2d2d30;
        border-bottom: 1px solid #444444;
        spacing: 4px;
        padding: 4px;
    }
    QToolBar QToolButton {
        background: transparent;
        border: none;
        color: #cccccc;
        padding: 4px 8px;
    }
    QToolBar QToolButton:hover {
        background-color: #444444;
    }
    QToolBar QToolButton:checked {
        background-color: #094771;
    }
"""

DARK_APP_TOOLBAR_STYLE = """
    QToolBar {
        background-color: #2d2d30;
        border-bottom: 1px solid #444444;
        spacing: 6px;
        padding: 4px 8px;
    }
    QToolBar QToolButton {
        background: transparent;
        border: none;
        color: #cccccc;
        padding: 4px 10px;
        font-size: 12px;
    }
    QToolBar QToolButton:hover {
        background-color: #444444;
    }
    QToolBar QToolButton:checked {
        background-color: #094771;
    }
"""

DARK_APP_TOOLBAR_COLLAPSE_BTN = """
    QPushButton {
        background: transparent;
        border: none;
        color: #cccccc;
        font-size: 10px;
        padding: 2px;
    }
    QPushButton:hover {
        background-color: #444444;
        color: #ffffff;
    }
"""

DARK_PREVIEW_TOOLBAR_STYLE = """
    QToolBar {
        background-color: #2d2d30;
        border-bottom: 1px solid #444444;
        spacing: 4px;
        padding: 4px;
    }
    QToolBar QToolButton {
        background: transparent;
        border: none;
        color: #cccccc;
        padding: 4px 8px;
    }
    QToolBar QToolButton:hover {
        background-color: #444444;
    }
    QToolBar QToolButton:checked {
        background-color: #094771;
    }
"""

DARK_MENU_BAR_STYLE = """
    QMenuBar {
        background-color: #323233;
        color: #cccccc;
        border-bottom: 1px solid #444444;
    }
    QMenuBar::item {
        padding: 4px 8px;
        background: transparent;
    }
    QMenuBar::item:selected {
        background-color: #444444;
    }
    QMenu {
        background-color: #252526;
        color: #cccccc;
        border: 1px solid #444444;
    }
    QMenu::item {
        padding: 6px 24px 6px 12px;
    }
    QMenu::item:selected {
        background-color: #094771;
    }
    QMenu::separator {
        height: 1px;
        background-color: #444444;
        margin: 4px 12px;
    }
"""

DARK_STATUS_BAR_STYLE = """
    QStatusBar {
        background-color: #007acc;
        color: #ffffff;
        border-top: 1px solid #444444;
    }
"""

DARK_MAIN_WINDOW_STYLE = """
    QMainWindow {
        background-color: #1e1e1e;
    }
"""

DARK_CONTEXT_MENU_STYLE = """
    QMenu {
        background-color: #252526;
        color: #cccccc;
        border: 1px solid #444444;
    }
    QMenu::item {
        padding: 6px 24px 6px 12px;
    }
    QMenu::item:selected {
        background-color: #094771;
    }
    QMenu::separator {
        height: 1px;
        background-color: #444444;
        margin: 4px 12px;
    }
"""

# ============================================================================
# QSS Stylesheets for Light Theme
# ============================================================================

LIGHT_EDITOR_STYLE = """
    QTextEdit {
        background-color: #ffffff;
        color: #333333;
        border: none;
        selection-background-color: #add6ff;
    }
"""

LIGHT_ACTIVITY_BAR_STYLE = """
    QWidget {
        background-color: #f8f8f8;
        border-right: 1px solid #e0e0e0;
    }
"""

LIGHT_EXPLORER_TOGGLE_BTN_STYLE = """
    QPushButton {
        background: transparent;
        border: none;
        color: #666666;
        font-size: 20px;
    }
    QPushButton:hover {
        color: #333333;
        background-color: #e8e8e8;
    }
    QPushButton:checked {
        color: #333333;
        border-left: 2px solid #007acc;
        background-color: #e0e0e0;
    }
"""

LIGHT_THEME_TOGGLE_BTN_STYLE = """
    QPushButton {
        background: transparent;
        border: none;
        color: #666666;
        font-size: 20px;
    }
    QPushButton:hover {
        color: #333333;
        background-color: #e8e8e8;
    }
    QPushButton:checked {
        color: #333333;
        border-left: 2px solid #007acc;
        background-color: #e0e0e0;
    }
"""

LIGHT_SPLITTER_STYLE = """
    QSplitter::handle {
        background-color: #cccccc;
    }
    QSplitter::handle:hover {
        background-color: #007acc;
    }
"""

LIGHT_EXPLORER_PANEL_STYLE = """
    QWidget {
        background-color: #f3f3f3;
        border-right: 1px solid #e0e0e0;
    }
"""

LIGHT_EXPLORER_TOOLBAR_STYLE = """
    QToolBar {
        spacing: 4px;
        padding: 8px 4px;
        background-color: #f3f3f3;
        border-bottom: 1px solid #e0e0e0;
    }
    QToolBar QToolButton {
        background: transparent;
        border: none;
        color: #333333;
        padding: 4px 8px;
    }
    QToolBar QToolButton:hover {
        background-color: #e0e0e0;
    }
"""

LIGHT_FILE_TREE_STYLE = """
    QTreeView {
        background-color: #ffffff;
        color: #333333;
        border: none;
        selection-background-color: #0078d4;
        selection-color: #ffffff;
    }
    QTreeView::item {
        padding: 4px;
    }
    QTreeView::item:hover {
        background-color: #e8e8e8;
    }
"""

LIGHT_TOOLBAR_STYLE = """
    QToolBar {
        background-color: #f8f8f8;
        border-bottom: 1px solid #e0e0e0;
        spacing: 4px;
        padding: 4px;
    }
    QToolBar QToolButton {
        background: transparent;
        border: none;
        color: #333333;
        padding: 4px 8px;
    }
    QToolBar QToolButton:hover {
        background-color: #e0e0e0;
    }
    QToolBar QToolButton:checked {
        background-color: #0078d4;
    }
"""

LIGHT_APP_TOOLBAR_STYLE = """
    QToolBar {
        background-color: #f8f8f8;
        border-bottom: 1px solid #e0e0e0;
        spacing: 6px;
        padding: 4px 8px;
    }
    QToolBar QToolButton {
        background: transparent;
        border: none;
        color: #333333;
        padding: 4px 10px;
        font-size: 12px;
    }
    QToolBar QToolButton:hover {
        background-color: #e0e0e0;
    }
    QToolBar QToolButton:checked {
        background-color: #0078d4;
    }
"""

LIGHT_APP_TOOLBAR_COLLAPSE_BTN = """
    QPushButton {
        background: transparent;
        border: none;
        color: #333333;
        font-size: 10px;
        padding: 2px;
    }
    QPushButton:hover {
        background-color: #e0e0e0;
        color: #000000;
    }
"""

LIGHT_PREVIEW_TOOLBAR_STYLE = """
    QToolBar {
        background-color: #f8f8f8;
        border-bottom: 1px solid #e0e0e0;
        spacing: 4px;
        padding: 4px;
    }
    QToolBar QToolButton {
        background: transparent;
        border: none;
        color: #333333;
        padding: 4px 8px;
    }
    QToolBar QToolButton:hover {
        background-color: #e0e0e0;
    }
    QToolBar QToolButton:checked {
        background-color: #0078d4;
    }
"""

LIGHT_MENU_BAR_STYLE = """
    QMenuBar {
        background-color: #f8f8f8;
        color: #333333;
        border-bottom: 1px solid #e0e0e0;
    }
    QMenuBar::item {
        padding: 4px 8px;
        background: transparent;
    }
    QMenuBar::item:selected {
        background-color: #e0e0e0;
    }
    QMenu {
        background-color: #ffffff;
        color: #333333;
        border: 1px solid #cccccc;
    }
    QMenu::item {
        padding: 6px 24px 6px 12px;
    }
    QMenu::item:selected {
        background-color: #e8e8e8;
    }
    QMenu::separator {
        height: 1px;
        background-color: #e0e0e0;
        margin: 4px 12px;
    }
"""

LIGHT_STATUS_BAR_STYLE = """
    QStatusBar {
        background-color: #007acc;
        color: #ffffff;
        border-top: 1px solid #e0e0e0;
    }
"""

LIGHT_MAIN_WINDOW_STYLE = """
    QMainWindow {
        background-color: #ffffff;
    }
"""

LIGHT_CONTEXT_MENU_STYLE = """
    QMenu {
        background-color: #ffffff;
        color: #333333;
        border: 1px solid #cccccc;
    }
    QMenu::item {
        padding: 6px 24px 6px 12px;
    }
    QMenu::item:selected {
        background-color: #e8e8e8;
    }
    QMenu::separator {
        height: 1px;
        background-color: #e0e0e0;
        margin: 4px 12px;
    }
"""

# ============================================================================
# HTML Templates for Markdown Preview
# ============================================================================

LIGHT_PREVIEW_CSS = """
    body {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
        line-height: 1.6;
        color: #333;
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
        background-color: #ffffff;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #2c3e50;
        margin-top: 24px;
        margin-bottom: 16px;
        font-weight: 600;
    }
    h1 { font-size: 2em; border-bottom: 1px solid #eaecef; padding-bottom: 0.3em; }
    h2 { font-size: 1.5em; border-bottom: 1px solid #eaecef; padding-bottom: 0.3em; }
    h3 { font-size: 1.25em; }
    p { margin-bottom: 16px; }
    code {
        background-color: #f6f8fa;
        padding: 0.2em 0.4em;
        border-radius: 3px;
        font-size: 85%;
        color: #e83e8c;
    }
    pre {
        background-color: #f6f8fa;
        padding: 16px;
        border-radius: 6px;
        overflow: auto;
        line-height: 1.45;
    }
    pre code {
        background-color: transparent;
        padding: 0;
    }
    blockquote {
        border-left: 4px solid #dfe2e5;
        padding-left: 16px;
        color: #6a737d;
        margin: 16px 0;
    }
    ul, ol {
        padding-left: 2em;
        margin-bottom: 16px;
    }
    li { margin-bottom: 4px; }
    table {
        border-collapse: collapse;
        width: 100%;
        margin-bottom: 16px;
    }
    th, td {
        border: 1px solid #dfe2e5;
        padding: 6px 13px;
    }
    th { background-color: #f6f8fa; }
    a {
        color: #0366d6;
        text-decoration: none;
    }
    a:hover { text-decoration: underline; }
    img { max-width: 100%; }
    hr {
        height: 2px;
        padding: 0;
        margin: 24px 0;
        background-color: #eaecef;
        border: 0;
    }
    .emoji { font-size: 1.2em; }
    input[type="checkbox"] {
        margin-right: 8px;
    }
"""

DARK_PREVIEW_CSS = """
    body {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
        line-height: 1.6;
        color: #d4d4d4;
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
        background-color: #1e1e1e;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff;
        margin-top: 24px;
        margin-bottom: 16px;
        font-weight: 600;
    }
    h1 { font-size: 2em; border-bottom: 1px solid #404040; padding-bottom: 0.3em; }
    h2 { font-size: 1.5em; border-bottom: 1px solid #404040; padding-bottom: 0.3em; }
    h3 { font-size: 1.25em; }
    p { margin-bottom: 16px; }
    code {
        background-color: #2d2d2d;
        padding: 0.2em 0.4em;
        border-radius: 3px;
        font-size: 85%;
        color: #9cdcfe;
    }
    pre {
        background-color: #2d2d2d;
        padding: 16px;
        border-radius: 6px;
        overflow: auto;
        line-height: 1.45;
    }
    pre code {
        background-color: transparent;
        padding: 0;
    }
    blockquote {
        border-left: 4px solid #404040;
        padding-left: 16px;
        color: #858585;
        margin: 16px 0;
    }
    ul, ol {
        padding-left: 2em;
        margin-bottom: 16px;
    }
    li { margin-bottom: 4px; }
    table {
        border-collapse: collapse;
        width: 100%;
        margin-bottom: 16px;
    }
    th, td {
        border: 1px solid #404040;
        padding: 6px 13px;
    }
    th { background-color: #2d2d2d; }
    a {
        color: #3794ff;
        text-decoration: none;
    }
    a:hover { text-decoration: underline; }
    img { max-width: 100%; }
    hr {
        height: 2px;
        padding: 0;
        margin: 24px 0;
        background-color: #404040;
        border: 0;
    }
    .emoji { font-size: 1.2em; }
    input[type="checkbox"] {
        margin-right: 8px;
    }
"""

def get_light_preview_html(content="", placeholder=False):
    """Return light themed HTML for markdown preview"""
    if placeholder:
        body_content = '<div style="text-align: center; color: #999; margin-top: 50px;"><p>Markdown preview will appear here</p></div>'
    else:
        body_content = content
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            {LIGHT_PREVIEW_CSS}
        </style>
    </head>
    <body>
        {body_content}
    </body>
    </html>
    """

def get_dark_preview_html(content="", placeholder=False):
    """Return dark themed HTML for markdown preview"""
    if placeholder:
        body_content = '<div style="text-align: center; color: #858585; margin-top: 50px;"><p>Markdown preview will appear here</p></div>'
    else:
        body_content = content
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            {DARK_PREVIEW_CSS}
        </style>
    </head>
    <body>
        {body_content}
    </body>
    </html>
    """

# ============================================================================
# Theme style dictionaries for easy access
# ============================================================================

DARK_THEMES = {
    'editor': DARK_EDITOR_STYLE,
    'activity_bar': DARK_ACTIVITY_BAR_STYLE,
    'explorer_toggle_btn': DARK_EXPLORER_TOGGLE_BTN_STYLE,
    'splitter': DARK_SPLITTER_STYLE,
    'explorer_panel': DARK_EXPLORER_PANEL_STYLE,
    'explorer_toolbar': DARK_EXPLORER_TOOLBAR_STYLE,
    'file_tree': DARK_FILE_TREE_STYLE,
    'toolbar': DARK_TOOLBAR_STYLE,
    'menu_bar': DARK_MENU_BAR_STYLE,
    'status_bar': DARK_STATUS_BAR_STYLE,
    'main_window': DARK_MAIN_WINDOW_STYLE,
    'context_menu': DARK_CONTEXT_MENU_STYLE,
}

LIGHT_THEMES = {
    'editor': LIGHT_EDITOR_STYLE,
    'activity_bar': LIGHT_ACTIVITY_BAR_STYLE,
    'explorer_toggle_btn': LIGHT_EXPLORER_TOGGLE_BTN_STYLE,
    'splitter': LIGHT_SPLITTER_STYLE,
    'explorer_panel': LIGHT_EXPLORER_PANEL_STYLE,
    'explorer_toolbar': LIGHT_EXPLORER_TOOLBAR_STYLE,
    'file_tree': LIGHT_FILE_TREE_STYLE,
    'toolbar': LIGHT_TOOLBAR_STYLE,
    'menu_bar': LIGHT_MENU_BAR_STYLE,
    'status_bar': LIGHT_STATUS_BAR_STYLE,
    'main_window': LIGHT_MAIN_WINDOW_STYLE,
    'context_menu': LIGHT_CONTEXT_MENU_STYLE,
}
