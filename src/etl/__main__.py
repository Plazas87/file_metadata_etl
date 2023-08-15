"""Application entrypoint."""
import logging
import pathlib
import sys

from .config import settings
from .orquestrator import Orchestrator
from .services.dates_processor import DatesProcessor
from .services.extractor import VideoDataExtractor
from .services.loader import DataLoader

logging.basicConfig(format='%(asctime)s %(message)s', level="INFO")
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    # Generate dates to be loaded.
    dates_processor = DatesProcessor(date_format=settings.DATE_INPUT_FORMAT)
    dates = dates_processor.process(initial_date=sys.argv[1], end_date=sys.argv[2])

    # Data Extractor
    video_extractor = VideoDataExtractor()

    # Data Loader
    data_loader = DataLoader(
        database_name=settings.POSTGRES_DB,
        user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        host=settings.PG_HOST,
        port=settings.PG_PORT,
        table_name=settings.PG_VIDEO_TABLE_NAME,
    )

    # ETL orquestractor
    orchestrator = Orchestrator(
        extractor=video_extractor,
        loader=data_loader,
        root_video_path=pathlib.Path(settings.VIDEO_PATH),
        dates=dates,
    )

    # Start the ETL
    orchestrator.run()
