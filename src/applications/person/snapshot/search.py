from repositories.person.snapshot.meta_data import RepositoryPersonSnapshotMetaData
from repositories.utils.database.query.person_snapshot import RepositoryUtilDatabaseQueryPersonSnapshot
from repositories.utils.database.query.person_snapshot import RepositoryUtilDatabaseQueryPersonSnapshotSortByKey
from environment import Environment
from error import Error
from applications import ApplicationBase
from dto.person.snapshot.meta_data import DtoPersonSnapshotMetaData
from dto.person.snapshot.query import DtoPersonSnapshotQuery


class ApplicationPersonSnapshotSearchError(Error):
    pass


class ApplicationPersonSnapshotSearch(ApplicationBase):
    def __init__(
        self,
        repository_person_snapshot_meta_data: RepositoryPersonSnapshotMetaData,
    ):
        self.repository_person_snapshot_meta_data = repository_person_snapshot_meta_data

    @classmethod
    def create(cls, environment: Environment) -> "ApplicationPersonSnapshotSearch":
        return cls(
            repository_person_snapshot_meta_data=RepositoryPersonSnapshotMetaData.create(
                environment=environment,
            ),
        )

    def search(
        self,
        query: DtoPersonSnapshotQuery | None = None,
    ) -> list[DtoPersonSnapshotMetaData]:
        try:
            database_query = None
            if query is not None:
                database_query = RepositoryUtilDatabaseQueryPersonSnapshot(
                    ids=query.ids,
                    camera_ids=query.camera_ids,
                    view_ids=query.view_ids,
                    is_junk=query.is_junk,
                    timestamp_after=query.timestamp_after,
                    timestamp_before=query.timestamp_before,
                    person_ids=query.person_ids,
                    sort_by_list=[
                        RepositoryUtilDatabaseQueryPersonSnapshotSortByKey(sort_by.value)
                        for sort_by in query.sort_by_list
                    ] if query.sort_by_list is not None else None,
                )
            meta_data_sequence = self.repository_person_snapshot_meta_data.find(query=database_query)
            return meta_data_sequence.to_dto()
        except Error as error:
            raise ApplicationPersonSnapshotSearchError(error) from error
