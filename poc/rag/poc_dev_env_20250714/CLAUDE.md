# CLAUDE.md

このファイルは、Claude Code (claude.ai/code) がこのリポジトリでコードを扱う際のガイダンスを提供します。

## プロジェクト概要

これは、Python と `uv` パッケージマネージャーを使用したAIカスタマーサポート用のRAG（Retrieval-Augmented Generation）システムの概念実証です。このシステムは以下を統合します：

- **BigQuery** - データ取得とDLP APIによるプライバシーマスキング
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

このシステムには以下のAPIキーと認証情報が必要です：
- GCP（BigQuery、DLP API）
- OpenAI API
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