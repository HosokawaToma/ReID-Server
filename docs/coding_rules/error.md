# エラー

## 1. エラーハンドリング

### 1.1. Repository層

### 1.2. Application層

### 1.3. Presentation層

### 1.4. Domainクラス

## 2. カスタムエラー

### 2.1. システムエラー（`CustomSystemError`）

- アプリケーションのバグやインフラの問題など、想定外の事態に発生するエラー

#### 2.1.1. 内部サーバーエラー（`InternalServerError`）

- 予期せぬ例外の発生に対して投げるエラー
- HTTPステータス: `500 Internal Server Error`

#### 2.1.2. 外部連携エラー（`BadGatewayError`）

- 外部システムが原因の予期せぬ例外の発生に対して投げるエラー
- HTTPステータス: `502 Bad Gateway`

#### 2.1.3. サービス利用不可エラー（`ServiceUnavailableError`）

- サーバーが一時的にリクエストを処理できない場合に対して投げるエラー
- HTTPステータス: `503 Service Unavailable`

#### 2.1.4. タイムアウトエラー（`GatewayTimeoutError`）

- 処理が規定時間内に終わらなかった場合に対して投げるエラー
- HTTPステータス: `504 Gateway Timeout`

### 2.2. クライアントエラー（`ClientError`）

- クライアントのリクエスト内容に問題がある場合に発生するエラー

#### 2.2.1 認証エラー（`AuthenticationError`）

- 不正なログイン情報に対して投げるエラー
- HTTPステータス: `401 Unauthorized`

#### 2.2.2 認可エラー（`AuthorizationError`）

- 不正な権限アクセスに対して投げるエラー
- HTTPステータス: `403 Forbidden`

#### 2.2.3 バリデーションエラー（`ValidationError`）

- 不正な入力形式に対して投げるエラー
- HTTPステータス: `400 Bad Request`

#### 2.2.4 未検出エラー（`NotFoundError`）

- 不正なデータアクセスに対して投げるエラー
- HTTPステータス: `404 Not Found`

#### 2.2.5. ビジネスロジックエラー（`BusinessError`）

- 仕様上不正な処理に対して投げるエラー

##### 2.2.5.1. 競合エラー（`ConflictError`）

- 不正なデータ重複に対して投げるエラー
- HTTPステータス: `409 Conflict`

##### 2.2.5.2. 処理不要エラー（`UnprocessableError`）

- 不正な業務ルール違反に対して投げるエラー
- HTTPステータス: `422 Unprocessable Entity`

#### 2.2.6. レートリミットエラー（`TooManyRequestsError`）

- 不正なリクエスト数に対して投げるエラー
- HTTPステータス: `429 Too Many Requests`

#### 2.2.7. ペイロード過大エラー（`PayloadTooLargeError`）

- 不正なデータ量に対して投げるエラー
- HTTPステータス: `413 Payload Too Large`
