# Scripts ディレクトリ

このディレクトリには、ReID-Server のセットアップとメンテナンスに使用するスクリプトが含まれています。

## スクリプト一覧

### create_certs.sh

SSL/TLS 証明書を作成するスクリプトです。

**使用方法:**

```bash
DOMAIN=yourdomain.com ./scripts/create_certs.sh
```

**注意:** 現在は参照用のスクリプトです（即座に終了します）。

---

### fix_coturn_tls.sh

Coturn の TLS 設定を修正するスクリプトです。

**問題:**

- Coturn コンテナが`nobody`ユーザーで実行されるため、証明書ファイルの権限が厳しすぎると読み込めない
- docker-compose.yaml で環境変数を使用しているが、未設定の場合に問題が発生

**解決内容:**

1. 証明書ファイル（`localhost.crt`と`localhost.key`）の権限を 644 に変更
2. docker-compose.yaml の証明書パス設定を確認・修正ガイドを表示

**使用方法:**

```bash
./scripts/fix_coturn_tls.sh
```

**修正内容:**

- `resources/certs/localhost.crt` の権限を `644` に変更
- `resources/certs/localhost.key` の権限を `644` に変更

**注意:**

- 本番環境では秘密鍵の権限は 600（所有者のみ）が推奨ですが、Coturn コンテナが`nobody`ユーザーで実行されるため、644 が必要です。
- docker-compose.yaml の証明書パスが環境変数（`${CERT_PATH}`）を使用している場合は、直接パス（`./resources/certs/localhost.crt`）に変更するか、`.env`ファイルに環境変数を設定してください。

---

### alembic.sh

データベースマイグレーションを実行するスクリプトです。

**使用方法:**

```bash
./scripts/alembic.sh
```

---

## Coturn TLS 設定の問題解決手順

### 問題の症状

- `WARNING: cannot find private key file: /etc/coturn/certs/privkey.pem`
- `WARNING: cannot start TLS and DTLS listeners because private key file is not set properly`

### 解決手順

1. **証明書ファイルの権限を修正:**

   ```bash
   chmod 644 resources/certs/localhost.crt
   chmod 644 resources/certs/localhost.key
   ```

2. **docker-compose.yaml の確認:**

   証明書パスが環境変数を使用している場合:

   ```yaml
   volumes:
     - ${CERT_PATH}:/etc/coturn/certs/fullchain.pem:ro
     - ${PKEY_PATH}:/etc/coturn/certs/privkey.pem:ro
   ```

   直接パスに変更（推奨）:

   ```yaml
   volumes:
     - ./resources/certs/localhost.crt:/etc/coturn/certs/fullchain.pem:ro
     - ./resources/certs/localhost.key:/etc/coturn/certs/privkey.pem:ro
   ```

   または、.env ファイルに設定:

   ```bash
   CERT_PATH=/home/komorilab/ReID-Server/resources/certs/localhost.crt
   PKEY_PATH=/home/komorilab/ReID-Server/resources/certs/localhost.key
   ```

3. **Coturn コンテナの再起動:**

   ```bash
   docker compose restart coturn
   ```

4. **動作確認:**

   ```bash
   docker logs reid-server-coturn-1 | grep -E "(TLS|DTLS|Certificate|Private key|ERROR|WARNING)"
   ```

   正常な場合は以下が表示されます:

   - `INFO: Certificate file found`
   - `INFO: Private key file found`
   - `INFO: TLS cipher suite`
   - `INFO: DTLS cipher suite`

   以下の警告が出ていなければ正常です:

   - `WARNING: cannot find private key file`
   - `WARNING: cannot start TLS and DTLS listeners`

---

## トラブルシューティング

### 証明書が見つからない場合

```bash
# 証明書ファイルの確認
ls -la resources/certs/

# 証明書ファイルが存在しない場合は作成
DOMAIN=localhost ./scripts/create_certs.sh
```

### 権限の問題が続く場合

```bash
# ファイルの所有者と権限を確認
ls -la resources/certs/localhost.*

# 所有者が正しくない場合は修正（プロジェクトディレクトリの所有者に）
sudo chown $USER:$USER resources/certs/localhost.*
chmod 644 resources/certs/localhost.*
```
