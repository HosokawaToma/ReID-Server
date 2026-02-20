"""
人物 ID のドメインモデル

人物スナップショットに割り当てる「誰であるか」を表す値。有効な人物には UUID を持たせ、
ゴミ検出（全身未検出・複数人など）の場合は UUID を持たずゴミであることを示すフラグで表現する。
新規採番・ゴミとしてのマーク・同一内容の複製を提供する。
"""
from dataclasses import dataclass, field
from domain.id import DomainId
from domain.utils.base import DomainUtilsBase


@dataclass(frozen=True)
class DomainPersonId(DomainUtilsBase):
    """
    人物 ID のドメインモデル。

    人物を一意に識別する UUID を保持する。ゴミデータの場合は UUID を持たない。
    ゴミであることを示すフラグが True のときは「人物として扱わない」ことを表し、ReID の正解ラベルや同一人物判定で用いる。
    等価・ハッシュは UUID の有無とゴミフラグの両方に基づく。
    """
    id: DomainId | None = field(default=None)
    is_junk: bool = field(default=True)

    @classmethod
    def new_id(cls) -> "DomainPersonId":
        """
        新規の UUID を採番し、ゴミでないことを示すフラグを付けたインスタンスを返す。

        人物検出結果を「有効な 1 人」として扱う際に用いる。

        :return DomainPersonId: 新規 UUID を持ちゴミでないインスタンス
        """
        return cls(id=DomainId(), is_junk=False)

    @classmethod
    def junk(cls) -> "DomainPersonId":
        """
        UUID を持たず、ゴミであることを示すフラグを付けたインスタンスを返す。

        全身未検出・複数人検出などで「人物として扱わない」場合に用いる。

        :return DomainPersonId: ゴミとしてマークされたインスタンス
        """
        return cls(id=None, is_junk=True)

    def copy(self) -> "DomainPersonId":
        """
        同じ UUID とゴミフラグを持つ別インスタンスを返す。

        不変のため、同じ人物 ID を別のドメインオブジェクトに渡す際に用いる。

        :return DomainPersonId: 同一内容の新しいインスタンス
        """
        return DomainPersonId(id=self.id, is_junk=self.is_junk)

    def __eq__(self, other: object) -> bool:
        """
        比較対象が同じ型かつ UUID の有無とゴミフラグがともに等しい場合に True を返す。

        :param object other: 比較対象
        :return bool: 等しければ True
        """
        if not isinstance(other, DomainPersonId):
            return False
        return self.id == other.id and self.is_junk == other.is_junk

    def __hash__(self) -> int:
        """
        UUID とゴミフラグに基づくハッシュを返す。セット・辞書のキーに利用できる。

        :return int: ハッシュ値
        """
        return hash((self.id, self.is_junk))
