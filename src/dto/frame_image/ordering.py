from dataclasses import dataclass
from typing import Literal

@dataclass
class DtoFrameImageOrdering:
    ordering: list[Literal["timestamp_asc", "timestamp_desc"]]
