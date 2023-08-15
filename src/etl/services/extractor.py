"""Data extractor module."""
import pathlib
from typing import Generator, List

from ..dtos import VideoMetaData
from ..services import IExtractor


class VideoDataExtractor(IExtractor):
    """VideoDataExtractor class."""

    _root_video_path: pathlib.Path

    def extract(self, path: pathlib.Path) -> Generator[VideoMetaData, None, None]:
        """Load and prepare the data to be processed."""
        # iter over all files in a directory and generate metadata
        for video_path in list(path.rglob("*.*")):
            yield VideoMetaData(
                name=video_path.stem,
                extension=video_path.suffix,
                size=video_path.stat().st_size,
                absolute_path=str(video_path.absolute()),
            )
