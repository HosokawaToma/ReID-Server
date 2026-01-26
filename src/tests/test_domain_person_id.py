import pytest
import uuid
from domain.person.id import DomainPersonId
from domain.id import DomainId


class TestDomainPersonId:
    """DomainPersonIdクラスのテスト"""

    def test_from_model_with_person_id_and_not_junk(self):
        """person_idがあり、ゴミデータではない場合のテスト"""
        test_uuid = uuid.uuid4()
        result = DomainPersonId.from_model(person_id=test_uuid, is_junk=False)
        
        assert result.id is not None
        assert result.id.id == test_uuid
        assert result.is_junk is False

    def test_from_model_with_person_id_and_junk(self):
        """person_idがあり、ゴミデータの場合のテスト"""
        test_uuid = uuid.uuid4()
        result = DomainPersonId.from_model(person_id=test_uuid, is_junk=True)
        
        assert result.id is not None
        assert result.id.id == test_uuid
        assert result.is_junk is True

    def test_from_model_with_none_person_id_and_junk(self):
        """person_idがなく、ゴミデータの場合のテスト"""
        result = DomainPersonId.from_model(person_id=None, is_junk=True)
        
        assert result.id is None
        assert result.is_junk is True

    def test_from_model_with_none_person_id_and_not_junk(self):
        """person_idがなく、ゴミデータではない場合のテスト（矛盾しているがモデルから生成可能）"""
        result = DomainPersonId.from_model(person_id=None, is_junk=False)
        
        assert result.id is None
        assert result.is_junk is False

    def test_from_model_creates_equivalent_object_to_manual_construction(self):
        """from_modelが手動構築と同じオブジェクトを生成することを確認"""
        test_uuid = uuid.uuid4()
        
        # from_modelを使用した場合
        from_model_result = DomainPersonId.from_model(person_id=test_uuid, is_junk=False)
        
        # 手動で構築した場合（Repository層で以前使われていた方法）
        manual_result = DomainPersonId(
            id=DomainId(id=test_uuid) if test_uuid is not None else None,
            is_junk=False,
        )
        
        assert from_model_result == manual_result
        assert from_model_result.id == manual_result.id
        assert from_model_result.is_junk == manual_result.is_junk

    def test_from_model_creates_equivalent_object_with_none(self):
        """from_modelがNoneの場合も手動構築と同じオブジェクトを生成することを確認"""
        # from_modelを使用した場合
        from_model_result = DomainPersonId.from_model(person_id=None, is_junk=True)
        
        # 手動で構築した場合（Repository層で以前使われていた方法）
        manual_result = DomainPersonId(
            id=None,
            is_junk=True,
        )
        
        assert from_model_result == manual_result
        assert from_model_result.id == manual_result.id
        assert from_model_result.is_junk == manual_result.is_junk
