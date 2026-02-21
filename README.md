# 研究目的

# 本システムの説明

## ファイル・ディレクトリ構成

```
ReID-Server/
├── .cursor/                              # Cursor設定
├── .github/                              # GitHub設定
├── docs/                                 # ドキュメント
├── src/                                  # ソースコード
│   ├── applications/                     # アプリケーション層
│   ├── background/                       # バックグラウンド処理
│   ├── domain/                           # ドメインモデル
│   ├── dto/                              # データ転送オブジェクト
│   ├── migration/                        # データベースのマイグレーション
│   ├── modules/                          # 外部モジュール（ReIDモデルなど）
│   ├── presentation/                     # プレゼンテーション層
│   ├── repositories/                     # リポジトリ層
│   ├── tests/                            # ユニットテスト
│   ├── background_main.py                # バックグラウンドプロセスのエントリポイント
│   ├── environment.py                    # 環境変数管理
│   ├── error.py                          # エラー定義
│   ├── logger.py                         # ロガー
│   └── main.py                           # WebAPIサーバのエントリポイント
├── .cursorrules                          # Cursorルール
├── .env.example                          # 環境変数ファイル例
├── .gitignore                            # Git除外設定
├── .python-version                       # Pythonバージョン
├── Caddyfile                             # Caddy設定ファイル
├── dev.Caddyfile                         # 開発環境用Caddy設定
├── prod.Caddyfile                        # 本番環境用Caddy設定
├── Dockerfile                            # Dockerイメージ定義
├── LICENSE                               # ライセンス
├── README.md                             # README
├── alembic.ini                           # Alembic設定
├── docker-compose.yaml                   # Docker Compose設定
├── docker-compose.override.yaml.example  # Docker Compose上書き設定例
├── exampl.http                           # HTTPリクエスト例
├── init.sql                              # データベース初期化SQL
├── pyrightconfig.json                    # Pyright設定
├── pytest.ini                            # pytest設定
└── requirements.txt                      # Python依存パッケージ
```

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
