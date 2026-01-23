from repositories.person.snapshot import RepositoryPersonSnapshot
from repositories.utils.database.query.person_snapshot import RepositoryUtilDatabaseQueryPersonSnapshot
from repositories.utils.database.query.person_snapshot import RepositoryUtilDatabaseQueryPersonSnapshotSortByKey
from environment import Environment
from error import Error
from applications import ApplicationBase
from dto.person.snapshot.detail import DtoPersonSnapshotDetail
from dto.person.snapshot.query import DtoPersonSnapshotQuery


class ApplicationPersonSnapshotSearchError(Error):
    pass


class ApplicationPersonSnapshotSearch(ApplicationBase):
    def __init__(
        self,
        repository_person_snapshot: RepositoryPersonSnapshot,
    ):
        self.repository_person_snapshot = repository_person_snapshot

    @classmethod
    def create(cls, environment: Environment) -> "ApplicationPersonSnapshotSearch":
        return cls(
            repository_person_snapshot=RepositoryPersonSnapshot.create(
                environment=environment,
            ),
        )

    def search(
        self,
        query: DtoPersonSnapshotQuery | None = None,
    ) -> list[DtoPersonSnapshotDetail]:
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
            detail_sequence = self.repository_person_snapshot.find_details(query=database_query)
            return [DtoPersonSnapshotDetail(
                id=detail.id.id,
                camera_id=detail.location.camera_id,
                view_id=detail.location.view_id,
                timestamp=detail.timestamp.timestamp,
                is_junk=detail.person_id.is_junk,
                person_id=detail.person_id.id.id if detail.person_id.id is not None else None,
            ) for detail in detail_sequence]
        except Error as error:
            raise ApplicationPersonSnapshotSearchError(error) from error
