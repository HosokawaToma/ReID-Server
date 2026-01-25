from sqlalchemy import UUID, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
import uuid
from datetime import datetime
import sqlalchemy as sa

Base = declarative_base()

class MigrationModelPersonSnapshotsAnswerLabels(Base):
    """
    人物検出結果の正解ラベルを保存するテーブル
    機械的に割り当てるIDではなく、人の手で割り当てるIDを保存する
    :param UUID person_snapshot_id: 人物検出結果のID
    :param UUID person_id: 正解人物のID
    :param bool is_junk: 正解人物がゴミデータかどうか
    :param datetime created_at: 作成日時
    :param datetime updated_at: 更新日時
    """
    __tablename__ = "person_snapshots_answer_labels"
    person_snapshot_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("person_snapshots.id")
        nullable=False,
        primary_key=True,
    )
    person_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
    )
    is_junk: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=sa.func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=sa.func.now(),
        onupdate=sa.func.now(),
        nullable=False,
    )
