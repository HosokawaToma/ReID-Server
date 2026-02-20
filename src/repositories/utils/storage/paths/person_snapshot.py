"""
人物スナップショット画像のストレージパス

person_snapshots ディレクトリ内のファイル名を ID で表す。
"""
from dataclasses import dataclass
from domain.id import DomainId
from repositories.utils.storage.paths.base import RepositoryUtilStoragePathBase
from typing import ClassVar


@dataclass
class RepositoryUtilStoragePathPersonSnapshot(RepositoryUtilStoragePathBase):
    """
    人物スナップショット画像のストレージパスを保持する。person_snapshots ディレクトリ内で ID をファイル名とする。
    """
    directory: ClassVar[str] = "person_snapshots"
    id: DomainId

    @property
    def name(self) -> str:
        """スナップショットIDの文字列をファイル名として返す。"""
        return str(self.id)
