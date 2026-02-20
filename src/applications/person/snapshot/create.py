"""
人物検出作成アプリケーション

カメラフレーム（位置・時刻・画像）を受け取り、人物検出パイプラインの入口となる作成キューに 1 件投入する。
実際の検出・ゴミ判定・特徴量抽出・ReID はバックグラウンドワーカーがキューから取り出して行う。
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
    人物検出作成のキュー投入を担当するアプリケーション。

    受け取った位置・時刻・画像をカメラフレーム画像として組み立て、作成キュー（Redis）に 1 件追加する。
    キュー投入に合わせて DB へのフレーム登録とストレージへの画像保存も行う。
    呼び出しが返る時点では人物検出（YOLO・ReID）は未実行で、バックグラウンドで順次処理される。
    """

    def __init__(
        self,
        repository_person_snapshot_create_queue: RepositoryPersonSnapshotCreateQueue,
    ):
        """
        人物検出作成キュー用リポジトリを設定する。

        :param RepositoryPersonSnapshotCreateQueue repository_person_snapshot_create_queue: キューへの投入と DB/ストレージ同期を行うリポジトリ
        """
        self.repository_person_snapshot_create_queue = repository_person_snapshot_create_queue

    @classmethod
    def create(cls, environment: Environment) -> "ApplicationPersonSnapshotCreate":
        """
        環境変数からキューリポジトリを組み立て、アプリケーションインスタンスを生成する。

        :param Environment environment: 環境変数（Redis・DB・ストレージ接続先）
        :return ApplicationPersonSnapshotCreate: アプリケーションインスタンス
        """
        return cls(
            repository_person_snapshot_create_queue=RepositoryPersonSnapshotCreateQueue.create(
                environment),
        )

    def save(self, location: DtoLocation, timestamp: DtoTimestamp, image: DtoImage) -> None:
        """
        1 件のカメラフレームを人物検出作成キューに投入する。

        入力は撮影位置（カメラID・ビューID）、撮影時刻、画像のバイト列とフォーマット。
        新規の UUID を採番したカメラフレーム画像としてキューに追加し、あわせて DB へのフレーム登録とストレージへの画像保存を行う。
        キュー投入または DB/ストレージ処理に失敗した場合は InternalServerError となる。

        :param DtoLocation location: 撮影位置（カメラID・ビューID）
        :param DtoTimestamp timestamp: 撮影日時
        :param DtoImage image: 画像データ（バイト列とフォーマット）
        :raises InternalServerError: キュー投入または DB/ストレージ処理に失敗した場合
        """
        self.repository_person_snapshot_create_queue.push(DomainCameraFrameImage(
            id=DomainId(),
            location=DomainLocation(
                camera_id=location.camera_id, view_id=location.view_id),
            timestamp=DomainTimestamp(timestamp=timestamp.timestamp),
            image=DomainImage(bytes=image.bytes, format=image.format),
        ))
