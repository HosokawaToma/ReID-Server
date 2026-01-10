# 1. テストの実行

```bash
# すべてのテストを実行
docker compose run --rm app python -m pytest

# カバレッジレポート付きで実行
docker compose run --rm app python -m pytest --cov=src --cov-report=html

# 特定のテストファイルを実行
docker compose run --rm app python -m pytest src/tests/test_modules_hasher.py

# マーカーでフィルタリング（例: ユニットテストのみ）
docker compose run --rm app python -m pytest -m unit
```

# 2. テストの構成

- テストファイルは `src/tests/` ディレクトリに配置
- テスト設定は `pytest.ini` に記載
- 共通フィクスチャは `src/tests/conftest.py` に定義

# 3. テストの書き方

## 3.1. 単体テスト

- モックを用い，テスト対象のみをテストすることを単体テストとする
- 単体テストには `pytest.mark.unit` マーカーを設定する
- 単体テストの実行時間は最大でも 10ms 以下とする
- 単体テストはテスト対象のロジックのみをテストすることを目的とする

## 3.2. 統合テスト

- モックを用いず，テスト対象と依存する他のモジュールをテストすることを統合テストとする
- 統合テストには `pytest.mark.integration` マーカーを設定する
- 統合テストの実行時間は最大でも 100ms 以下とする
- 統合テストはテスト対象と依存する他のモジュールをまとめてテストすることを目的とする
