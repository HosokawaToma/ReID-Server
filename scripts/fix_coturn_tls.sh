#!/bin/bash

# Coturn TLS設定の修正スクリプト
#
# このスクリプトは、CoturnコンテナでTLS証明書が正しく読み込まれるように設定を修正します。
#
# 問題点:
# 1. 証明書ファイルの権限が厳しすぎて、Coturnコンテナ（nobodyユーザー）が読み込めない
# 2. docker-compose.yamlで環境変数を使用しているが、未設定の場合に問題が発生
#
# 解決策:
# 1. 証明書ファイルの権限を644に変更（所有者以外も読み取り可能に）
# 2. docker-compose.yamlの証明書パスを直接指定に変更（環境変数ではなく）

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

echo "=========================================="
echo "Coturn TLS設定の修正"
echo "=========================================="
echo ""

# 証明書ファイルのパス
CERT_FILE="${PROJECT_ROOT}/resources/certs/localhost.crt"
KEY_FILE="${PROJECT_ROOT}/resources/certs/localhost.key"

# 証明書ファイルの存在確認
if [ ! -f "${CERT_FILE}" ]; then
    echo "エラー: 証明書ファイルが見つかりません: ${CERT_FILE}"
    echo "先に create_certs.sh を実行して証明書を作成してください。"
    exit 1
fi

if [ ! -f "${KEY_FILE}" ]; then
    echo "エラー: 秘密鍵ファイルが見つかりません: ${KEY_FILE}"
    echo "先に create_certs.sh を実行して証明書を作成してください。"
    exit 1
fi

echo "✓ 証明書ファイルの存在を確認"
echo ""

# 証明書ファイルの権限を確認・修正
echo "証明書ファイルの権限を確認・修正中..."

CERT_PERM=$(stat -c "%a" "${CERT_FILE}")
KEY_PERM=$(stat -c "%a" "${KEY_FILE}")

echo "  証明書の現在の権限: ${CERT_PERM}"
echo "  秘密鍵の現在の権限: ${KEY_PERM}"

# 証明書ファイルの権限を644に変更（所有者以外も読み取り可能）
if [ "${CERT_PERM}" != "644" ]; then
    echo "  証明書の権限を644に変更中..."
    chmod 644 "${CERT_FILE}"
    echo "  ✓ 証明書の権限を変更しました"
else
    echo "  ✓ 証明書の権限は既に適切です"
fi

# 秘密鍵ファイルの権限を644に変更
# 注意: 本番環境では600（所有者のみ読み書き可能）が推奨ですが、
# Coturnコンテナがnobodyユーザーで実行されるため、644が必要
if [ "${KEY_PERM}" != "644" ]; then
    echo "  秘密鍵の権限を644に変更中..."
    chmod 644 "${KEY_FILE}"
    echo "  ✓ 秘密鍵の権限を変更しました"
else
    echo "  ✓ 秘密鍵の権限は既に適切です"
fi

echo ""
echo "=========================================="
echo "docker-compose.yamlの設定確認"
echo "=========================================="
echo ""

DOCKER_COMPOSE="${PROJECT_ROOT}/docker-compose.yaml"

if [ ! -f "${DOCKER_COMPOSE}" ]; then
    echo "警告: docker-compose.yamlが見つかりません: ${DOCKER_COMPOSE}"
    exit 1
fi

# docker-compose.yamlで証明書パスが直接指定されているか確認
if grep -q "localhost.crt:/etc/coturn/certs/fullchain.pem" "${DOCKER_COMPOSE}"; then
    echo "✓ docker-compose.yamlの証明書パスは既に直接指定されています"
elif grep -q "\${CERT_PATH}:/etc/coturn/certs/fullchain.pem" "${DOCKER_COMPOSE}"; then
    echo "⚠ docker-compose.yamlで環境変数\${CERT_PATH}が使用されています"
    echo ""
    echo "以下のように修正してください:"
    echo ""
    echo "変更前:"
    echo "  - \${CERT_PATH}:/etc/coturn/certs/fullchain.pem:ro"
    echo "  - \${PKEY_PATH}:/etc/coturn/certs/privkey.pem:ro"
    echo ""
    echo "変更後:"
    echo "  - ./resources/certs/localhost.crt:/etc/coturn/certs/fullchain.pem:ro"
    echo "  - ./resources/certs/localhost.key:/etc/coturn/certs/privkey.pem:ro"
    echo ""
    echo "または、.envファイルに以下を設定してください:"
    echo "  CERT_PATH=${PROJECT_ROOT}/resources/certs/localhost.crt"
    echo "  PKEY_PATH=${PROJECT_ROOT}/resources/certs/localhost.key"
fi

echo ""
echo "=========================================="
echo "Coturnコンテナの再起動"
echo "=========================================="
echo ""

read -p "Coturnコンテナを再起動しますか？ (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    cd "${PROJECT_ROOT}"
    docker compose restart coturn
    echo ""
    echo "✓ Coturnコンテナを再起動しました"
    echo ""
    echo "ログを確認してください:"
    echo "  docker logs reid-server-coturn-1 | grep -E '(TLS|DTLS|Certificate|Private key)'"
else
    echo "スキップしました。手動で再起動してください:"
    echo "  docker compose restart coturn"
fi

echo ""
echo "=========================================="
echo "完了"
echo "=========================================="
echo ""
echo "修正内容の確認:"
echo "  1. 証明書ファイルの権限を644に変更"
echo "  2. docker-compose.yamlの証明書パス設定を確認"
echo ""
echo "TLSが正しく動作しているか確認するコマンド:"
echo "  docker logs reid-server-coturn-1 | grep 'TLS'"
echo ""
echo "警告 'cannot start TLS and DTLS listeners' が表示されなければ正常です。"

