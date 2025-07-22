# AI Customer Support Assistant

AIを活用したカスタマーサポート自動化システム。BigQueryのメール対応履歴を学習し、HubSpotで高品質な回答を生成します。

## 🏗️ システム構成

```
Webhook → RAG検索 → 回答生成 → HubSpot書き込み
    ↑         ↑
BigQuery → DLP API → Pinecone
```

## 🚀 主要機能

1. **RAG更新**: BigQuery → GCP DLP API → Pinecone
2. **回答生成**: Webhook → RAG検索 → 回答生成
3. **回答書き込み**: 生成結果 → HubSpot投稿

## 🛠️ 技術スタック

- **Runtime**: Deno + TypeScript
- **Database**: BigQuery
- **Vector DB**: Pinecone
- **PII Protection**: GCP DLP API
- **CRM**: HubSpot API
- **Deploy**(TBD): Deno Deploy / Supabase / Cloud Run

## 📁 プロジェクト構成

```
ai-customer-support/
├── main.ts                 # 統一エントリーポイント
├── deno.json              # Deno設定
├── .env.example           # 環境変数テンプレート
├── src/
│   ├── server.ts          # サーバー実装
│   ├── handlers/          # Webhook handlers
│   ├── services/          # 外部API clients
│   ├── types/             # TypeScript型定義
│   └── utils/             # ユーティリティ
├── bin/                   # デプロイスクリプト
└── docker/                # Docker設定
```

## 🔧 開発環境構築

### 前提条件

- Deno 1.40+
- ngrok（開発用）
- GCP プロジェクト
- Pinecone アカウント
- HubSpot アカウント

### セットアップ

1. **環境変数設定**
   ```bash
   cp .env.example .env
   # 必要な環境変数を設定
   ```

2. **ngrok設定**
   ```bash
   ngrok http 8000
   ```

3. **開発サーバー起動**
   ```bash
   deno run --allow-all main.ts
   ```

4. **テスト実行**
   ```bash
   deno test --allow-all
   ```

## 📊 環境変数

```env
# GCP
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json

# Pinecone
PINECONE_API_KEY=your-pinecone-key
PINECONE_INDEX_NAME=your-index-name

# HubSpot
HUBSPOT_ACCESS_TOKEN=your-hubspot-token

# BigQuery
BIGQUERY_DATASET=your-dataset
BIGQUERY_TABLE=your-table

# Server
PORT=8000
```

## 🚀 デプロイ

### Deno Deploy

```bash
./bin/deploy-deno.sh
```

### Supabase

```bash
./bin/deploy-supabase.sh
```

### Cloud Run

```bash
./bin/deploy-cloudrun.sh
```

## 🧪 テスト戦略

TDD（テスト駆動開発）に準拠：

1. Red: 失敗するテストを書く
2. Green: 最小限のコードで通す
3. Refactor: リファクタリング

```bash
# 全テスト実行
deno test --allow-all

# カバレッジ付き
deno test --allow-all --coverage

# 特定ファイル
deno test --allow-all src/services/dlp.test.ts
```

## 🔒 セキュリティ

- GCP DLP APIによる個人情報自動マスキング
- 環境変数による機密情報管理
- HTTPS通信の強制

## 📈 監視・ログ

- 構造化ログ出力
- エラー追跡
- パフォーマンス監視

## 🤝 開発フロー

1. Issue作成
2. ブランチ作成
3. TDD実装
4. PR作成
5. レビュー
6. マージ

## 📚 参考資料

- [Deno Documentation](https://deno.land/manual)
- [GCP DLP API](https://cloud.google.com/dlp/docs)
- [Pinecone Documentation](https://docs.pinecone.io/)
- [HubSpot API](https://developers.hubspot.com/docs/api/overview)
