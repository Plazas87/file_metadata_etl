"""ETL Orchestrator module."""
import logging
import pathlib
from typing import List

from .dtos import VideoMetaData
from .services import IExtractor, ILoader

logger = logging.getLogger(__name__)


class Orchestrator:
    """ETL Orchestrator."""

    _extractor: IExtractor[VideoMetaData, pathlib.Path]
    _loader: ILoader[VideoMetaData]
    _memory_buffer: int
    _root_video_path: str
    _dates: List[str]

    def __init__(
        self,
        extractor: IExtractor[VideoMetaData, pathlib.Path],
        loader: ILoader[VideoMetaData],
        root_video_path: str,
        dates: List[str],
        memory_buffer: int = 10,
    ) -> None:
        """Class constructor."""
        self._extractor = extractor
        self._loader = loader
        self._root_video_path = root_video_path
        self._dates = dates
        # Create the database table if does not exists. Use a context manager to handle connection cicle.
        with self._loader as db_client:
            db_client.create_table()

        self._memory_buffer = memory_buffer

    def run(self) -> None:
        """Execute the ETL process."""
        # Control memory data to avoid out of memory crashes using a buffer of 10 data registes at time
        logger.info("ETL Started")

        video_data_list: List[VideoMetaData] = []
        for date in self._dates:
            path = self._root_video_path / pathlib.Path(date)

            logger.info("Processing Path: '%s", path)
            for data_in_memory_count, video_data in enumerate(self._extractor.extract(path=path)):
                video_data_list.append(video_data)
                # if the buffer is full then save the data
                if data_in_memory_count % self._memory_buffer == 0:
                    with self._loader as db_client:
                        db_client.load(data=video_data_list)

                    video_data_list = []

        logger.info("ETL completed")
