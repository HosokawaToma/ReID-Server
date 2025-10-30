#!/bin/bash

# ReID-Server 初期設定スクリプト
# このスクリプトを実行すると、docker compose upだけで動作する状態になります

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

echo "=========================================="
echo "ReID-Server 初期設定"
echo "=========================================="
echo ""

cd "${PROJECT_ROOT}"

# .envファイルの存在確認
if [ ! -f "${PROJECT_ROOT}/.env" ]; then
    echo "エラー: .envファイルが見つかりません"
    echo "${PROJECT_ROOT}/.env を作成してください"
    exit 1
fi

# .envファイルから必要な変数を読み込む
source "${PROJECT_ROOT}/.env"

# DOMAINが設定されていない場合はlocalhostをデフォルトとして使用
DOMAIN=${DOMAIN:-localhost}

echo "✓ .envファイルを読み込みました"
echo ""

# ============================================
# 1. 証明書の作成
# ============================================
echo "=========================================="
echo "1. SSL/TLS証明書の作成"
echo "=========================================="
echo ""

CERT_DIR="${PROJECT_ROOT}/resources/certs"
CERT_FILE="${CERT_DIR}/localhost.crt"
KEY_FILE="${CERT_DIR}/localhost.key"

# 証明書ディレクトリの作成
mkdir -p "${CERT_DIR}"

# 証明書が既に存在するか確認
if [ -f "${CERT_FILE}" ] && [ -f "${KEY_FILE}" ]; then
    echo "✓ 証明書ファイルは既に存在します"
else
    echo "証明書ファイルを作成中..."
    openssl req -x509 -nodes -newkey rsa:2048 -days 365 \
        -keyout "${KEY_FILE}" \
        -out "${CERT_FILE}" \
        -subj "/C=JP/ST=Tokyo/L=Chiyoda/O=Dev/CN=${DOMAIN}"
    echo "✓ 証明書ファイルを作成しました"
fi

echo ""

# ============================================
# 2. 証明書ファイルの権限修正
# ============================================
echo "=========================================="
echo "2. 証明書ファイルの権限修正"
echo "=========================================="
echo ""

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

# ============================================
# 3. docker-compose.yamlの証明書パス修正
# ============================================
echo "=========================================="
echo "3. docker-compose.yamlの設定確認・修正"
echo "=========================================="
echo ""

DOCKER_COMPOSE="${PROJECT_ROOT}/docker-compose.yaml"

if [ ! -f "${DOCKER_COMPOSE}" ]; then
    echo "エラー: docker-compose.yamlが見つかりません"
    exit 1
fi

# docker-compose.yamlで証明書パスが環境変数を使用している場合、直接パスに変更
if grep -q "\${CERT_PATH}:/etc/coturn/certs/fullchain.pem" "${DOCKER_COMPOSE}"; then
    echo "docker-compose.yamlの証明書パスを環境変数から直接パスに変更中..."

    # 一時ファイルを作成
    TEMP_FILE=$(mktemp)

    # 環境変数を直接パスに置換
    sed -e "s|\${CERT_PATH}|./resources/certs/localhost.crt|g" \
        -e "s|\${PKEY_PATH}|./resources/certs/localhost.key|g" \
        "${DOCKER_COMPOSE}" > "${TEMP_FILE}"

    mv "${TEMP_FILE}" "${DOCKER_COMPOSE}"
    echo "✓ docker-compose.yamlの証明書パスを修正しました"
elif grep -q "localhost.crt:/etc/coturn/certs/fullchain.pem" "${DOCKER_COMPOSE}"; then
    echo "✓ docker-compose.yamlの証明書パスは既に直接指定されています"
else
    echo "⚠ 警告: docker-compose.yamlの証明書パス設定が確認できませんでした"
    echo "手動で確認してください"
fi

echo ""

# ============================================
# 4. 必要なディレクトリの作成
# ============================================
echo "=========================================="
echo "4. 必要なディレクトリの作成"
echo "=========================================="
echo ""

# volumesディレクトリの作成
mkdir -p "${PROJECT_ROOT}/volumes/app"
mkdir -p "${PROJECT_ROOT}/volumes/mysql"
mkdir -p "${PROJECT_ROOT}/volumes/chroma"
mkdir -p "${PROJECT_ROOT}/results/identify_person"
mkdir -p "${PROJECT_ROOT}/results/rtc"

echo "✓ 必要なディレクトリを作成しました"
echo ""

# ============================================
# 完了メッセージ
# ============================================
echo "=========================================="
echo "初期設定が完了しました！"
echo "=========================================="
echo ""
echo "次のステップ:"
echo "  1. docker compose up を実行してコンテナを起動"
echo "  2. コンテナ起動後、以下のコマンドでデータベースマイグレーションを実行:"
echo "     ./scripts/alembic.sh"
echo ""
echo "または、docker compose up の後、以下のコマンドでマイグレーションを実行:"
echo "  docker compose exec app alembic upgrade head"
echo ""
echo "注意: データベースマイグレーションはコンテナが起動した後で実行する必要があります"
echo ""

