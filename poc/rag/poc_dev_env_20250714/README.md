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
  - [x] `gcloud auth application-default login`
  - [x] DLP 有効化
    - [機密データの匿名化](https://cloud.google.com/sensitive-data-protection/docs/deidentify-sensitive-data?hl=ja)
  - [] Big Query API、DLP API確認
    - [x] 権限付与依頼
      - BigQuery クエリジョブの実行権限:
        - roles/bigquery.jobUser
        - roles/bigquery.dataViewer（対象データセットに対して）
      - DLP マスキング用権限:
        - roles/dlp.user
      - 共通権限:
        - roles/serviceusage.serviceUsageConsumer
      - 一時的にオーナー権限をいただいた
- [x] Python環境
  - [x] 仮想環境(uv)
  - [x] ライブラリインストール
  - [x] 各種API クライアント
  - linter formatterは一旦なし(ruffあたりおすすめされてる)
- [x] Claude Code でのコーディング方法を軽く調べる
- [x] APIキーの管理方法
  - 一旦環境変数で。
- [] BigQueryの疎通確認
- [x] DLPの疎通確認
  - `check_dlp_api.py` で確認
- [] Claude Code API の疎通確認
- [x] OpenAI API の疎通確認
  - `check_open_api_embeding.py` で確認
- [] Pinecone API の疎通確認
- [] OpenAI と Pinecone の連携確認
- [] Claude と Pinecone の連携確認

## 直近(2025/07/15〜)やること

- [x] DLPの精度チェック
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
uv add <<package>>
```

実行

```
uv run xxx.py
```

## GCPのAPI利用

[Google Cloud CLI をインストールする](https://cloud.google.com/sdk/docs/install-sdk?utm_source=chatgpt.com&hl=ja)

GCPのAPIを利用するときは、APIが有効化されているか確認。権限があるかを確認。権限がなければロール付与などを依頼。

自身のGoogleアカウントを使って SDK のAPIを利用するには下記のコマンドを使う

```
gcloud auth application-default login
```

[アプリケーションのデフォルト認証情報の仕組み](https://cloud.google.com/docs/authentication/application-default-credentials?utm_source=chatgpt.com&hl=ja)

これによって、認証情報がローカルに保存され、SDK利用時に自動認証される

> Linux / macOS: $HOME/.config/gcloud/application_default_credentials.json
> Windows: %APPDATA%\gcloud\application_default_credentials.json
