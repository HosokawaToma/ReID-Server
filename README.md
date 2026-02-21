# 研究目的

# 本システムの説明

# 本システムのセットアップ手順

## 前提条件

本システムは下記システムに依存している．

- Docker
- Docker Compose
- NVIDIA Container Toolkit

## セットアップ手順

### 環境変数の設定

本システムを起動するには `.env` ファイルを作成する必要がある．
`.env` ファイルに記載している環境変数をシステムの設定値として利用している．
使用する環境変数は全て `.env.example` に記載している．
そのため `.env.example` をコピーして `.env` ファイルを作成することを推奨する．

```bash
cp .env.example .env
```

### Dockerイメージのビルドと起動

本システムはDockerコンテナ上で動作する．
全てのDockerコンテナを立ち上げる必要がある．

```bash
docker compose up -d --build
```

### データベースのマイグレーション

本システムはデータベースにRDBを採用している．
そのためテーブル定義が必要である．

```bash
docker compose run --rm app python -m alembic upgrade head
```

# データ収集手順

## カメラシステムを起動

# 評価方法手順

## Webアプリケーションを起動

## 正解ラベルの割り当て

## 評価指標の計算
