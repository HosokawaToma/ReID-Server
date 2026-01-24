from repositories.utils.database import RepositoryUtilDatabase
from repositories.utils.database.query.camera_frame import RepositoryUtilDatabaseQueryCameraFrame
from migration.models.camera_frames import MigrationModelCameraFrame
from domain.id import DomainId
from domain.camera_frame import DomainCameraFrame
from domain.timestamp import DomainTimestamp
from domain.location import DomainLocation
from domain.camera_frame.sequence import DomainCameraFrameSequence
from environment import Environment

class RepositoryCameraFrame:
    def __init__(self, database: RepositoryUtilDatabase):
        self.database = database

    @classmethod
    def create(cls, environment: Environment) -> "RepositoryCameraFrame":
        return cls(
            database=RepositoryUtilDatabase.create(environment),
        )

    def _model_to_domain(self, model: MigrationModelCameraFrame) -> DomainCameraFrame:
        return DomainCameraFrame(
            id=DomainId(id=model.id),
            location=DomainLocation(camera_id=model.camera_id, view_id=model.view_id),
            timestamp=DomainTimestamp(timestamp=model.timestamp),
        )

    def find(self, query: RepositoryUtilDatabaseQueryCameraFrame | None = None) -> DomainCameraFrameSequence:
        with self.database as session:
            session_query = session.query(MigrationModelCameraFrame)
            if query is not None:
                session_query = query.build(session_query)
            models = session_query.all()
            return DomainCameraFrameSequence(items=[self._model_to_domain(model) for model in models])
