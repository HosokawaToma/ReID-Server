# デプロイ

## 前提条件

- Docker
- Docker Compose
- NVIDIA Container Toolkit

## セットアップ手順

### 1. 環境変数の設定

`.env.example`をコピーして`.env`ファイルを作成します。
必要であれば環境変数を変更してください。

```bash
cp .env.example .env
```

### 2. Dockerイメージのビルドと起動

```bash
docker compose up -d --build
```

### 3. データベースマイグレーション

```bash
docker compose run --rm app python -m alembic upgrade head
```
