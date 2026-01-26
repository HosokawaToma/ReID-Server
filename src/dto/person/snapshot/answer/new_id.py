import uuid


class DtoPersonSnapshotAnswerNewId:
    def __init__(self, person_snapshot_id: uuid.UUID, person_id: uuid.UUID | None, is_junk: bool):
        """
        人物検出結果の正解ラベルの新しいIDを表すDTO
        :param uuid.UUID person_snapshot_id: 人物検出結果のID
        :param uuid.UUID | None person_id: 正解人物のID（ゴミデータの場合はNone）
        :param bool is_junk: 正解人物がゴミデータかどうか
        """
        self.person_snapshot_id = person_snapshot_id
        self.person_id = person_id
        self.is_junk = is_junk
