from dataclasses import dataclass, field
import uuid

@dataclass
class DomainPersonSnapshotDetection:
    """
    人物検出の検出結果に関するドメイン知識を集約する
    :param uuid.UUID person_snapshot_id: 人物検出のID
    :param int class_id: クラスID
    :param float confidence: 信頼度
    :param int x: x座標
    :param int y: y座標
    :param int width: 幅
    :param int height: 高さ
    :param uuid.UUID id: 人物検出のID
    """
    person_snapshot_id: uuid.UUID
    class_id: int
    confidence: float
    x: int
    y: int
    width: int
    height: int
    id: uuid.UUID = field(default_factory=uuid.uuid4)
