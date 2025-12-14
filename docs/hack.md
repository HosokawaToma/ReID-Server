# HACK

## マイグレーションファイルの作成

```bash
docker compose run --rm app python -m alembic revision --autogenerate
```

## マイグレーションの実行

```bash
docker compose run --rm app python -m alembic upgrade head
```
