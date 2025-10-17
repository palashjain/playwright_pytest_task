import configparser
from pathlib import Path
from typing import Optional


class ConfigManager:
    _instance: Optional['ConfigManager'] = None
    _config: Optional[configparser.ConfigParser] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance._initialize_config()
        return cls._instance
    
    def _initialize_config(self) -> None:
        self._config = configparser.ConfigParser()
        config_path = Path(__file__).parent.parent / 'config' / 'config.ini'
        
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        self._config.read(config_path)
    
    def get(self, section: str, key: str, fallback: str = None) -> str:
        return self._config.get(section, key, fallback=fallback)
    
    def get_int(self, section: str, key: str, fallback: int = None) -> int:
        return self._config.getint(section, key, fallback=fallback)
    
    def get_boolean(self, section: str, key: str, fallback: bool = None) -> bool:
        return self._config.getboolean(section, key, fallback=fallback)
    
    @property
    def base_url(self) -> str:
        return self.get('APP', 'base_url')
    
    @property
    def browser(self) -> str:
        return self.get('APP', 'browser', 'chromium')
    
    @property
    def headless(self) -> bool:
        return self.get_boolean('APP', 'headless', False)
    
    @property
    def timeout(self) -> int:
        return self.get_int('APP', 'timeout', 30000)
    
    @property
    def username(self) -> str:
        return self.get('CREDENTIALS', 'username')
    
    @property
    def password(self) -> str:
        return self.get('CREDENTIALS', 'password')
    
    @property
    def downloads_path(self) -> Path:
        base_path = Path(__file__).parent.parent
        return base_path / self.get('PATHS', 'downloads_path', 'downloads')
    
    @property
    def testdata_path(self) -> Path:
        base_path = Path(__file__).parent.parent
        return base_path / self.get('PATHS', 'testdata_path', 'testData')

    @property
    def screenshots_path(self) -> Path:
        base_path = Path(__file__).parent.parent
        return base_path / self.get('PATHS', 'screenshots_path', 'screenshots')
