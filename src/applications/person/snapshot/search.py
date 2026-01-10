from dao.person.snapshot.meta_data import DaoPersonSnapshotMetaData
from database.query.person_snapshot import DatabaseQueryPersonSnapshot
from database.query.person_snapshot import DatabaseQueryPersonSnapshotSortByKey
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
        dao_person_snapshot_meta_data: DaoPersonSnapshotMetaData,
    ):
        self.dao_person_snapshot_meta_data = dao_person_snapshot_meta_data

    @classmethod
    def create(cls, environment: Environment) -> "ApplicationPersonSnapshotSearch":
        return cls(
            dao_person_snapshot_meta_data=DaoPersonSnapshotMetaData.create(
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
                database_query = DatabaseQueryPersonSnapshot(
                    ids=query.ids,
                    camera_ids=query.camera_ids,
                    view_ids=query.view_ids,
                    is_junk=query.is_junk,
                    timestamp_after=query.timestamp_after,
                    timestamp_before=query.timestamp_before,
                    person_ids=query.person_ids,
                    sort_by_list=[
                        DatabaseQueryPersonSnapshotSortByKey(sort_by.value)
                        for sort_by in query.sort_by_list
                    ] if query.sort_by_list is not None else None,
                )
            return self.dao_person_snapshot_meta_data.find(query=database_query)
        except Error as error:
            raise ApplicationPersonSnapshotSearchError(error) from error
