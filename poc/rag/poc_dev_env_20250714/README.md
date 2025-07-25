# 検証環境構築

検証環境構築まとめ

## 技術・環境整理

- データ取得と前処理（BigQuery & DLP）(一旦ローカルテキストファイルでいいかも？？ Metabaseからローカルファイルにコピペ保存する形にして、ファイル読み込みでも検証可能)
- ベクトルデータベース（Pinecone）
- ベクトル化(~~OpenAI~~)
  - ベクトル化は Pinecone でも可能。一旦こちらを使う
- RAG実行（Pinecone + Claude）
- 一連のツールを連携・検証する環境（Python）

## TODO

- [x] GCP設定周り
  - [x] gcloud cliインストール
  - [x] gcloud 初期化
  - [x] `gcloud auth application-default login`
  - [x] DLP 有効化
    - [機密データの匿名化](https://cloud.google.com/sensitive-data-protection/docs/deidentify-sensitive-data?hl=ja)
  - [x] GCP権限付与依頼
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
- [] Claude API の疎通確認
- [x] OpenAI API の疎通確認
  - `check_open_api_embeding.py` で確認
  - Pineconeに Embeddingの機能があることが判明もしかしたら使わないかも。
- [x] Pinecone API の疎通確認 (`check_pinecone_api.py`)
  - [x] Pineconeインデックスの設定とクライアント接続確認
  - [x] API経由でレコードを追加する
- [] メールQAペアの匿名化と要約
  - [] BigQueryからQAペアを取ってくる
  - [] それを匿名化
  - [] GPT-4o-miniによる要約
  - [] 要約をBigQueryに保存
    - [] BigQueryへのテーブル追加
    - [] BigQuery API の確認
- [] DLP と Pinecone の連携確認
  - [] サンプルメールデータの準備（10件のcustomerメール）
  - [] メールをベクトル化してPineconeに登録する処理の実装（PineconeのEmbedding機能を使用）
  - [] 新しいメールでの類似検索機能の実装
  - [] 検索結果の妥当性確認（上位結果が実際に似ているかの検証）
  - [] Pineconeメタデータ構造の最適化とQAペア対応への拡張検討
- [] OpenAI と Pinecone の連携確認
  - OpenAIのEmbeddingではなく、PineconeのEmbedding機能を使用する方針に変更
- [] Claude と Pinecone の連携確認

## (2025/07/15〜2025/07/22) やったこと

- [x] DLPの精度チェック
- [x] OpenAIの文字列のベクトル化
- [x] Pineconeにデータ突っ込んでインデックス化してみる

## 直近やること(2025/07/23〜)やること

- DLPとメールQAペアの要約
  - [] メールQAペアの取得
  - [] QAペアに対し、DLPで機密情報を匿名化
    - (多少もれててもしょうがない。のちのLLMがプロンプト次第で省いてくれそう。LLMによる要約に多少個人情報が入るリスクは大きなクリティカルにはならなそう)
  - [] QAペアをLLMによってそれぞれ3~5行程度に要約
    - [x] LLMの選定
      - Claude
      - GPT-4o-mini (圧倒的にコスパ良い。Claude Codeがアドバイスくれた。ありがとう)
    - [] QはそのままLLMに投げる
    - [] Aは、Qと一緒にLLMに投げる
  - [] テーブル項目
    - thread_id (QAの関連付け)
    - query
    - answer
    - sent_at
    - [] 他にないか考える
  - [] 要約までの短いパイプラインづくり
    - [] BigQueryからデータを取ってくる
    - [] 要約
    - [] 一旦ローカルに保存
- QAペア要約のBigQueryへの保存
  - [] TODO調査
- DLPとPineconeの連携
  - [] メールデータ選び
    -  BigQueryから取ってくる
  - [] DLPによる匿名化の構成調整
  - [] Pinecone API によるEmbedding
  - [] Pinecone API メールデータ追加
  - [] Pinecode API による類似度ベース検索

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
