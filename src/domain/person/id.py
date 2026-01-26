from dataclasses import dataclass, field
from domain.id import DomainId
from domain.utils.base import DomainUtilsBase
import uuid

@dataclass(frozen=True)
class DomainPersonId(DomainUtilsBase):
    """
    人物のIDのドメインモデル
    """
    id: DomainId | None = field(default=None)
    is_junk: bool = field(default=True)

    @staticmethod
    def from_model(person_id: uuid.UUID | None, is_junk: bool) -> "DomainPersonId":
        """
        データベースモデルから人物IDを生成する
        :param uuid.UUID | None person_id: データベースの人物ID
        :param bool is_junk: ゴミデータかどうか
        :return DomainPersonId: 人物ID
        """
        return DomainPersonId(
            id=DomainId(id=person_id) if person_id is not None else None,
            is_junk=is_junk,
        )

    def new_id(self) -> "DomainPersonId":
        """
        新しい人物IDを生成する
        人物IDが割り当てられている場合はゴミデータではない
        :return DomainPersonId: 新しい人物ID
        """
        return DomainPersonId(id=DomainId(), is_junk=False)

    def junk(self) -> "DomainPersonId":
        """
        ゴミデータとして設定する
        ゴミデータには人物IDが割り当てられていない
        :return DomainPersonId: ゴミデータとして設定した人物ID
        """
        return DomainPersonId(id=None, is_junk=True)

    def copy(self) -> "DomainPersonId":
        """
        人物IDを複製する
        :return DomainPersonId: 人物IDを複製した人物ID
        """
        return DomainPersonId(id=self.id, is_junk=self.is_junk)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DomainPersonId):
            return False
        return self.id == other.id and self.is_junk == other.is_junk

    def __hash__(self) -> int:
        return hash((self.id, self.is_junk))
