# RAG検証システム

## 🎯 目的
BigQueryのメール対応履歴を使用してRAGシステムの効果を検証する。
RAGありなしで回答方針の精度がどれくらい向上するかを測定する。

## 🔬 検証計画

### 検証範囲
- **データ件数**: 3件のサンプルデータ
- **比較対象**: RAGあり vs RAGなし
- **評価指標**: 回答の精度・関連性

### 検証フロー
```
BigQuery → DLP API → Pinecone → RAG検索 → 回答生成
    ↓         ↓         ↓         ↓
 履歴取得   個人情報    ベクトル   類似検索
         マスキング   インデックス
```

## 🛠️ 技術スタック

- **言語**: TypeScript + Deno
- **データ取得**: BigQuery
- **個人情報保護**: Google DLP API
- **ベクトル検索**: Pinecone
- **テスト**: Deno標準テスト

## 📁 ファイル構成

```
poc/rag/
├── README.md              # このファイル
├── sample_index.jsonl     # サンプルデータ
├── bigquery_client.ts     # BigQuery連携
├── dlp_client.ts          # DLP API連携
├── pinecone_client.ts     # Pinecone連携
├── rag_search.ts          # RAG検索機能
├── comparison_test.ts     # 比較テスト
└── types.ts               # 型定義
```

## 🚀 実行方法

### 1. 環境設定
```bash
# 環境変数を設定
export GOOGLE_CLOUD_PROJECT="your-project-id"
export GOOGLE_APPLICATION_CREDENTIALS="path/to/service-account.json"
export PINECONE_API_KEY="your-pinecone-key"
export PINECONE_INDEX_NAME="rag-test-index"
export BIGQUERY_DATASET="your-dataset"
export BIGQUERY_TABLE="your-table"
```

### 2. データ構造確認・分析（事前調査）
```bash
# BigQueryテーブルの構造を確認
bq show --schema $GOOGLE_CLOUD_PROJECT:$BIGQUERY_DATASET.$BIGQUERY_TABLE

# データサンプルを確認
bq query --use_legacy_sql=false \
  "SELECT * FROM \`$GOOGLE_CLOUD_PROJECT.$BIGQUERY_DATASET.$BIGQUERY_TABLE\` LIMIT 10"

# データ件数を確認
bq query --use_legacy_sql=false \
  "SELECT COUNT(*) as total_records FROM \`$GOOGLE_CLOUD_PROJECT.$BIGQUERY_DATASET.$BIGQUERY_TABLE\`"

# カテゴリ別の分布を確認
bq query --use_legacy_sql=false \
  "SELECT category, COUNT(*) as count FROM \`$GOOGLE_CLOUD_PROJECT.$BIGQUERY_DATASET.$BIGQUERY_TABLE\` GROUP BY category ORDER BY count DESC"

# 日付別の分布を確認
bq query --use_legacy_sql=false \
  "SELECT DATE(timestamp) as date, COUNT(*) as count FROM \`$GOOGLE_CLOUD_PROJECT.$BIGQUERY_DATASET.$BIGQUERY_TABLE\` GROUP BY date ORDER BY date DESC LIMIT 30"
```

### 3. データ準備
```bash
# BigQueryからサンプルデータを取得
deno run --allow-all bigquery_client.ts

# DLP APIで個人情報をマスキング
deno run --allow-all dlp_client.ts

# Pineconeにインデックスを作成
deno run --allow-all pinecone_client.ts
```

### 3. 検証実行
```bash
# RAG検証テストを実行
deno test --allow-all comparison_test.ts
```

## 📊 データ構造

### BigQueryデータ
```json
{
  "ticket_id": "TK-001",
  "customer_query": "商品の返品について",
  "response": "返品は購入から30日以内であれば...",
  "category": "返品・交換",
  "timestamp": "2024-01-15T10:00:00Z"
}
```

### DLP処理後データ
```json
{
  "ticket_id": "TK-001",
  "customer_query": "商品の返品について",
  "response": "返品は購入から30日以内であれば...",
  "category": "返品・交換",
  "timestamp": "2024-01-15T10:00:00Z",
  "masked_pii": true
}
```

### Pineconeインデックス
```json
{
  "id": "TK-001",
  "values": [0.1, 0.2, ...],
  "metadata": {
    "category": "返品・交換",
    "response": "返品は購入から30日以内であれば..."
  }
}
```

## 🧪 テスト戦略

### 比較テスト
1. **RAGなし**: 基本的なLLMによる回答生成
2. **RAGあり**: 関連する過去事例を参照した回答生成

### 評価基準
- **精度**: 回答の正確性
- **関連性**: 質問との関連度
- **一貫性**: 過去の対応との整合性

## 🔒 セキュリティ

- Google DLP APIによる個人情報の自動マスキング
- 環境変数による機密情報管理
- 最小権限の原則に基づくアクセス制御

## 📈 成功指標

- RAGありの回答精度がRAGなしより20%以上向上
- 関連する過去事例の検索精度が80%以上
- 処理時間が3秒以内

## 🔄 次のステップ

1. 基本機能実装
2. 3件のサンプルデータでテスト
3. 結果分析と改善点の特定
4. 本格運用への拡張計画策定

## 📚 参考資料

- [BigQuery Client Library](https://cloud.google.com/bigquery/docs/reference/libraries)
- [Google DLP API](https://cloud.google.com/dlp/docs/reference/rest)
- [Pinecone Documentation](https://docs.pinecone.io/)
- [Deno Testing](https://deno.land/manual/testing)