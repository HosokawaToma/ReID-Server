#!/bin/bash

# ============================================
# 証明書の作成スクリプト
# ============================================
set -e

# スクリプトのディレクトリとプロジェクトのルートディレクトリを取得
# POSIX互換の方法でスクリプトのパスを取得
if [ -n "${BASH_SOURCE:-}" ]; then
    # bashの場合
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
else
    # shやdashの場合
    SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
fi
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

# プロジェクトのルートディレクトリに移動
cd "${PROJECT_ROOT}"

# .envファイルの存在確認
if [ ! -f "${PROJECT_ROOT}/.env" ]; then
    echo "エラー: .envファイルが見つかりません"
    echo "${PROJECT_ROOT}/.env を作成してください"
    exit 1
fi

# .envファイルから必要な変数を読み込む（存在する場合）
# POSIX互換の方法で.envファイルを読み込む
if [ -f "${PROJECT_ROOT}/.env" ]; then
    . "${PROJECT_ROOT}/.env"
fi

# DOMAINが設定されていない場合はlocalhostをデフォルトとして使用
DOMAIN=${DOMAIN:-localhost}

# Dockerが利用可能か確認
if ! command -v docker >/dev/null 2>&1; then
    echo "エラー: Dockerがインストールされていません"
    echo "Dockerをインストールしてから再実行してください"
    exit 1
fi

# 必要な環境変数の確認
if [ -z "${CERTS_PATH}" ]; then
    echo "エラー: CERTS_PATH環境変数が設定されていません"
    echo ".env ファイルに CERTS_PATH を設定してください"
    exit 1
fi

# 証明書ファイルのパスをDOMAINベースで設定
CERT_PATH="${CERTS_PATH}/${CERT_FILE}"
KEY_PATH="${CERTS_PATH}/${KEY_FILE}"

echo "✓ .envファイルを読み込みました"
echo ""

echo "=========================================="
echo "1. SSL/TLS証明書の作成"
echo "=========================================="
echo ""

# 証明書ディレクトリの作成
mkdir -p "${CERTS_PATH}"

# Dockerを使ってopensslを実行する関数
run_openssl() {
    # 証明書ディレクトリを絶対パスに変換（POSIX互換のためlocalは使わない）
    certs_dir="$(cd "${CERTS_PATH}" && pwd)"
    docker run --rm \
        -v "${certs_dir}:/certs" \
        -w /certs \
        frapsoft/openssl \
        $*
}

# 証明書が既に存在するか確認
if [ -f "${CERT_FILE}" ] && [ -f "${KEY_FILE}" ]; then
    echo "✓ 証明書ファイルは既に存在します"
else
    echo "証明書ファイルを作成中..."
    run_openssl req -x509 -nodes -newkey rsa:2048 -days 365 \
        -keyout "$(basename "${KEY_FILE}")" \
        -out "$(basename "${CERT_FILE}")" \
        -subj "/C=JP/ST=Tokyo/L=Chiyoda/O=Dev/CN=${DOMAIN}"
    echo "✓ 証明書ファイルを作成しました"
fi

# 証明書ファイルの権限を644に変更（Coturnコンテナがnobodyユーザーで読み込めるように）
if [ -f "${CERT_FILE}" ]; then
    CERT_PERM=$(stat -c "%a" "${CERT_FILE}")
    if [ "${CERT_PERM}" != "644" ]; then
        chmod 644 "${CERT_FILE}"
        echo "✓ 証明書の権限を644に変更しました"
    else
        echo "✓ 証明書の権限は既に適切です"
    fi
else
    echo "エラー: 証明書ファイルが見つかりません: ${CERT_FILE}"
    exit 1
fi

if [ -f "${KEY_FILE}" ]; then
    KEY_PERM=$(stat -c "%a" "${KEY_FILE}")
    if [ "${KEY_PERM}" != "644" ]; then
        chmod 644 "${KEY_FILE}"
        echo "✓ 秘密鍵の権限を644に変更しました"
    else
        echo "✓ 秘密鍵の権限は既に適切です"
    fi
else
    echo "エラー: 秘密鍵ファイルが見つかりません: ${KEY_FILE}"
    exit 1
fi

echo ""

echo "=========================================="
echo "証明書の作成が完了しました"
echo "=========================================="
echo ""

echo "証明書ファイル:"
echo "  - 証明書: ${CERT_FILE}"
echo "  - 秘密鍵: ${KEY_FILE}"
echo ""

echo "証明書の有効期限:"
# Dockerを使って証明書の実際の有効期限を取得
CERT_NOT_BEFORE=$(run_openssl x509 -in "$(basename "${CERT_FILE}")" -noout -startdate 2>/dev/null | cut -d= -f2)
CERT_NOT_AFTER=$(run_openssl x509 -in "$(basename "${CERT_FILE}")" -noout -enddate 2>/dev/null | cut -d= -f2)
if [ -n "${CERT_NOT_BEFORE}" ] && [ -n "${CERT_NOT_AFTER}" ]; then
    echo "  - 有効開始日: ${CERT_NOT_BEFORE}"
    echo "  - 有効期限: ${CERT_NOT_AFTER}"
else
    # opensslで取得できない場合のフォールバック（Linux用）
    CERT_DATE=$(stat -c %y "${CERT_FILE}" 2>/dev/null | cut -d' ' -f1)
    echo "  - 作成日: ${CERT_DATE}"
    echo "  - 有効期限: 365日（証明書ファイルから確認できませんでした）"
fi
