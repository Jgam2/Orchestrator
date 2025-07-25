"""
Logging Tool for system logging.
"""

import logging
import sys
from typing import Dict, Any, Optional

def setup_logging(
    level: int = logging.INFO,
    log_file: Optional[str] = None,
    log_format: Optional[str] = None
) -> None:
    """
    Set up logging configuration.
    
    Args:
        level: Logging level
        log_file: Optional log file path
        log_format: Optional log format string
    """
    # Set default format if not provided
    if log_format is None:
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Configure logging
    handlers = []
    
    # Add console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter(log_format))
    handlers.append(console_handler)
    
    # Add file handler if specified
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(logging.Formatter(log_format))
        handlers.append(file_handler)
    
    # Configure root logger
    logging.basicConfig(
        level=level,
        format=log_format,
        handlers=handlers
    )
    
    # Set level for specific loggers
    logging.getLogger("orchestrator").setLevel(level)

class LoggingTool:
    """
    Handles system logging.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the Logging Tool.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config or {}
        self.logger = logging.getLogger("orchestrator")
        
        # Configure logging if not already done
        log_level = self.config.get("log_level", logging.INFO)
        log_file = self.config.get("log_file")
        log_format = self.config.get("log_format")
        
        setup_logging(log_level, log_file, log_format)
        
        self.logger.info("LoggingTool initialized")
    
    def log(self, level: int, message: str, *args, **kwargs) -> None:
        """
        Log a message at the specified level.
        
        Args:
            level: Logging level
            message: Message to log
            *args: Additional positional arguments for the message
            **kwargs: Additional keyword arguments for the message
        """
        self.logger.log(level, message, *args, **kwargs)
    
    def debug(self, message: str, *args, **kwargs) -> None:
        """
        Log a debug message.
        
        Args:
            message: Message to log
            *args: Additional positional arguments for the message
            **kwargs: Additional keyword arguments for the message
        """
        self.logger.debug(message, *args, **kwargs)
    
    def info(self, message: str, *args, **kwargs) -> None:
        """
        Log an info message.
        
        Args:
            message: Message to log
            *args: Additional positional arguments for the message
            **kwargs: Additional keyword arguments for the message
        """
        self.logger.info(message, *args, **kwargs)
    
    def warning(self, message: str, *args, **kwargs) -> None:
        """
        Log a warning message.
        
        Args:
            message: Message to log
            *args: Additional positional arguments for the message
            **kwargs: Additional keyword arguments for the message
        """
        self.logger.warning(message, *args, **kwargs)
    
    def error(self, message: str, *args, **kwargs) -> None:
        """
        Log an error message.
        
        Args:
            message: Message to log
            *args: Additional positional arguments for the message
            **kwargs: Additional keyword arguments for the message
        """
        self.logger.error(message, *args, **kwargs)
    
    def critical(self, message: str, *args, **kwargs) -> None:
        """
        Log a critical message.
        
        Args:
            message: Message to log
            *args: Additional positional arguments for the message
            **kwargs: Additional keyword arguments for the message
        """
        self.logger.critical(message, *args, **kwargs)