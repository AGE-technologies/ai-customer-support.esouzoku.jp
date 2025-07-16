# CLAUDE.md

このファイルは、Claude Code (claude.ai/code) がこのリポジトリでコードを扱う際のガイダンスを提供します。

## プロジェクト概要

これは、Python と `uv` パッケージマネージャーを使用したAIカスタマーサポート用のRAG（Retrieval-Augmented Generation）システムの概念実証です。このシステムは以下を統合します：

- **BigQuery & Data Loss Prevention** - データ取得とDLPによるプライバシーマスキング
- **OpenAI** - テキストのベクトル化
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
- `openai>=1.95.1` - OpenAI APIクライアント
- `pinecone>=7.3.0` - Pineconeベクトルデータベースクライアント

## よく使うコマンド

### アプリケーションの実行
```bash
uv run main.py
```

### パッケージ管理
```bash
# 依存関係のインストール
uv sync

# 新しいパッケージの追加
uv add package-name

# requirements.txtから追加
uv add -r requirements.txt
```

### Python環境
```bash
# 特定のPythonバージョンをインストール
uv python install 3.13.5

# Pythonバージョンを固定
uv python pin 3.13.5
```

## アーキテクチャ

これは最小限の構造を持つPOC開発環境です：

- `main.py` - 基本的なhello world機能を持つエントリーポイント
- `pyproject.toml` - プロジェクト設定と依存関係
- `requirements.txt` - 代替の依存関係指定
- `README.md` - 開発セットアップドキュメントとTODOリスト

### 計画されたアーキテクチャ（READMEより）
```
BigQuery → DLP API → OpenAI (ベクトル化) → Pinecone → Claude → レスポンス
```

## 開発ワークフロー

README TODOリストに基づいて、開発は以下の順序で進行しています：
1. ✅ 環境セットアップ（Python + uv）
2. ⏳ API接続確認（BigQuery、DLP、OpenAI、Pinecone、Claude）
3. ⏳ DLP精度テスト
4. ⏳ OpenAIテキストベクトル化
5. ⏳ Pineconeインデックス化とデータ統合
6. ⏳ Claude + Pinecone統合によるRAG

## API統合要件

このシステムには以下のAPIキーと認証情報が必要：
- GCP（BigQuery、DLP API）
  - 基本的に `gcloud auth application-default login` を行うので、認証情報はローカルに保存されている。その前提で、SDKを利用する
- OpenAI API
  - 環境変数
- Pinecone API
- Claude API

## ファイル構造

現在は必要最小限のファイルのみ：
- アプリケーション全体を含む単一の `main.py`
- 標準的なPythonプロジェクトファイル（`pyproject.toml`、`requirements.txt`）
- ドキュメント（`README.md`）

## 注意事項

- これは開発初期段階の概念実証です
- READMEには実装進捗の詳細なTODOアイテムが含まれています
- 環境はモダンなPython依存関係管理のためにuvを使用
- 各サービス間のRAGパイプライン統合の検証に焦点を当てています

## コーディング方針 

- 初めて触る外部APIやSDKの疎通確認を行うときは、「最低限」のコードを書く。
  - 「最低限」とは、下記のことをいう。
    - 外部APIの要求するパラメータに対して正しい入力ができていて、正常な結果が返却されるかの確認
    - 返却された値を検証するための1~2パターンの処理
    - 実行時にどの処理が行うかがわかる標準出力処理
- 基本的にソースコードの実行はユーザーが行う。勝手に実行しない。

## コーディング規約

- 新規作成・更新されたテキストファイルの最終行には改行が入る
- 外部APIのクライアントクラスがSDKに定義されている場合は基本的にmain関数の中で初期化する
- その外部APIクライアントに依存する関数を呼ぶ場合、各処理関数はそのクライアントを引数として受け取る(簡易DI)
