# 検証環境構築

検証環境構築まとめ

## 技術・環境整理

- データ取得と前処理（BigQuery & DLP）(一旦ローカルテキストファイルでいいかも？？ Metabaseからローカルファイルにコピペ保存する形にして、ファイル読み込みでも検証可能)
- ベクトルデータベース（Pinecone）
- ベクトル化(OpenAI)
- RAG実行（Pinecone + Claude）
- 一連のツールを連携・検証する環境（Python）

## TODO

- ~~[] GCP周り~~
  - [x] gcloud cliインストール
  - [] gcloud 初期化
  - [] Big Query API、DLP API 有効化
  - [] 認証情報の確認
- [x] Python環境
  - [x] 仮想環境(uv)
  - [x] ライブラリインストール
  - [x] 各種API クライアント
  - linter formatterは一旦なし(ruffあたりおすすめされてる)
- [] Claude Code でのコーディング方法調べる
- [] APIキーの管理
- [] ~~BigQuery・DLP API の疎通確認~~
- [] Claude Code API の疎通確認
- [] OpenAI API の疎通確認
- [] Pinecone API の疎通確認
- [] ~~BigQuery と~~ OpenAI と Pinecone の連携確認
- [] Claude と Pinecone の連携確認

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