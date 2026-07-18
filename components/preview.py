"""
Markdown Preview Component
"""

from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtCore import QTimer
import markdown
from pygments.formatters import HtmlFormatter

import constants
import styles


class MarkdownPreview(QWebEngineView):
    """Web view for rendering markdown preview"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.dark_mode = False
        self._scroll_position = 0
        self._restore_timer = QTimer(self)
        self._restore_timer.setSingleShot(True)
        self._restore_timer.timeout.connect(self._restore_scroll)
        self.loadFinished.connect(self._on_load_finished)
        
        # Inject scroll tracking script
        self.page().runJavaScript(self._get_scroll_tracking_js())
        
        # Set initial HTML
        self.setHtml(self.get_default_html())
        
    def _get_scroll_tracking_js(self):
        """Return JavaScript for tracking scroll position"""
        return '''
        (function() {
            window.addEventListener('scroll', function() {
                window._mdevScrollPosition = window.scrollY || document.documentElement.scrollTop || document.body.scrollTop || 0;
            });
            window._mdevScrollPosition = 0;
        })()
        '''
    
    def toggle_dark_mode(self):
        """Toggle between light and dark theme"""
        self.dark_mode = not self.dark_mode
        # Update preview with current content
        markdown_text = self.parent().editor.toPlainText()
        self.update_preview(markdown_text)
        
    def get_default_html(self):
        """Return default HTML when no markdown is present"""
        if self.dark_mode:
            return styles.get_dark_preview_html(placeholder=True)
        return styles.get_light_preview_html(placeholder=True)
    
    def update_preview(self, markdown_text):
        """Update the preview with rendered markdown"""
        # Read the current scroll position from JavaScript before updating
        self.page().runJavaScript(
            'window._mdevScrollPosition || 0',
            self._update_scroll_position
        )
        
        if not markdown_text.strip():
            self.setHtml(self.get_default_html())
            return
        
        # 1. Generate Pygments CSS with theme-specific style
        pygments_style = 'monokai' if self.dark_mode else 'default'
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
        full_content = css_injection + html_content
        
        # 4. Choose theme based on dark_mode setting
        if self.dark_mode:
            full_html = styles.get_dark_preview_html(full_content)
        else:
            full_html = styles.get_light_preview_html(full_content)
        
        self.setHtml(full_html)

    def _on_load_finished(self, success):
        """Called when the page finishes loading"""
        if success:
            # Re-inject scroll tracking script
            self.page().runJavaScript(self._get_scroll_tracking_js())
            # Delay restoration slightly to ensure page is fully rendered
            self._restore_timer.start(50)
    
    def _restore_scroll(self):
        """Restore the scroll position after a brief delay"""
        if hasattr(self, '_scroll_position') and self._scroll_position > 0:
            self.page().runJavaScript(
                f'window.scrollTo(0, {self._scroll_position});'
            )
    
    def _update_scroll_position(self, result):
        """Update stored scroll position"""
        if result is not None:
            self._scroll_position = result
