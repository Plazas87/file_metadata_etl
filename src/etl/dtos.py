from dataclasses import dataclass


@dataclass
class VideoMetaData:
    """VideoMetaData data tranfer object."""
    
    name: str
    extension: str
    size: str
    absolute_path: str
    