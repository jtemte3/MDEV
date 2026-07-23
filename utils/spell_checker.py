"""
Spell Checker Utility for MDEV

Provides real-time spell checking with suggestions for misspelled words.
"""

from spellchecker import SpellChecker
from PyQt5.QtGui import QTextCursor, QTextCharFormat, QColor
from PyQt5.QtCore import QTimer
import re


class SpellCheckEngine:
    """Spell checking engine that checks words and provides suggestions."""
    
    def __init__(self, language='en'):
        """Initialize the spell checker with the specified language."""
        self.spell = SpellChecker(language=language)
        self._custom_words = set()
        self._markdown_tokens = set(['#', '##', '###', '####', '#####', '######', 
                                     '*', '**', '***', '-', '_', '`', '```',
                                     '---', '---', '***', '___',
                                     '[]', '()', '()', '[]()',
                                     '>', '>>', '>>>'])
        
    def add_custom_word(self, word):
        """Add a word to the custom dictionary."""
        word = word.lower().strip()
        if word:
            self.spell.word_frequency.add(word)
            self._custom_words.add(word)
            
    def remove_custom_word(self, word):
        """Remove a word from the custom dictionary."""
        word = word.lower().strip()
        if word in self._custom_words:
            self.spell.word_frequency.subtract(word)
            self._custom_words.discard(word)
            
    def is_misspelled(self, word):
        """Check if a word is misspelled."""
        if not word:
            return False
        # Skip markdown tokens and URLs
        if word in self._markdown_tokens:
            return False
        if self._is_url_or_code(word):
            return False
        unknown = self.spell.unknown([word])
        return word in unknown
    
    def _is_url_or_code(self, word):
        """Check if the word is a URL, email, or code-like string."""
        # Skip URLs
        if '://' in word or word.startswith('http'):
            return True
        # Skip emails
        if '@' in word:
            return True
        # Skip strings that look like code (contain multiple special chars)
        if any(c in word and word.count(c) > 1 for c in ['/', '\\', '.', '_', '-']):
            return True
        return False
    
    def get_suggestions(self, word, max_suggestions=5):
        """Get spelling suggestions for a misspelled word."""
        if not word:
            return []
        suggestions = self.spell.correction(word)
        if suggestions:
            return [suggestions] + list(self.spell.candidates(word))[:max_suggestions]
        return []
    
    def check_word(self, word):
        """Check a word and return (is_correct, suggestions) tuple."""
        if not word:
            return True, []
        if self._is_url_or_code(word):
            return True, []
        if not self.is_misspelled(word):
            return True, []
        return False, self.get_suggestions(word)


class SpellCheckHighlighter:
    """Handles highlighting of misspelled words in the editor."""
    
    def __init__(self, editor, spell_engine):
        """
        Initialize the highlighter.
        
        Args:
            editor: The MarkdownEditorTextEdit instance
            spell_engine: SpellCheckEngine instance
        """
        self.editor = editor
        self.spell_engine = spell_engine
        self._misspelled_words = {}  # position -> word mapping
        
        # Full document check timer (slower, runs after inactivity)
        self._full_check_timer = QTimer(editor)
        self._full_check_timer.setSingleShot(True)
        self._full_check_timer.timeout.connect(self._perform_full_spell_check)
        self._full_check_delay = 1500  # 2 seconds of inactivity
        
        self._is_checking = False  # Flag to prevent recursive spell checks
        
        # Connect to document changes
        self.editor.document().contentsChanged.connect(self._on_content_changed)
        
    def _create_misspelled_format(self):
        """Create the text format for misspelled word highlighting."""
        format = QTextCharFormat()
        format.setUnderlineStyle(QTextCharFormat.SpellCheckUnderline)
        format.setUnderlineColor(QColor(255, 0, 0))  # Red wavy underline
        return format
        
    def _on_content_changed(self):
        """Called when document content changes - schedule a spell check."""
        if self._is_checking:
            return
        # Restart both timers
        self._full_check_timer.stop()
        self._full_check_timer.start(self._full_check_delay)
            
    def _perform_full_spell_check(self):
        """Perform comprehensive spell check on the entire document."""
        if self._is_checking:
            return
        self._is_checking = True

        document = self.editor.document()
        # Block signals to prevent UI lag and recursive checks
        document.blockSignals(True)
        document.setUndoRedoEnabled(False)

        # Save the current modified state BEFORE spell check
        was_modified = document.isModified()
        try:
            # Clear all underlines
            self._remove_all_spell_underlines(document)
            
            block = document.begin()
            while block.isValid():
                text = block.text()
                words = self._extract_words(text)
                
                for word, start_pos in words:
                    if self.spell_engine.is_misspelled(word):
                        position = block.position() + start_pos
                        length = len(word)
                        self._misspelled_words[position] = word
                        self._apply_highlight(document, position, length)
                
                block = block.next()
        except Exception:
            pass
        finally:
            document.blockSignals(False)
            document.setUndoRedoEnabled(True)
            # Restore the original modified state (spell check shouldn't mark as modified)
            document.setModified(was_modified)
            self._is_checking = False
    
    def _apply_highlight(self, document, position, length):
        """Apply spell check underline to a specific range."""
        cursor = QTextCursor(document)
        cursor.setPosition(position)
        cursor.setPosition(position + length, QTextCursor.KeepAnchor)
        existing_format = cursor.charFormat()
        existing_format.setUnderlineStyle(QTextCharFormat.SpellCheckUnderline)
        existing_format.setUnderlineColor(QColor(255, 0, 0))
        cursor.setCharFormat(existing_format)
        
    def _clear_block_underlines(self, block):
        """Clear spell check underlines in a specific block."""
        document = self.editor.document()
        cursor = QTextCursor(block)
        cursor.select(QTextCursor.BlockUnderCursor)
        clear_format = QTextCharFormat()
        clear_format.setUnderlineStyle(QTextCharFormat.NoUnderline)
        cursor.mergeCharFormat(clear_format)
        
        # Remove positions in this block from tracking dict
        block_pos = block.position()
        block_len = len(block.text())
        positions_to_remove = [pos for pos in self._misspelled_words.keys() 
                              if block_pos <= pos < block_pos + block_len]
        for pos in positions_to_remove:
            del self._misspelled_words[pos]
            
    def _remove_all_spell_underlines(self, document):
        """Remove all spell check underlines from the document without affecting other formatting."""
        self._misspelled_words.clear()
        cursor = QTextCursor(document)
        cursor.select(QTextCursor.Document)
        clear_format = QTextCharFormat()
        clear_format.setUnderlineStyle(QTextCharFormat.NoUnderline)
        cursor.mergeCharFormat(clear_format)
            
    def _extract_words(self, text):
        """Extract words with their positions from text."""
        words = []
        # Match word characters (letters, numbers, underscores)
        for match in re.finditer(r'\b[a-zA-Z]+\b', text):
            word = match.group()
            # Skip very short words (likely not meaningful)
            if len(word) >= 2:
                words.append((word, match.start()))
        return words
    
    def _clear_highlights(self):
        """Clear all spell check highlights."""
        self._misspelled_words.clear()
        # Reset the document's default format
        document = self.editor.document()
        cursor = QTextCursor(document)
        cursor.select(QTextCursor.Document)
        # Remove wave underline from all text
        fmt = cursor.charFormat()
        fmt.setUnderlineStyle(QTextCharFormat.NoUnderline)
        cursor.setCharFormat(fmt)
        
    def get_word_at_position(self, position):
        """
        Get the misspelled word at a given position, if any.
        
        Args:
            position: Position in the document
            
        Returns:
            Tuple of (word, position, length) or None
        """
        # Check if position is in any misspelled word
        for pos, word in self._misspelled_words.items():
            if pos <= position < pos + len(word):
                return (word, pos, len(word))
        return None
    
    def get_word_under_cursor(self):
        """Get the word under the current cursor position."""
        cursor = self.editor.textCursor()
        position = cursor.position()
        return self.get_word_at_position(position)
