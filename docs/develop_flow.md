# 開発フロー

## 1. Issueのアサイン

- 未着手のIssueから着手するものを選択し、自分をAssignee（担当者）に設定してください。
- 要件や仕様が不明瞭な場合は、この段階でコメント等で質問し、認識齟齬を防ぎます。
- メモとしてコメントを使用することも推奨しています。

## 2. ローカルでブランチの作成

- 最新のデフォルトブランチ（現在は `main`）から、作業用のフィーチャーブランチを作成します。
- フィーチャーブランチは必ず `feature/#{Issue番号}` にしてください。
  - 内容を命名で示したい場合は `feature/#{Issue番号}-{任意の命名}` としてください。

## 3. 開発

- コミットの粒度は、変更内容がわかるような論理的な単位で分割してください。
- コミットメッセージには、プレフィックスをつけることを推奨します
  - 例: `feat:`, `fix:`, `refactor:`, `docs:`
- 必ずローカルで動作確認および単体テストを実行し、エラーがないことを確認してください。


## 4. Pull Requestの作成

- ある程度実装が完了したら（またはWIP段階でも）、リモートリポジトリへプッシュし、Pull Request (PR) を作成します。
- タイトルは、Issueと同じものを使うことを推奨しています。
- 概要は、用意されているPRテンプレートに沿って記述してください。

## 5. CIパイプライン

- PRを作成すると自動的にCI（継続的インテグレーション）が走ります。
- CIが「Red（失敗）」の状態ではマージできません。エラーログを確認し、修正コミットを追加してください。

## 6. コードレビュー

- 開発者は、返ってきたレビューをResolve conversationしてはいけません。
- 開発者は、返ってきたレビュー全てに対し、コメントを返信しなければいけません。
- レビューには以下のラベルが付与されており、種類により対応を変更してください。

ラベル | 期待するアクション | 意味
-- | -- | --
![must](https://img.shields.io/badge/review-must-red.svg) | 修正必須 | 対応しなければマージができない指摘
![imo](https://img.shields.io/badge/review-imo-orange.svg) | 修正任意 | 基本的に対応してほしい指摘
![nits](https://img.shields.io/badge/review-nits-green.svg) | 修正任意 | 変更の提案
![next-badge](https://img.shields.io/badge/review-next-blueviolet) | 修正不要 | 他Issueなどで対応する指摘
![ask](https://img.shields.io/badge/review-ask-blue.svg) | 回答必須 | コードの意図や仕様について確認したい
![suggestion](https://img.shields.io/badge/review-suggestion-blue.svg) |  |
![memo-badge](https://img.shields.io/badge/review-memo-lightgrey) | ただの雑談(勿論スルー可) | コード理解・解説のためのメモ書き
![good-badge](https://img.shields.io/badge/review-good-blightgreen.svg) | ただの雑談(勿論スルー可) | いいなーって思ったやつにつける

### 6.1. GitHub Copilotによるコードレビュー

- 開発が終了し、CIが通ったら、GitHub Copilotへレビュー依頼を送ります。
- GitHub Copilotは、![must](https://img.shields.io/badge/review-must-red.svg) 又は ![imo](https://img.shields.io/badge/review-imo-orange.svg) 又は ![nits](https://img.shields.io/badge/review-nits-green.svg) 以外のレビューを送信しません。
  - もししていた場合は無視をする対応をしてください。
  - 明らかに的外れであった場合は、ラベルに関係せず未対応にすることが許されます（コメントの返信は必須）。

### 6.2. 人によるコードレビュー

- 開発が終了し、CIが通り、Github Copilotのレビュー全てにコメントを返信をした場合は、@HosokawaToma にコードレビューを依頼します。
- レビュー担当者が必要であると判断した場合は、再度GitHub Copilotへレビュー依頼を送ります。

## 7. デフォルトブランチへマージ

- 開発が終了し、CIが通り、レビュー担当者から apploved をもらった場合、デフォルトブランチへマージしてください。
