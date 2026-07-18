"""
Constants for MDEV (MarkDown Editor/Viewer)
"""

# Application metadata
APP_NAME = "MDEV (MarkDown Editor/Viewer)"
APP_VERSION = "1.4.0"

# Default window geometry
DEFAULT_WINDOW_WIDTH = 1200
DEFAULT_WINDOW_HEIGHT = 800
DEFAULT_WINDOW_X = 100
DEFAULT_WINDOW_Y = 100

# Default splitter sizes
DEFAULT_SPLITTER_SIZES = [600, 600]
DEFAULT_EXPLORER_SPLITTER_SIZES = [250, 1100]

# Activity bar
ACTIVITY_BAR_WIDTH = 48

# Project explorer
EXPLORER_MIN_WIDTH = 200
EXPLORER_MAX_WIDTH = 500

# Auto-save settings
AUTO_SAVE_DELAY_MS = 2000  # 2 seconds
PREVIEW_UPDATE_DELAY_MS = 300  # 300ms debounce
EXPLORER_SAVE_DELAY_MS = 500  # 500ms debounce after resize

# File extensions
MARKDOWN_EXTENSIONS = ('.md', '.markdown', '.txt')

# Settings file
SETTINGS_FILE_NAME = 'settings.json'

# Default settings
DEFAULT_SETTINGS = {
    'dark_mode': True,
    'app_theme': 'dark',  # 'dark' or 'light'
    'editor_visible': True,
    'preview_visible': True,
    'window_width': DEFAULT_WINDOW_WIDTH,
    'window_height': DEFAULT_WINDOW_HEIGHT,
    'window_x': DEFAULT_WINDOW_X,
    'window_y': DEFAULT_WINDOW_Y,
    'splitter_sizes': DEFAULT_SPLITTER_SIZES,
    'explorer_splitter_sizes': DEFAULT_EXPLORER_SPLITTER_SIZES,
    'last_directory': None
}

# Keyboard shortcuts
SHORTCUTS = {
    'new': 'Ctrl+N',
    'open': 'Ctrl+O',
    'save': 'Ctrl+S',
    'save_as': 'Ctrl+Shift+S',
    'open_directory': 'Ctrl+Shift+O',
    'new_file_in_dir': 'Ctrl+Shift+N',
    'new_folder_in_dir': 'Ctrl+Shift+F',
    'auto_save_now': 'Ctrl+Alt+S',
    'exit': 'Ctrl+Q',
    'undo': 'Ctrl+Z',
    'redo': 'Ctrl+Y',
    'cut': 'Ctrl+X',
    'copy': 'Ctrl+C',
    'paste': 'Ctrl+V',
    'toggle_preview': 'Ctrl+P',
    'toggle_editor': 'Ctrl+E',
    'toggle_dark_mode': 'Ctrl+D',
    'toggle_app_theme': 'Ctrl+Shift+T',
    'toggle_explorer': 'Ctrl+Shift+E',
    'bold': 'Ctrl+B',
    'italic': 'Ctrl+I',
    'link': 'Ctrl+K',
    'inline_code': 'Ctrl+Shift+K',
}

# Editor settings
EDITOR_FONT_FAMILY = 'Consolas'
EDITOR_FONT_SIZE = 11

# UI font
UI_FONT_FAMILY = 'Segoe UI'
UI_FONT_SIZE = 10

# Markdown extensions
MARKDOWN_EXTENSIONS_LIST = [
    'fenced_code',
    'codehilite',
    'tables',
    'toc',
    'nl2br',
    'sane_lists',
    'attr_list',
    'md_in_html',
]

MARKDOWN_EXTENSION_CONFIGS = {
    'codehilite': {
        'use_pygments': True,
        'noclasses': False,
        'css_class': 'highlight',
    }
}
