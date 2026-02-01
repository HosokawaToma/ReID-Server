from dataclasses import dataclass

@dataclass(frozen=True)
class DtoReidCmcCurve:
    """
    CMC曲線を表すDTO
    """
    cmc_curve: list[float]
