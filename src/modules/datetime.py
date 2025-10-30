from datetime import datetime

class ModuleDatetime:
    def from_iso_format(self, timestamp: str) -> datetime:
        return datetime.fromisoformat(timestamp)
