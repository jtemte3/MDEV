"""
Markdown Utilities
"""

import markdown
from pygments.formatters import HtmlFormatter

import constants


def convert_markdown_to_html(markdown_text, dark_mode=False):
    """Convert markdown text to HTML with syntax highlighting"""
    if not markdown_text.strip():
        return ""
    
    # 1. Generate Pygments CSS with theme-specific style
    pygments_style = 'monokai' if dark_mode else 'default'
    formatter = HtmlFormatter(style=pygments_style, cssclass='highlight', noclasses=False)
    pygments_css = formatter.get_style_defs('.highlight')
    css_injection = f"<style>{pygments_css}</style>"
    
    # 2. Convert markdown to HTML
    html_content = markdown.markdown(
        markdown_text,
        extensions=constants.MARKDOWN_EXTENSIONS_LIST,
        extension_configs=constants.MARKDOWN_EXTENSION_CONFIGS,
    )
    
    # 3. Inject CSS at the top of the content
    return css_injection + html_content


def get_markdown_extensions():
    """Return the list of markdown extensions"""
    return constants.MARKDOWN_EXTENSIONS_LIST


def get_markdown_extension_configs():
    """Return the markdown extension configurations"""
    return constants.MARKDOWN_EXTENSION_CONFIGS
