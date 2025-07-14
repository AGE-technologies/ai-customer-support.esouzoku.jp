# RAG検証システム

## 🎯 目的
BigQueryのメール対応履歴を使用してRAGシステムの効果を検証する。

特に、

- DLP APIの精度
- RAGありなしで回答方針の精度がどれくらい向上するか
を測定する。

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

## 🧪 テスト戦略

### 評価基準

- 誤って個人情報がインデックスされないか
- RAGの有無での精度の違い

## 📚 参考資料

- [BigQuery Client Library](https://cloud.google.com/bigquery/docs/reference/libraries)
- [Google DLP API](https://cloud.google.com/dlp/docs/reference/rest)
- [Pinecone Documentation](https://docs.pinecone.io/)
- [Deno Testing](https://deno.land/manual/testing)