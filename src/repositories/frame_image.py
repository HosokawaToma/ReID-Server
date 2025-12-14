from repositories import RepositoryDatabase
from repositories import RepositoryStorage
from repositories import RepositoryStorageImage
from repositories import RepositoryStorageImageFindParams
from repositories import RepositoryStorageImageDeleteParams
from error import Error
from domain.frame_image import DomainFrameImage
from environment import Environment
from dataclasses import dataclass
import uuid
from datetime import datetime
from migration.models.frame_image import MigrationModelFrameImage
from sqlalchemy.orm import Query
from PIL import Image

@dataclass
class RepositoryFrameImageFindParams:
    ids: list[uuid.UUID] | None = None

@dataclass
class RepositoryFrameImageDeleteParams:
    id: uuid.UUID

class RepositoryFrameImageError(Error):
    pass

class RepositoryFrameImage:
    def __init__(self, database: RepositoryDatabase, storage: RepositoryStorage):
        self.database = database
        self.storage = storage

    @classmethod
    def create(cls, environment: Environment) -> "RepositoryFrameImage":
        return cls(
            database=RepositoryDatabase.create(
                environment),
            storage=RepositoryStorage.create(
                environment,
                directory="frame_images",
            ),
        )

    def _build_filters(self, query: Query, params: RepositoryFrameImageFindParams) -> Query:
        if params.ids is not None:
            query = query.filter(MigrationModelFrameImage.id.in_(params.ids))
        return query

    def _model_to_domain(self, model: MigrationModelFrameImage, image: Image.Image) -> DomainFrameImage:
        return DomainFrameImage(
            id=uuid.UUID(str(model.id)),
            camera_id=int(str(model.camera_id)),
            view_id=int(str(model.view_id)),
            timestamp=datetime.fromisoformat(str(model.timestamp)),
            image=image,
        )

    def save(self, frame_image: DomainFrameImage) -> None:
        with self.database as session:
            session.add(MigrationModelFrameImage(
                id=frame_image.id,
                camera_id=frame_image.camera_id,
                view_id=frame_image.view_id,
                timestamp=frame_image.timestamp,
            ))
        self.storage.image_save(RepositoryStorageImage(
            name=str(frame_image.id),
            image=frame_image.image,
        ))

    def find_first(self, params: RepositoryFrameImageFindParams | None = None) -> DomainFrameImage:
        with self.database as session:
            query = session.query(MigrationModelFrameImage)
            if params is not None:
                query = self._build_filters(query, params)
            model = query.first()
            if model is None:
                raise RepositoryFrameImageError("Frame image not found")
            image = self.storage.image_find_one(RepositoryStorageImageFindParams(
                name=str(model.id)))
            return self._model_to_domain(model, image.image)

    def delete(self, frame_image: DomainFrameImage) -> None:
        with self.database as session:
            session.query(MigrationModelFrameImage).filter(
                MigrationModelFrameImage.id == frame_image.id,
            ).delete()
        self.storage.image_delete(RepositoryStorageImageDeleteParams(
            name=str(frame_image.id),
        ))
