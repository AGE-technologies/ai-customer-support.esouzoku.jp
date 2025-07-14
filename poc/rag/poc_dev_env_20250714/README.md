# 検証環境構築

検証環境構築まとめ

## 技術・環境整理

1. データ取得と前処理（BigQuery & DLP）
2. ベクトルデータベース（Pinecone）
3. RAG実行（Claude）
4. 一連のツールを連携・検証する環境（Python）

### 直近決めたいこと・欲しいもの

- ベクトル化を行うためのツールが必要 (or)
  - OpenAI
  - Coreha
- メール回答に適したLLM選定 (or)
  - Claude 3.5 <- APIキーいただいたのでこれでよさそう
  - GPT-4-turbo

## TODO

- [] GCP周り
  - [x] gcloud cliインストール
  - [ ] gcloud 初期化
    - プロジェクトの選択で一旦ストップ。メールデータの溜まっているプロジェクトが知りたいです
  - [] Big Query API、DLP API 有効化
  - [] 認証情報の確認
- [] Python環境
  - [] 仮想環境
  - [] ライブラリインストール
  - [] Claude API クライアント
- [] APIキーの管理
- [] BigQuery・DLP API の疎通確認
- [] Claude Code API の疎通確認
- [] BigQuery と Claude の連携確認
- [] Claude と Pinecone の連携確認
