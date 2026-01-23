from repositories.camera_frame import RepositoryCameraFrame
from repositories.utils.database.query.camera_frame import RepositoryUtilDatabaseQueryCameraFrame
from repositories.utils.database.query.camera_frame import RepositoryUtilDatabaseQueryCameraFrameSortByKey
from dto.camera_frame import DtoCameraFrame
from dto.camera_frame.query import DtoCameraFrameQuery
from environment import Environment
from applications import ApplicationBase

class ApplicationCameraFrameSearch(ApplicationBase):
    def __init__(self, repository_camera_frame: RepositoryCameraFrame):
        self.repository_camera_frame = repository_camera_frame

    @classmethod
    def create(cls, environment: Environment) -> "ApplicationCameraFrameSearch":
        return cls(
            repository_camera_frame=RepositoryCameraFrame.create(environment),
        )

    def search(self, query: DtoCameraFrameQuery | None = None) -> list[DtoCameraFrame]:
        database_query = None
        if query is not None:
            database_query = RepositoryUtilDatabaseQueryCameraFrame(
                ids=query.ids,
                camera_ids=query.camera_ids,
                view_ids=query.view_ids,
                timestamp_after=query.timestamp_after,
                timestamp_before=query.timestamp_before,
                sort_by_list=[
                    RepositoryUtilDatabaseQueryCameraFrameSortByKey(sort_by.value)
                    for sort_by in query.sort_by_list
                ] if query.sort_by_list is not None else None,
            )
        camera_frames = self.repository_camera_frame.find(
            query=database_query,
        )
        return [DtoCameraFrame(
            id=camera_frame.id.id,
            camera_id=camera_frame.location.camera_id,
            view_id=camera_frame.location.view_id,
            timestamp=camera_frame.timestamp.timestamp,
        ) for camera_frame in camera_frames]
