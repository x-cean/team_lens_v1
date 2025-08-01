import logging
import sys

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    handlers=[
        logging.FileHandler("project.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("team_lens_v1")