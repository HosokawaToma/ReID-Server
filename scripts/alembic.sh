#!/bin/bash
set -euo pipefail

# Alembic マイグレーションスクリプト
# 使用方法:
#   ローカル実行:
#     ./scripts/alembic.sh "マイグレーションメッセージ"  # マイグレーションの作成と実行
#     ./scripts/alembic.sh --create-only "メッセージ"    # マイグレーションファイルの作成のみ
#     ./scripts/alembic.sh --upgrade-only                # マイグレーションの実行のみ
#
#   Docker Compose実行:
#     docker compose run --rm app alembic upgrade head
#     docker compose run --rm app alembic revision --autogenerate -m "メッセージ"
#
#   ./scripts/alembic.sh --help                       # ヘルプを表示

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

show_help() {
    cat << EOF
Alembic マイグレーションスクリプト

使用方法:
  $0 [オプション] [メッセージ]

オプション:
  --create-only     マイグレーションファイルの作成のみ（実行しない）
  --upgrade-only    マイグレーションの実行のみ（作成しない）
  --help           このヘルプメッセージを表示

例（ローカル実行）:
  $0 "ユーザーテーブルにemailカラムを追加"
  $0 --create-only "新しいテーブルを作成"
  $0 --upgrade-only

例（Docker Compose実行）:
  # マイグレーションの実行のみ
  docker compose run --rm app alembic upgrade head

  # マイグレーションファイルの作成
  docker compose run --rm app alembic revision --autogenerate -m "メッセージ"

  # 作成と実行を一度に
  docker compose run --rm app bash -c "alembic revision --autogenerate -m 'メッセージ' && alembic upgrade head"
EOF
}

CREATE_ONLY=false
UPGRADE_ONLY=false

# 引数の解析
while [[ $# -gt 0 ]]; do
    case $1 in
        --create-only)
            CREATE_ONLY=true
            shift
            ;;
        --upgrade-only)
            UPGRADE_ONLY=true
            shift
            ;;
        --help|-h)
            show_help
            exit 0
            ;;
        -*)
            echo "エラー: 不明なオプション: $1" >&2
            show_help
            exit 1
            ;;
        *)
            MESSAGE="$1"
            shift
            ;;
    esac
done

cd "$PROJECT_ROOT"

# マイグレーションファイルの作成
if [[ "$UPGRADE_ONLY" == false ]]; then
    if [[ -z "${MESSAGE:-}" ]]; then
        echo "エラー: マイグレーションメッセージが必要です" >&2
        echo "使用方法: $0 \"マイグレーションメッセージ\"" >&2
        exit 1
    fi

    echo "マイグレーションファイルを作成中..."
    alembic revision --autogenerate -m "$MESSAGE"
    echo "✓ マイグレーションファイルの作成が完了しました"
fi

# マイグレーションの実行
if [[ "$CREATE_ONLY" == false ]]; then
    echo "マイグレーションを実行中..."
    alembic upgrade head
    echo "✓ マイグレーションの実行が完了しました"
fi
