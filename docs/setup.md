# セットアップ手順

## 0. 前提条件

- Docker
- NVIDIA Container Toolkit

## 1. .envファイルの作成

```bash
cp .env.example .env
```

## 2. 起動

```bash
docker compose up -d --build
```

## 3. マイグレーション

```bash
docker compose run --rm app python -m alembic upgrade head
```

株式会社スマイル
050-5785-7974

株式会社スマサポ
担当：あべ
0120-195-276
