"""
カメラフレーム画像のストレージパス

frame_images ディレクトリ内のファイル名を ID で表す。
"""
from dataclasses import dataclass
from domain.id import DomainId
from repositories.utils.storage.paths.base import RepositoryUtilStoragePathBase
from typing import ClassVar


@dataclass
class RepositoryUtilStoragePathCameraFrame(RepositoryUtilStoragePathBase):
    """
    カメラフレーム画像のストレージパスを保持する。frame_images ディレクトリ内で ID をファイル名とする。

    保存先が camera_frame_images ではなく frame_images なのは過去の設計に合わせている。
    Todo: 将来的に camera_frame_images に変更する。
    """
    directory: ClassVar[str] = "frame_images"
    id: DomainId

    @property
    def name(self) -> str:
        """カメラフレームIDの文字列をファイル名として返す。"""
        return str(self.id)
