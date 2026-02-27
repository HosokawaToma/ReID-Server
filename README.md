# 研究目的

本システムは，複数のカメラから取得した映像フレームを用いて **人物検出・人物再同定（ReID）・人流解析** を行うためのサーバシステムである．
街区や施設内のカメラをまたいで人物の移動を追跡し，人流パターンを定量的に把握することを目的としている．

- **人物検出**: カメラフレームから人物領域のみを切り出す
- **選別処理**: 再同定に不適切な画像（他者の混入・姿勢不良など）を除外候補として識別
- **人物再同定（ReID）**: CLIP-ReID による特徴ベクトル抽出と類似度計算により，同一人物を紐付け
- **評価機能**: CMC 曲線や mAP を算出し，再同定性能を定量評価

これらの機能を通じて，カメラ機種や設置環境に依存しない，拡張性と保守性の高い人流計測基盤を提供する．

# 本システムの説明

本システムは，Web API とバックグラウンドジョブワーカーから構成されるサーバサイドアプリケーションである．
API がクライアントからのカメラ画像を受信しバックグラウンドワーカーが **物体検出 → 選別 → 特徴量抽出 → 再同定 → 評価** の各処理を非同期に実行する．
データは RDB（PostgreSQL）およびベクトル検索拡張（pgvector）に保存され，人物検出画像・特徴量・人物 ID・ジャンクフラグなどを一貫して管理する．

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

## カメラ画像（人物検出）の送信 API

本システムは，クライアント（カメラ側）から送信される **カメラフレーム画像** を起点として人流データを生成する．
人物検出キューへの投入は `POST /person/snapshot/create` エンドポイントで行う．

- **HTTP メソッド / パス**
  - `POST /person/snapshot/create`
- **認証**
  - 管理クライアント向け Bearer トークン（`Authorization: Bearer <token>`）必須
- **コンテンツタイプ**
  - `multipart/form-data` または `application/json`（実装は `PresentationUtilFromImage` などのユーティリティを経由）
- **リクエストパラメータ**
  - `image`:
    - 種別: 画像バイナリ
    - 説明: カメラで撮影した 1 フレーム分の画像
  - `timestamp`:
    - 種別: 文字列（ISO 8601 形式 `YYYY-MM-DDTHH:MM:SS`）
    - 説明: 撮影日時
  - `camera_id`:
    - 種別: 整数
    - 説明: カメラ ID（地点 ID としても扱う）
  - `view_id`:
    - 種別: 整数
    - 説明: ビュー ID（シーン ID）
- **レスポンス**
  - 成功時: `200 OK`
    - ボディ例:
      - `{"message": "Person snapshot created"}`
  - バリデーションエラーなど: `400 Bad Request`

- **内部処理の流れ（概要）**
  1. クライアントが `/person/snapshot/create` に画像・撮影時刻・カメラ ID・ビュー ID を送信する
  2. サーバが受信内容を検証し，カメラフレームおよび人物検出ジョブをキューに投入する
  3. API は受け付け完了レスポンスを即時に返す（非同期処理）
  4. バックグラウンドワーカーがキューを監視し，人物検出画像の生成・選別・特徴量抽出・再同定を非同期で実行する

カメラフレームや人物検出結果の検索には，例えば `POST /frame/search/{page}`，`POST /person/snapshot/search/{page}` などの検索 API を利用できる（ページ番号はパス，検索条件は JSON ボディ）。
詳細な検索条件やレスポンススキーマは `src/presentation/camera_frame/search.py` および `src/presentation/person/snapshot/search/__init__.py` を参照すること．

# 評価方法手順

## 正解ラベルの割り当て API

人物再同定の精度評価を行うためには，人物検出画像（スナップショット）に対して **人手による正解人物 ID（Ground Truth）** を付与する必要がある．
正解ラベルの検索・割り当てには，主に次の API を利用する．

- **人物検出一覧の取得**
  - `POST /person/snapshot/search/{page}`
    - パスパラメータ: `page`（1 始まりのページ番号）
    - リクエストボディ（任意，JSON）例:
      - `{"camera_ids": [1], "timestamp_after": "...", "timestamp_before": "..." }`
    - レスポンス: `person_snapshots` 配列と `pagination`（`total_items`, `total_pages`）

- **正解ラベル一覧の取得**
  - `POST /person/snapshot/answer/search`
    - リクエストボディ（任意，JSON）:
      - `person_snapshot_ids`: 人物検出 ID 一覧（UUID の配列）
      - `person_ids`: 人物 ID 一覧（UUID の配列）
      - `is_junk`: ゴミフラグ（`true` / `false`）
      - `sort_by_list`: 作成日時の昇順/降順（`"created_at_asc"`, `"created_at_desc"`）
    - レスポンス: `person_snapshot_answers` 配列（`id`, `person_id`, `is_junk` など）

- **正解ラベルの一括割り当て**
  - `POST /person/snapshot/answer/assign`
    - リクエストボディ（必須，JSON）:
      - `source_person_snapshot_id`: 正解ラベルのコピー元となる人物検出 ID（UUID）
      - `target_person_snapshot_ids`: 正解ラベルをコピーする人物検出 ID 一覧（UUID の配列）
    - レスポンス: 成功時 `200 OK` と
      - `{"message": "Answer label assigned"}`

これらの API を組み合わせることで，対象期間・カメラを絞り込んだ上で人物検出を検索し，個々のスナップショットに人物 ID を付与したり，代表スナップショットから他の複数スナップショットへ正解 ID を一括コピーしたりできる．
こうして，指定日・試行ごとに評価用の正解ラベル付きデータセットを構成する．

## 評価指標の計算 API（CMC / mAP）

正解ラベルの付与が完了したら，専用の評価エンドポイントを呼び出して ReID の照合精度を算出する．
本システムは，仕様書で定義される **CMC 曲線（Rank-k）** と **mAP** を評価指標として利用し，ジャンク込み・ジャンク除外の両条件で結果を返す．

- **再同定評価の実行**
  - `GET /reid/evaluation/{date}/{attempt}`
    - パスパラメータ:
      - `date`: 評価対象日（`YYYY-MM-DD` 形式）
      - `attempt`: 試行回数（整数）
    - 認証:
      - 現状，認証不要（公開エンドポイント）
    - レスポンス（200 OK）
      - `cmc_curve_with_junk`: ジャンク込みの CMC 曲線（Rank-k の配列）
      - `cmc_curve_without_junk`: ジャンク除外の CMC 曲線
      - `map_with_junk`: ジャンク込みの mAP 値
      - `map_without_junk`: ジャンク除外の mAP 値
      - `query_person_ids`: 評価に用いたクエリ人物 ID 一覧（UUID 文字列の配列）

このエンドポイントは，指定日の人物検出データと付与済みの正解ラベルに基づき，Market1501 と同一の考え方でクエリ・ギャラリを定義して CMC 曲線および mAP を自動計算する．
利用者は，評価対象の日付と試行番号を指定して `/reid/evaluation/{date}/{attempt}` を呼び出すだけで，ジャンク込み・ジャンク除外の両方の指標を取得できる．

# ドキュメント

- `docs/specification.md`: システム全体の仕様書（目的・要件・評価指標など）
- `docs/develop/rules.md`: 開発ルール（機能要件・非機能要件・保守性など）
- `docs/develop/coding_rule.md`: コーディング規約
- `docs/develop/design_rule.md`: 設計ルール（ここを見るとコードが読みやすくなるよ思うよ）
- `docs/develop/unit_test.md`: ユニットテストに関するルール
- `docs/hack.md`: よく使うコマンドや開発メモ
