# HACK

## マイグレーションファイルの作成

```bash
docker compose run --rm app python -m alembic revision --autogenerate
```

## マイグレーションの実行

```bash
docker compose run --rm app python -m alembic upgrade head
```

## テストの実行

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
