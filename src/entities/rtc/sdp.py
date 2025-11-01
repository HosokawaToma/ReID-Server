from dataclasses import dataclass

@dataclass
class EntityRtcSdp:
    sdp: str
    type: str
