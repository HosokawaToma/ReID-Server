"""
人物検出作成アプリケーション。

位置・時刻・画像からカメラフレームを組み立て、人物検出処理の入口となるジョブを登録する役割を持つ。
登録されたジョブはバックグラウンド処理によって人物検出や再同定に利用される。
"""
from environment import Environment
from applications import ApplicationBase
from repositories.person.snapshot.create_queue import RepositoryPersonSnapshotCreateQueue
from dto.location import DtoLocation
from dto.timestamp import DtoTimestamp
from dto.image import DtoImage
from domain.camera_frame.image import DomainCameraFrameImage
from domain.id import DomainId
from domain.location import DomainLocation
from domain.timestamp import DomainTimestamp
from domain.image import DomainImage


class ApplicationPersonSnapshotCreate(ApplicationBase):
    """
    人物検出作成ジョブの登録を担当するアプリケーション。

    受け取った位置・時刻・画像からカメラフレームを組み立て、人物検出処理に必要なジョブを登録する。
    呼び出し時点では検出や再同定は行わず、後続のバックグラウンド処理に委ねる。
    """

    def __init__(
        self,
        repository_person_snapshot_create_queue: RepositoryPersonSnapshotCreateQueue,
    ):
        """
        人物検出作成ジョブの登録先となるリポジトリを受け取る。

        :param RepositoryPersonSnapshotCreateQueue repository_person_snapshot_create_queue: カメラフレームを人物検出作成ジョブとして登録するリポジトリ
        """
        self.repository_person_snapshot_create_queue = repository_person_snapshot_create_queue

    @classmethod
    def create(cls, environment: Environment) -> "ApplicationPersonSnapshotCreate":
        """
        環境設定からリポジトリを組み立て、アプリケーションインスタンスを生成する。

        :param Environment environment: 接続先などの環境設定
        :return ApplicationPersonSnapshotCreate: アプリケーションインスタンス
        """
        return cls(
            repository_person_snapshot_create_queue=RepositoryPersonSnapshotCreateQueue.create(
                environment),
        )

    def save(self, location: DtoLocation, timestamp: DtoTimestamp, image: DtoImage) -> None:
        """
        カメラフレームを作成し人物検出処理の対象として登録する．

        入力は撮影位置、撮影時刻、カメラフレーム画像．
        新規の ID を採番したカメラフレーム画像を人物検出処理の入口として登録する．

        :param DtoLocation location: 撮影位置（カメラID・ビューID）
        :param DtoTimestamp timestamp: 撮影日時
        :param DtoImage image: 画像データ（バイト列とフォーマット）
        """
        self.repository_person_snapshot_create_queue.push(DomainCameraFrameImage(
            id=DomainId(),
            location=DomainLocation(
                camera_id=location.camera_id, view_id=location.view_id),
            timestamp=DomainTimestamp(timestamp=timestamp.timestamp),
            image=DomainImage(bytes=image.bytes, format=image.format),
        ))
