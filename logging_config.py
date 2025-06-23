import logging
import sys

def setup_logging(level=logging.INFO):
    """
    Set up logging configuration for the entire application.
    
    Args:
        level: The logging level (default: DEBUG)
    """
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),  # Print to console
        ],
        force=True  # Override any existing configuration
    )

def get_logger(name):
    """
    Get a logger with the specified name.
    
    Args:
        name: The name for the logger (usually __name__)
        
    Returns:
        A configured logger instance
    """
    return logging.getLogger(name)