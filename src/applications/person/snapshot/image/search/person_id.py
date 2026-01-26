from environment import Environment
from repositories.person.snapshot import RepositoryPersonSnapshot
from repositories.utils.database.query.person_snapshot import RepositoryUtilDatabaseQueryPersonSnapshot
from applications import ApplicationBase
from dto.id import DtoId
import uuid


class ApplicationPersonSnapshotImageSearchPersonId(ApplicationBase):
    def __init__(
        self,
        repository_person_snapshot: RepositoryPersonSnapshot,
    ):
        self.repository_person_snapshot = repository_person_snapshot

    @classmethod
    def create(cls, environment: Environment) -> "ApplicationPersonSnapshotImageSearchPersonId":
        return cls(
            repository_person_snapshot=RepositoryPersonSnapshot.create(environment),
        )

    def search(self, person_id: DtoId) -> list[uuid.UUID]:
        """
        人物IDに紐づく人物検出画像IDリストを検索する
        :param DtoId person_id: 人物ID
        :return list[uuid.UUID]: 人物検出画像IDリスト
        """
        # person_idで人物検出IDのリストを取得
        database_query = RepositoryUtilDatabaseQueryPersonSnapshot(
            person_ids=[person_id.id],
        )
        id_sequence = self.repository_person_snapshot.find_ids(query=database_query)
        
        # IDのリストを返す
        return [snapshot_id.id for snapshot_id in id_sequence.items]
