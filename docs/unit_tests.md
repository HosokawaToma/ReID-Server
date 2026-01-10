### テストの実行

```bash
# すべてのテストを実行
pytest

# カバレッジレポート付きで実行
pytest --cov=src --cov-report=html

# 特定のテストファイルを実行
pytest tests/test_modules_hasher.py

# マーカーでフィルタリング（例: ユニットテストのみ）
pytest -m unit
```

### テストの構成

- テストファイルは `tests/` ディレクトリに配置
- テスト設定は `pytest.ini` に記載
- 共通フィクスチャは `tests/conftest.py` に定義
