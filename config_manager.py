# config_manager.py
"""
Configuration Manager for Flux
This file can be used standalone or compiled into an executable.
"""

import json
import os
from pathlib import Path

class ConfigManager:
    """Handles saving and loading application settings from a file."""
    
    # Use app data directory for config file
    @staticmethod
    def get_config_path():
        """Get the config file path."""
        if os.name == 'nt':  # Windows
            app_data = os.getenv('APPDATA')
            config_dir = Path(app_data) / "Flux"
        else:  # Linux/Mac
            config_dir = Path.home() / ".config" / "Flux"
        
        config_dir.mkdir(parents=True, exist_ok=True)
        return config_dir / "config.json"
    
    # Default configuration settings
    DEFAULT_CONFIG = {
        # General
        "homepage": "https://www.google.com",
        "new_tab_page": "homepage",  # "homepage", "blank", or "restore"
        "search_engine": "https://www.google.com/search?q={}",
        "ask_download_location": True,
        
        # Appearance
        "tab_position": "top",  # "top" or "left"
        "compact_mode": False,
        "theme": "dark",  # "dark", "light", or "auto"
        
        # Privacy
        "cookie_policy": "allow_all",  # "allow_all", "block_third_party", "block_all"
        "do_not_track": False,
        "allow_location": False,
        "allow_notifications": False,
        
        # Advanced
        "hardware_acceleration": True,
        "javascript_enabled": True,
        "auto_load_images": True,
        "plugins_enabled": False,
        "edit_mode_enabled": False,
        "dev_tools_enabled": True,
        # On first launch, show welcome onboarding
        "first_run": True,
    }

    def __init__(self):
        """Initialize config manager."""
        self.config_file = self.get_config_path()
        self.config = self.load_config()

    def load_config(self):
        """Loads configuration from file or returns defaults."""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    # Merge with defaults to handle new settings
                    config = self.DEFAULT_CONFIG.copy()
                    config.update(loaded_config)
                    return config
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not read config file. Using defaults. Error: {e}")
                return self.DEFAULT_CONFIG.copy()
        else:
            # Save default config
            default_config = self.DEFAULT_CONFIG.copy()
            self.config = default_config
            self.save_config()
            return default_config

    def save_config(self):
        """Saves the current configuration to file."""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4)
        except IOError as e:
            print(f"Error: Could not save config file. Error: {e}")

    def get_setting(self, key):
        """Retrieves a setting by key."""
        return self.config.get(key, self.DEFAULT_CONFIG.get(key))

    def set_setting(self, key, value):
        """Sets a setting value."""
        self.config[key] = value

    def reset_to_defaults(self):
        """Reset all settings to defaults."""
        self.config = self.DEFAULT_CONFIG.copy()
        self.save_config()


# Standalone test
if __name__ == "__main__":
    manager = ConfigManager()
    print("Config file location:", manager.config_file)
    print("Current settings:", json.dumps(manager.config, indent=2))