from dataclasses import dataclass

@dataclass(frozen=True)
class DtoPagination:
    total_items: int
    total_pages: int
