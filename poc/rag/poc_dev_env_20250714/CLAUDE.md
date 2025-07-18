# CLAUDE.md

このファイルは、Claude Code (claude.ai/code) がこのリポジトリでコードを扱う際のガイダンスを提供します。

## プロジェクト概要

これは、Python と `uv` パッケージマネージャーを使用したAIカスタマーサポート用のRAG（Retrieval-Augmented Generation）システムの概念実証です。このシステムは以下を統合します：

- **BigQuery & Data Loss Prevention** - データ取得とDLPによるプライバシーマスキング
- **OpenAI** - テキストのベクトル化（注：PineconeのEmbedding機能を使用する方針に変更）
- **Pinecone** - ベクトルデータベースの保存と検索
- **Claude (Anthropic)** - 回答生成

## 開発環境

### Python環境 (uv)
- `.python-version` でPython 3.13.5を指定
- 依存関係管理に `uv` を使用
- 仮想環境は `uv` によって自動管理

### 依存関係
`pyproject.toml` のコアライブラリ：
- `anthropic>=0.57.1` - Claude APIクライアント
- `openai>=1.95.1` - OpenAI APIクライアント（注：EmbeddingはPineconeの機能を使用する方針に変更）
- `pinecone>=7.3.0` - Pineconeベクトルデータベースクライアント

## よく使うコマンド

### パッケージ管理

```bash
# 新しいパッケージの追加
uv add package-name

# 依存関係のインストール
uv sync

# 実行
uv run xxx.py
```

### Python環境（uv）

```bash
# uv インストール & 初期化
curl -LsSf https://astral.sh/uv/install.sh | sh
uv init

# 特定のPythonバージョンをインストール
uv python install 3.13.5

# Pythonバージョンを固定
uv python pin 3.13.5
```

## アーキテクチャ

これは最小限の構造を持つPOC開発環境です：

- `check_xxx.py` - 各APIの疎通確認や連携確認を行うためのPythonスクリプト
- `pyproject.toml` - プロジェクト設定と依存関係
- `README.md` - 開発セットアップドキュメントとTODOリスト

### 計画されたアーキテクチャ（READMEより）

```
BigQuery → DLP API → Pinecone (ベクトル化・保存・検索) → Claude → レスポンス
```

## 開発ワークフロー

README TODOリストに基づいて、下記項目の達成を目指しています：

### 環境セットアップ
- [x] Python環境（uv）
- [x] 各種API クライアント
- [x] APIキーの管理方法

### GCP関連
- [x] gcloud cliインストール
- [x] gcloud 初期化
- [x] `gcloud auth application-default login`
- [x] DLP 有効化
- [x] 権限付与（BigQuery、DLP API）
- [ ] BigQueryの疎通確認
- [x] DLPの疎通確認 (`check_dlp_api.py`)

### API接続確認
- [x] OpenAI API の疎通確認 (`check_open_api_embeding.py`)
- [x] DLPの疎通確認 (`check_dlp_api.py`)
- [ ] Claude Code API の疎通確認
- [ ] Pinecone API の疎通確認

### 連携確認
- [x] OpenAIの文字列のベクトル化
- [ ] Pineconeにデータ突っ込んでインデックス化
- [ ] OpenAI と Pinecone の連携確認
- [ ] Claude と Pinecone の連携確認

### 精度テスト
- [ ] DLPの精度チェック


--- 

## これより下記の項目はClaudeにより編集されない

## 注意事項

- これは開発初期段階の概念実証です
- READMEには実装進捗の詳細なTODOアイテムが含まれています
- 環境はモダンなPython依存関係管理のためにuvを使用
- 各サービス間のRAGパイプライン統合の検証に焦点を当てています

## API統合要件

このシステムには以下のAPIキーと認証情報が必要：
- GCP（BigQuery、DLP API）
  - 基本的に `gcloud auth application-default login` を行い、認証情報はローカルに保存する。その前提で、SDKを利用する
- OpenAI API
  - 環境変数
- Pinecone API
- Claude API

## コーディング方針 

- 初めて触る外部APIやSDKの疎通確認を行うときは、「最低限」のコードを書く
  - 「最低限」とは、下記のことをいう。
    - 外部APIの要求するパラメータに対して正しい入力ができていて、正常な結果が返却されるかの確認
    - 返却された値を検証するための1~2パターンの処理
    - 実行時にどの処理が行うかがわかる標準出力処理
- 基本的にソースコードの実行はユーザーが行う。Claudeは勝手にソースコードを実行しない

## コーディング規約

- 新規作成・更新されたテキストファイルの最後には、`\n\n`（空の最終行）を入れる
- 外部APIのクライアントクラスがSDKに定義されている場合は基本的にmain関数の中で初期化する
- その外部APIクライアントに依存する関数は、そのクライアントを引数として受け取る(簡易DI)

## 用語定義

- **CHECKファイル** : 疎通・連携確認のためのプログラムファイル。`check_` という接頭辞のあるファイルはこれ。
- **CHECKED** : CHECKファイルの内容について、疎通・連携が確認された状態

## TODOリスト

下記にTODOリストが存在する

- CLAUDE.md
- README.md

## コーディングとTODOリストの連携

- CHECKファイルのドキュメントコメントとして `For Claude: CHECKED`　があればTODOリストの該当の項目にチェックを入れる
- また `得られた知見` の内容はTODOリストに記載する必要はありません。代わりに、CHECKファイルの名前を項目につける
- これらの項目の状態の更新は、「`Check TODO`」という指示で行われる。

## ユーザー(K)の性格

- このプロジェクトのメンバーには、ユーザー K が存在します。
- Kが「気が重い」と感じるタスクは下記のようなタスクです
  - 数あるリソースから欲しい情報を調べ、取ってくること
  - 各種ツールの設定
  - Claudeが余計なことをしないようにする指示の構成を考えること
