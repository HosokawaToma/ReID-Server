### テストの実行

```bash
# すべてのテストを実行
docker compose run --rm app python -m pytest

# カバレッジレポート付きで実行
docker compose run --rm app python -m pytest --cov=src --cov-report=html

# 特定のテストファイルを実行
docker compose run --rm app python -m pytest tests/test_modules_hasher.py

# マーカーでフィルタリング（例: ユニットテストのみ）
docker compose run --rm app python -m pytest -m unit
```

### テストの構成

- テストファイルは `tests/` ディレクトリに配置
- テスト設定は `pytest.ini` に記載
- 共通フィクスチャは `tests/conftest.py` に定義
