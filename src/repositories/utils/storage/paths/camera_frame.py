from dataclasses import dataclass
from domain.id import DomainId
from repositories.utils.storage.paths.base import RepositoryUtilStoragePathBase
from typing import ClassVar

@dataclass
class RepositoryUtilStoragePathCameraFrame(RepositoryUtilStoragePathBase):
    """
    カメラフレーム画像のパスを表すドメインモデル
    保存先がcamera_frame_imagesではなくframe_imagesになっているのは、過去の設計に合わせているため
    Todo: 将来的にcamera_frame_imagesに変更する
    :param directory: ディレクトリ
    :param id: カメラフレームID
    """
    directory: ClassVar[str] = "frame_images"
    id: DomainId

    @property
    def name(self) -> str:
        return str(self.id)
