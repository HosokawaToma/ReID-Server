from dataclasses import dataclass
from domain.timestamp import DomainTimestamp
from domain.utils.base import DomainUtilsBase

@dataclass(frozen=True)
class DomainToken(DomainUtilsBase):
    """
    トークンのドメインモデル
    """
    token: str
    expires_at: DomainTimestamp
