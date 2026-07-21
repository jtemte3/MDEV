"""
Markdown Preview Component
"""

from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtCore import pyqtSignal, QTimer
import markdown
from pygments.formatters import HtmlFormatter

import constants
import styles


class MarkdownPreview(QWebEngineView):
    """Web view for rendering markdown preview with synchronous scrolling support"""
    
    # Signal emitted when preview scroll position changes
    scroll_position_changed = pyqtSignal(int)
    
    # Scroll change tolerance (pixels) - ignore small changes to prevent drift
    SCROLL_TOLERANCE = 5
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.dark_mode = False
        self._is_syncing_scroll = False  # Flag to prevent infinite scroll sync loops
        self._content_height = 0  # Total scrollable height of preview content
        self._scroll_ratio = 0.0  # Current scroll ratio (0.0 to 1.0)
        self._last_scroll_y = 0  # Track last scroll position for change detection
        self._pending_sync_scroll_y = None  # Track expected scroll position after sync
        self._scroll_ratio_to_restore = None  # Scroll ratio to restore after content update
        self._is_updating_content = False  # Flag to prevent scroll sync during content updates
        self.loadFinished.connect(self._on_load_finished)
        
        # Set up scroll polling timer
        self._scroll_poll_timer = QTimer(self)
        self._scroll_poll_timer.setInterval(50)  # Poll every 50ms (~20fps)
        self._scroll_poll_timer.timeout.connect(self._poll_scroll_position)
        self._scroll_poll_timer.start()
        
        # Set initial HTML
        self.setHtml(self.get_default_html())
    
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
        # Save current scroll ratio before updating content to restore it after
        self._scroll_ratio_to_restore = self._scroll_ratio
        
        # Set flag to prevent scroll sync during content update
        self._is_updating_content = True
        
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
            # Get content height after load
            self._get_content_height()
            
            # Restore scroll position if we had one saved before content update
            if self._scroll_ratio_to_restore is not None:
                # Use a small delay to ensure content height is available
                QTimer.singleShot(50, self._restore_scroll_position)
    
    def _restore_scroll_position(self):
        """Restore the scroll position after content update."""
        if self._scroll_ratio_to_restore is not None:
            # Temporarily disable sync to prevent triggering editor scroll sync
            self._is_syncing_scroll = True
            self.set_scroll_ratio(self._scroll_ratio_to_restore)
            self._scroll_ratio_to_restore = None
            # Clear the content update flag
            self._is_updating_content = False
            # Reset flag after a brief delay
            QTimer.singleShot(100, self._reset_syncing_flag)
        else:
            # Clear the content update flag even if no scroll ratio to restore
            self._is_updating_content = False
    
    def _poll_scroll_position(self):
        """Poll the current scroll position and emit signal if changed."""
        # Don't poll if preview is not visible
        if not self.isVisible():
            return
        
        # Don't poll during content updates to prevent scroll sync issues
        if self._is_updating_content:
            return
        
        self.page().runJavaScript(
            '''(function() {
                try {
                    if (typeof window.scrollY !== 'undefined' && window.scrollY !== null) {
                        return window.scrollY;
                    }
                    if (document.documentElement && document.documentElement.scrollTop !== null) {
                        return document.documentElement.scrollTop;
                    }
                    if (document.body && document.body.scrollTop !== null) {
                        return document.body.scrollTop;
                    }
                    return 0;
                } catch(e) {
                    return 0;
                }
            })()''',
            self._handle_scroll_poll_result
        )
    
    def _handle_scroll_poll_result(self, scroll_y):
        """Handle the result of scroll position polling."""
        if scroll_y is None or not isinstance(scroll_y, (int, float)):
            return
        
        # If we're waiting for a sync to complete, check if we're close enough
        if self._pending_sync_scroll_y is not None:
            if abs(scroll_y - self._pending_sync_scroll_y) <= self.SCROLL_TOLERANCE:
                # We've reached the target scroll position, clear pending sync
                self._pending_sync_scroll_y = None
                self._last_scroll_y = scroll_y
                self._is_syncing_scroll = False
            return
        
        # Check if scroll position changed significantly (with tolerance)
        if abs(scroll_y - self._last_scroll_y) < self.SCROLL_TOLERANCE:
            return  # Ignore small changes to prevent drift
        
        self._last_scroll_y = scroll_y
        
        # Only emit signal if not currently syncing from editor
        if not self._is_syncing_scroll:
            # Calculate scroll ratio
            max_scroll = max(0, self._content_height - self.height())
            if max_scroll > 0:
                self._scroll_ratio = scroll_y / max_scroll
            else:
                self._scroll_ratio = 0.0
            
            # Emit signal with ratio (scaled to 0-1000 for precision)
            self.scroll_position_changed.emit(int(self._scroll_ratio * 1000))
    
    def _get_content_height(self):
        """Get the total scrollable height of the preview content"""
        self.page().runJavaScript(
            '''(function() {
                try {
                    if (document.documentElement && document.documentElement.scrollHeight) {
                        return document.documentElement.scrollHeight;
                    }
                    if (document.body && document.body.scrollHeight) {
                        return document.body.scrollHeight;
                    }
                    return 0;
                } catch(e) {
                    return 0;
                }
            })()''',
            self._update_content_height
        )
    
    def _update_content_height(self, result):
        """Update stored content height"""
        if result is not None and isinstance(result, (int, float)) and result > 0:
            self._content_height = result
    
    def sync_scroll_from_editor(self, editor_scroll_value, editor_max_scroll):
        """
        Synchronize preview scroll position based on editor scroll position.
        
        Args:
            editor_scroll_value: Current scroll value of the editor
            editor_max_scroll: Maximum scroll value of the editor
        """
        if self._is_syncing_scroll:
            return
        
        # Don't sync if content height is not yet loaded
        if self._content_height <= 0:
            return
        
        self._is_syncing_scroll = True
        
        # Calculate scroll ratio from editor (0.0 to 1.0)
        if editor_max_scroll > 0:
            self._scroll_ratio = editor_scroll_value / editor_max_scroll
        else:
            self._scroll_ratio = 0.0
        
        # Apply the same ratio to preview
        preview_scroll = int(self._scroll_ratio * max(0, self._content_height - self.height()))
        self.page().runJavaScript(f'window.scrollTo(0, {preview_scroll});')
        
        # Set pending sync target so poll timer knows to wait for this scroll
        self._pending_sync_scroll_y = preview_scroll
        
        # Reset the flag after a delay as a fallback (in case poll misses the target)
        QTimer.singleShot(100, self._reset_syncing_flag)
    
    def _reset_syncing_flag(self):
        """Reset the syncing flag after scroll operation completes."""
        self._is_syncing_scroll = False
        self._pending_sync_scroll_y = None
    
    def on_preview_scrolled(self, scroll_y):
        """
        Called when preview is scrolled. Emits signal to sync editor.
        
        Args:
            scroll_y: Current scroll Y position of the preview
        """
        if self._is_syncing_scroll:
            return
        
        self._is_syncing_scroll = True
        
        # Calculate scroll ratio from preview
        max_scroll = max(0, self._content_height - self.height())
        if max_scroll > 0:
            self._scroll_ratio = scroll_y / max_scroll
        else:
            self._scroll_ratio = 0.0
        
        # Emit signal to sync editor
        self.scroll_position_changed.emit(int(self._scroll_ratio * 1000))
        
        self._is_syncing_scroll = False
    
    def set_scroll_ratio(self, ratio):
        """
        Set the preview scroll position based on a ratio (0.0 to 1.0).
        
        Args:
            ratio: Scroll ratio between 0.0 (top) and 1.0 (bottom)
        """
        self._is_syncing_scroll = True
        self._scroll_ratio = max(0.0, min(1.0, ratio))
        preview_scroll = int(self._scroll_ratio * max(0, self._content_height - self.height()))
        self.page().runJavaScript(f'window.scrollTo(0, {preview_scroll});')
        self._is_syncing_scroll = False
