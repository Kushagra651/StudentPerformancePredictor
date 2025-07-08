# import logging
# import os
# from datetime import datetime

# # Create logs directory
# logs_dir = os.path.join(os.getcwd(), "logs")
# os.makedirs(logs_dir, exist_ok=True)

# # Generate log file path inside the logs directory
# log_filename = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
# LOG_FILE_PATH = os.path.join(logs_dir, log_filename)

# # Configure logging
# logging.basicConfig(
#     filename=LOG_FILE_PATH,
#     format='[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s',
#     level=logging.INFO,
# )

# # Test logging
# if __name__ == "__main__":
#     logging.info("Logging has started.")

import logging
import os
from datetime import datetime

# Create logs directory
logs_dir = os.path.join(os.getcwd(), "logs")
os.makedirs(logs_dir, exist_ok=True)

# Log file name with timestamp
log_filename = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
LOG_FILE_PATH = os.path.join(logs_dir, log_filename)

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE_PATH),
        logging.StreamHandler()
    ]
)


if __name__ == "__main__":
    logging.info("Logging has started.")


