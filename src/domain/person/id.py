from dataclasses import dataclass, field
from domain.id import DomainId
from domain.utils.base import DomainUtilsBase

@dataclass(frozen=True)
class DomainPersonId(DomainUtilsBase):
    """
    人物のIDのドメインモデル
    """
    id: DomainId | None = field(default=None)
    is_junk: bool = field(default=True)

    @classmethod
    def new_id(cls) -> "DomainPersonId":
        """
        新しい人物IDを生成する
        人物IDが割り当てられている場合はゴミデータではない
        :return DomainPersonId: 新しい人物ID
        """
        return cls(id=DomainId(), is_junk=False)

    @classmethod
    def junk(cls) -> "DomainPersonId":
        """
        ゴミデータとして設定する
        ゴミデータには人物IDが割り当てられていない
        :return DomainPersonId: ゴミデータとして設定した人物ID
        """
        return cls(id=None, is_junk=True)

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
