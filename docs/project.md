# プロジェクト構成

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

### `src/applications/`
アプリケーション層。ビジネスロジックを担当。

### `src/background/`
バックグラウンド処理。非同期タスクを担当。

### `src/domain/`
ドメイン層。ドメインモデルとビジネスルールを定義。

### `src/dto/`
データ転送オブジェクト。レイヤー間のデータ受け渡しに使用。

### `src/migration/`
データベースマイグレーション。ORMモデルとマイグレーションスクリプトを含む。

### `src/modules/`
外部モジュール（ReIDモデルなど）。

### `src/presentation/`
プレゼンテーション層。APIエンドポイントを担当。

### `src/repositories/`
リポジトリ層。データ永続化を担当。

### `src/tests/`
ユニットテスト。

### `docs/`
プロジェクトのドキュメント。

### `scripts/`
各種スクリプト。

