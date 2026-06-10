import logging
import os

LOG_DIR = "logs"

os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "application.log")


logging.basicConfig(
    filename=LOG_FILE,
    format="[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logger = logging.getLogger("Youtube_AI_Automation")