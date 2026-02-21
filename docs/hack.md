# HACK

## Docker関連

### コンテナの起動・停止

```bash
# 全コンテナを起動
docker compose up

# 全コンテナを停止
docker compose down

# 全コンテナを停止（ボリュームも削除）
docker compose down -v

# コンテナを再起動
docker compose restart

# 特定のサービスのみ起動
docker compose up -d app

# コンテナを再ビルドして起動
docker compose up -d --build
```

### ログ確認

```bash
# 全コンテナのログを表示
docker compose logs -f

# 特定のコンテナのログを表示
docker compose logs -f app

# 最新100行のログを表示
docker compose logs --tail=100 app

# 特定の時間以降のログを表示
docker compose logs --since 10m app
```

### コンテナ内でコマンド実行

```bash
# appコンテナ内でシェルを起動
docker compose exec app bash

# 特定のPythonスクリプトを実行
docker compose exec app python src/main.py

# バックグラウンドワーカーコンテナ内でシェルを起動
docker compose exec background-app bash
```

## データベース関連

### マイグレーション

```bash
# マイグレーションファイルの作成
docker compose run --rm app python -m alembic revision --autogenerate -m "マイグレーションメッセージ"

# マイグレーションの実行（最新まで）
docker compose run --rm app python -m alembic upgrade head

# マイグレーションの実行（1つ前のバージョンに戻す）
docker compose run --rm app python -m alembic downgrade -1

# マイグレーション履歴の確認
docker compose run --rm app python -m alembic history

# 現在のマイグレーションバージョンを確認
docker compose run --rm app python -m alembic current
```

### データベース接続

```bash
# PostgreSQLに接続
docker compose exec database psql -U ${POSTGRESQL_USER} -d ${POSTGRESQL_DATABASE}

# データベース一覧を表示
docker compose exec database psql -U ${POSTGRESQL_USER} -l

# テーブル一覧を表示
docker compose exec database psql -U ${POSTGRESQL_USER} -d ${POSTGRESQL_DATABASE} -c "\dt"

# 特定のテーブルの構造を確認
docker compose exec database psql -U ${POSTGRESQL_USER} -d ${POSTGRESQL_DATABASE} -c "\d person_snapshots"

# SQLクエリを実行
docker compose exec database psql -U ${POSTGRESQL_USER} -d ${POSTGRESQL_DATABASE} -c "SELECT COUNT(*) FROM person_snapshots;"
```

### データベースバックアップ・リストア

```bash
# バックアップを作成
docker compose exec database pg_dump -U ${POSTGRESQL_USER} ${POSTGRESQL_DATABASE} > backup_$(date +%Y%m%d_%H%M%S).sql

# バックアップからリストア
docker compose exec -T database psql -U ${POSTGRESQL_USER} ${POSTGRESQL_DATABASE} < backup.sql

# カスタムフォーマットでバックアップ（推奨）
docker compose exec database pg_dump -U ${POSTGRESQL_USER} -Fc ${POSTGRESQL_DATABASE} > backup_$(date +%Y%m%d_%H%M%S).dump

# カスタムフォーマットからリストア
docker compose exec -T database pg_restore -U ${POSTGRESQL_USER} -d ${POSTGRESQL_DATABASE} < backup.dump
```

## Redis関連

### Redis接続

```bash
# Redis CLIに接続
docker compose exec redis redis-cli

# Redis内のキー一覧を表示
docker compose exec redis redis-cli KEYS "*"

# 特定のキーの値を確認
docker compose exec redis redis-cli GET "キー名"

# キュー（リスト）の長さを確認
docker compose exec redis redis-cli LLEN "person_snapshot_create_queue"

# キュー（リスト）の内容を確認（削除せずに）
docker compose exec redis redis-cli LRANGE "person_snapshot_create_queue" 0 -1

# すべてのキーを削除（注意: 本番環境では使用しない）
docker compose exec redis redis-cli FLUSHALL
```

## ストレージ関連

```bash
# ストレージボリューム内のファイル一覧を確認
docker compose exec app ls -la /app/storage

# ストレージボリューム内の特定ディレクトリを確認
docker compose exec app ls -la /app/storage/person_snapshots

# ストレージボリュームの使用量を確認
docker volume inspect ReID-Server_app_storage
```

## テスト関連

```bash
# すべてのテストを実行
docker compose run --rm app python -m pytest

# カバレッジレポート付きで実行
docker compose run --rm app python -m pytest --cov=src --cov-report=html

# 特定のテストファイルを実行
docker compose run --rm app python -m pytest src/tests/test_modules_hasher.py

# 特定のテストクラスを実行
docker compose run --rm app python -m pytest src/tests/test_modules_hasher.py::TestHasher

# 特定のテスト関数を実行
docker compose run --rm app python -m pytest src/tests/test_modules_hasher.py::TestHasher::test_hash

# マーカーでフィルタリング（例: ユニットテストのみ）
docker compose run --rm app python -m pytest -m unit

# 詳細な出力で実行
docker compose run --rm app python -m pytest -v

# 最初に失敗したテストで停止
docker compose run --rm app python -m pytest -x

# 並列実行（pytest-xdistが必要）
docker compose run --rm app python -m pytest -n auto
```
