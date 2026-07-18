"""
Settings Manager Utility
"""

import os
import json

import constants


class SettingsManager:
    """Manages application settings persistence"""
    
    def __init__(self):
        # Use a settings file in the same directory as the script
        self.settings_file = os.path.join(os.path.dirname(__file__), '..', constants.SETTINGS_FILE_NAME)
        self.settings = self.load_settings()
    
    def load_settings(self):
        """Load settings from file, return defaults if not found"""
        default_settings = constants.DEFAULT_SETTINGS.copy()
        
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    loaded_settings = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    default_settings.update(loaded_settings)
            except (json.JSONDecodeError, IOError):
                pass
        
        return default_settings
    
    def save_settings(self):
        """Save settings to file"""
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=4)
        except IOError as e:
            print(f"Warning: Could not save settings: {e}")
    
    def get(self, key, default=None):
        """Get a setting value"""
        return self.settings.get(key, default)
    
    def set(self, key, value):
        """Set a setting value"""
        self.settings[key] = value
