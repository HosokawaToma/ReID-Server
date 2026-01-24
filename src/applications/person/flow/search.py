from repositories.person.snapshot import RepositoryPersonSnapshot
from repositories.utils.database.query.person_snapshot import RepositoryUtilDatabaseQueryPersonSnapshot
from environment import Environment
from applications import ApplicationBase
from dto.person.flow import DtoPersonFlow
from dto.person.flow.query import DtoPersonFlowQuery


class ApplicationPersonFlowSearch(ApplicationBase):
    def __init__(
        self,
        repository_person_snapshot: RepositoryPersonSnapshot,
    ):
        self.repository_person_snapshot = repository_person_snapshot

    @classmethod
    def create(cls, environment: Environment) -> "ApplicationPersonFlowSearch":
        return cls(
            repository_person_snapshot=RepositoryPersonSnapshot.create(
                environment=environment,
            ),
        )

    def search(self, query: DtoPersonFlowQuery | None = None) -> list[DtoPersonFlow]:
        """
        人流を検索する
        :param DtoPersonFlowQuery query: 人流検索条件
        :return list[DtoPersonFlow]: 人流リスト
        :raises ApplicationPersonFlowSearchError: 人流検索に失敗した場合に発生するエラー
        """
        database_query = None
        if query is not None:
            database_query = RepositoryUtilDatabaseQueryPersonSnapshot(
                timestamp_after=query.timestamp_after,
                timestamp_before=query.timestamp_before,
                person_ids=[query.person_id],
            )
        person_snapshots = self.repository_person_snapshot.find_details(query=database_query)
        flows = person_snapshots.to_flows()
        return [DtoPersonFlow(
            person_id=flow.person_id.id,
            source_camera_id=flow.source_location.camera_id,
            target_camera_id=flow.target_location.camera_id,
            source_timestamp=flow.source_timestamp.timestamp,
            target_timestamp=flow.target_timestamp.timestamp,
        ) for flow in flows]
