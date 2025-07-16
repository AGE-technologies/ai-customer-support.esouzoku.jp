# 検証環境構築

検証環境構築まとめ

## 技術・環境整理

- データ取得と前処理（BigQuery & DLP）(一旦ローカルテキストファイルでいいかも？？ Metabaseからローカルファイルにコピペ保存する形にして、ファイル読み込みでも検証可能)
- ベクトルデータベース（Pinecone）
- ベクトル化(OpenAI)
- RAG実行（Pinecone + Claude）
- 一連のツールを連携・検証する環境（Python）

## TODO

- [] GCP周り
  - [x] gcloud cliインストール
  - [x] gcloud 初期化
  - [] Big Query API、DLP API確認
    - [] 権限付与依頼
      - BigQuery クエリジョブの実行権限:
        - roles/bigquery.jobUser
        - roles/bigquery.dataViewer（対象データセットに対して）
      - DLP マスキング用権限:
        - roles/dlp.user
      - 共通権限:
        - roles/serviceusage.serviceUsageConsumer
- [x] Python環境
  - [x] 仮想環境(uv)
  - [x] ライブラリインストール
  - [x] 各種API クライアント
  - linter formatterは一旦なし(ruffあたりおすすめされてる)
- [x] Claude Code でのコーディング方法を軽く調べる
- [x] APIキーの管理方法
  - 一旦環境変数で。
- [] BigQueryの疎通確認
- [] DLPの疎通確認
- [] Claude Code API の疎通確認
- [x] OpenAI API の疎通確認
  - `check_open_api_embeding.py` で確認
- [] Pinecone API の疎通確認
- [] OpenAI と Pinecone の連携確認
- [] Claude と Pinecone の連携確認

## 直近(2025/07/15〜)やること

- [] DLPの精度チェック
- [x] OpenAIの文字列のベクトル化
- [] Pineconeにデータ突っ込んでインデックス化してみる

## Python環境構築(uv)

uv インストール & 初期化(カレントディレクトリを仮想環境に)

```
curl -LsSf https://astral.sh/uv/install.sh | sh
uv init
```

バージョン指定

```
uv python install 3.13.5
uv python pin 3.13.5
```

パッケージ追加

```
uv add -r requirements.txt
uv sync
```

実行

```
uv run xxx.py
```
