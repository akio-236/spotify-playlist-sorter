import logging
import os
from datetime import datetime


def setup_logging(log_dir: str = "logs"):
    """Configure logging for the application"""
    # Ensure log directory exists
    os.makedirs(log_dir, exist_ok=True)

    # Create log filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"app_{timestamp}.log")

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler(log_file), logging.StreamHandler()],
    )

    # Create a logger
    logger = logging.getLogger("spotify_playlist_sorter")

    return logger
