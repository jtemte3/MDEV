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
        
        # Preserve the original widget position for showing the menu later
        widget_position = position
        
        # Check if the clicked position is on a misspelled word
        misspelled_word_info = self._get_misspelled_word_at_position(position)
        
        if misspelled_word_info:
            word, doc_position, length = misspelled_word_info
            # Get suggestions for the misspelled word
            suggestions = self.parent_window.editor.spell_engine.get_suggestions(word)
            
            # Add spelling suggestions section
            if suggestions:
                self._add_spelling_suggestions(context_menu, word, suggestions)
                context_menu.addSeparator()
        
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
        
        # Add "Add to Dictionary" action if on misspelled word
        if misspelled_word_info:
            context_menu.addSeparator()
            add_to_dict_action = QAction('📖 Add to Dictionary', self.parent_window)
            add_to_dict_action.triggered.connect(lambda: self.on_add_to_dictionary(misspelled_word_info[0]))
            context_menu.addAction(add_to_dict_action)
        
        context_menu.exec_(self.parent_window.editor.mapToGlobal(widget_position))
    
    def _get_misspelled_word_at_position(self, position):
        """Get misspelled word info at the clicked position, if any."""
        if not self.parent_window or not hasattr(self.parent_window.editor, 'spell_highlighter'):
            return None
        # Convert the position from widget coordinates to document position
        editor = self.parent_window.editor
        cursor = editor.cursorForPosition(position)
        doc_position = cursor.position()
        return editor.spell_highlighter.get_word_at_position(doc_position)
    
    def _get_misspelled_word_at_cursor(self):
        """Get misspelled word info at cursor position, if any."""
        if not self.parent_window or not hasattr(self.parent_window.editor, 'spell_highlighter'):
            return None
        return self.parent_window.editor.spell_highlighter.get_word_under_cursor()
    
    def _add_spelling_suggestions(self, menu, original_word, suggestions):
        """Add spelling suggestions to the context menu."""
        # Limit to 5 suggestions
        max_suggestions = min(len(suggestions), 5)
        
        for i in range(max_suggestions):
            suggestion = suggestions[i]
            action = QAction(f'✅ {suggestion}', self.parent_window)
            action.triggered.connect(lambda checked, word=suggestion, orig=original_word: 
                                    self.on_replace_word(orig, word))
            menu.addAction(action)
    
    def on_replace_word(self, original_word, replacement):
        """Replace the original word with the suggested replacement."""
        if not self.parent_window:
            return
        
        editor = self.parent_window.editor
        cursor = editor.textCursor()
        
        # Get the misspelled word position
        word_info = editor.spell_highlighter.get_word_under_cursor()
        if word_info:
            word, pos, length = word_info
            # Select the misspelled word
            cursor.setPosition(pos)
            cursor.setPosition(pos + length, cursor.KeepAnchor)
            # Replace with the suggestion
            cursor.insertText(replacement)
            editor.setTextCursor(cursor)
    
    def on_add_to_dictionary(self, word):
        """Add a word to the custom dictionary."""
        if self.parent_window:
            self.parent_window.editor.spell_engine.add_custom_word(word)
            # Re-trigger spell check to update highlights
            self.parent_window.editor.spell_highlighter._perform_spell_check()
            self.parent_window.status_bar.showMessage(f'Added "{word}" to dictionary', 3000)
    
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
