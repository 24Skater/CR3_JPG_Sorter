import json
import os
from typing import Any, Dict, List

class Config:
    """Configuration manager for ImageSorter application."""
    
    DEFAULT_CONFIG = {
        "last_folder": "",
        "recursive": False,
        "move_other": False,
        "custom_extensions": [],
        "window_geometry": "480x340"
    }
    
    def __init__(self, config_file: str = "config.json") -> None:
        """
        Initialize configuration manager.
        
        Args:
            config_file: Path to configuration file
        """
        self.config_file = config_file
        self.config: Dict[str, Any] = self.load()
    
    def load(self) -> Dict[str, Any]:
        """Load configuration from file or create default."""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    return {**self.DEFAULT_CONFIG, **config}
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load config file: {e}")
                return self.DEFAULT_CONFIG.copy()
        return self.DEFAULT_CONFIG.copy()
    
    def save(self) -> None:
        """Save configuration to file."""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2)
        except IOError as e:
            print(f"Warning: Could not save config file: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value and save."""
        self.config[key] = value
        self.save()
    
    def get_custom_extensions(self) -> List[str]:
        """Get list of custom file extensions."""
        return self.config.get("custom_extensions", [])
    
    def add_custom_extension(self, ext: str) -> None:
        """Add a custom file extension."""
        ext = ext.lower()
        if not ext.startswith('.'):
            ext = '.' + ext
        
        custom_exts = self.get_custom_extensions()
        if ext not in custom_exts:
            custom_exts.append(ext)
            self.set("custom_extensions", custom_exts)

# Global config instance
config = Config()

