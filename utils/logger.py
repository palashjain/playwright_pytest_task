import logging
from pathlib import Path
from typing import Optional
from datetime import datetime


class Logger:
    _instance: Optional['Logger'] = None
    _logger: Optional[logging.Logger] = None
    
    def __new__(cls, name: str = 'PlaywrightFramework'):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._initialize_logger(name)
        return cls._instance
    
    def _initialize_logger(self, name: str) -> None:
        self._logger = logging.getLogger(name)
        self._logger.setLevel(logging.DEBUG)
        
        if self._logger.handlers:
            return
        
        log_dir = Path(__file__).parent.parent / 'logs'
        log_dir.mkdir(exist_ok=True)
        
        log_file = log_dir / f'test_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        self._logger.addHandler(file_handler)
        self._logger.addHandler(console_handler)
    
    def get_logger(self) -> logging.Logger:
        return self._logger
    
    def debug(self, message: str) -> None:
        self._logger.debug(message)
    
    def info(self, message: str) -> None:
        self._logger.info(message)
    
    def warning(self, message: str) -> None:
        self._logger.warning(message)
    
    def error(self, message: str) -> None:
        self._logger.error(message)
    
    def critical(self, message: str) -> None:
        self._logger.critical(message)
