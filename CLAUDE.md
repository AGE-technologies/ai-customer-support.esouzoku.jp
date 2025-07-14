# Claude Code Development Guide

このプロジェクトは TypeScript + Deno で構築されたAIカスタマーサポートシステムです。

## 🎯 プロジェクト概要

- **目的**: BigQueryのメール対応履歴を学習し、HubSpotで高品質な回答を自動生成
- **技術**: Deno + TypeScript (型安全 + TDD)
- **検証重視**: 小さく始めて効果を確認しながら拡張

## 🏗️ システム構成

```
Webhook → RAG検索 → 回答生成 → HubSpot書き込み
    ↑         ↑
BigQuery → DLP API → Pinecone
```

## 📁 プロジェクト構造

```
ai-customer-support/
├── main.ts                 # 統一エントリーポイント
├── deno.json              # Deno設定
├── .env.example           # 環境変数テンプレート
├── src/
│   ├── server.ts          # サーバー実装
│   ├── server.test.ts     # サーバーテスト
│   ├── handlers/          # Webhook handlers
│   │   ├── webhook.ts
│   │   └── webhook.test.ts
│   ├── services/          # 外部API clients
│   │   ├── bigquery.ts
│   │   ├── bigquery.test.ts
│   │   ├── dlp.ts
│   │   ├── dlp.test.ts
│   │   ├── pinecone.ts
│   │   ├── pinecone.test.ts
│   │   ├── hubspot.ts
│   │   ├── hubspot.test.ts
│   │   └── rag.ts
│   ├── types/             # TypeScript型定義
│   │   └── index.ts
│   └── utils/             # ユーティリティ
│       └── config.ts
├── bin/                   # デプロイスクリプト
│   ├── deploy-deno.sh     # Deno Deploy用
│   ├── deploy-supabase.sh # Supabase用
│   └── deploy-cloudrun.sh # Cloud Run用
└── docker/                # Docker設定
    └── Dockerfile
```

## 🔧 開発環境

### 必要なツール
- Deno 1.40+
- ngrok（開発用）
- GCP プロジェクト
- Pinecone アカウント
- HubSpot アカウント

### 開発コマンド

```bash
# 開発サーバー起動
deno run --allow-all main.ts

# テスト実行
deno test --allow-all

# テスト（カバレッジ付き）
deno test --allow-all --coverage

# 型チェック
deno check main.ts

# フォーマット
deno fmt

# リント
deno lint
```

## 🧪 テスト戦略

TDD（テスト駆動開発）に準拠：
1. **Red**: 失敗するテストを書く
2. **Green**: 最小限のコードで通す
3. **Refactor**: リファクタリング

### テストファイル配置
- `src/services/dlp.ts` → `src/services/dlp.test.ts`
- ソースコードと同じディレクトリに配置

### テスト実行
```bash
# 全テスト
deno test --allow-all

# 特定ファイル
deno test --allow-all src/services/dlp.test.ts
```

## 🚀 デプロイ

### デプロイ先選択肢
- **Deno Deploy**: 最もシンプル
- **Supabase**: Edge Functions
- **Cloud Run**: Docker経由

### デプロイスクリプト
```bash
./bin/deploy-deno.sh      # Deno Deploy
./bin/deploy-supabase.sh  # Supabase
./bin/deploy-cloudrun.sh  # Cloud Run
```

## 🔒 セキュリティ

- GCP DLP APIによる個人情報自動マスキング
- 環境変数による機密情報管理
- HTTPS通信の強制

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

## 🔄 開発フロー

1. Issue作成
2. ブランチ作成
3. TDD実装
4. PR作成
5. レビュー
6. マージ

## 📝 コーディング規約

- TypeScript strict mode
- Deno標準のフォーマット
- 関数型プログラミング推奨
- 型安全を最優先

## 🤖 AI補助

- 個人情報マスキング: GCP DLP API
- 回答生成: RAG + LLM
- 検証重視: 小さく始めて効果測定

## 🚨 トラブルシューティング

### よくある問題
1. **権限エラー**: `--allow-all`フラグの確認
2. **型エラー**: `deno check`でチェック
3. **環境変数**: `.env`ファイルの設定確認

### デバッグ
```bash
# 詳細ログ
deno run --allow-all --log-level debug main.ts

# 型チェック
deno check --all main.ts
```

## 📚 参考資料

- [Deno Documentation](https://deno.land/manual)
- [GCP DLP API](https://cloud.google.com/dlp/docs)
- [Pinecone Documentation](https://docs.pinecone.io/)
- [HubSpot API](https://developers.hubspot.com/docs/api/overview)

## 📈 次のステップ

1. 基本的なWebhook受信機能
2. BigQuery連携とDLP処理
3. Pinecone連携とRAG実装
4. HubSpot連携と回答投稿
5. 監視・ログ機能
6. 本番デプロイ