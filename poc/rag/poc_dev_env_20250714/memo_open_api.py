"""
OpenAI API による文字列のベクトル化の疎通確認

このスクリプトは、OpenAI Embeddings API を使用して文字列をベクトル化し、
基本的な機能の動作確認を行います。

実行方法:
    uv run memo_open_api.py

必要な環境変数:
    OPENAI_API_KEY: OpenAI API キー
"""

import os
from typing import List, Dict, Any
import openai
import numpy as np
from openai import OpenAI


def setup_openai_client() -> OpenAI:
    """OpenAI クライアントの初期化"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY 環境変数が設定されていません")
    
    client = OpenAI(api_key=api_key)
    return client


def create_embedding(client: OpenAI, text: str, model: str = "text-embedding-3-small") -> List[float]:
    """
    文字列をベクトル化する
    
    Args:
        client: OpenAI クライアント
        text: ベクトル化する文字列
        model: 使用するモデル（デフォルト: text-embedding-3-small）
        
    Returns:
        ベクトル（float のリスト）
    """
    try:
        response = client.embeddings.create(
            model=model,
            input=text
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"エラー: {e}")
        raise


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    2つのベクトル間のコサイン類似度を計算
    
    Args:
        vec1: ベクトル1
        vec2: ベクトル2
        
    Returns:
        コサイン類似度 (-1.0 ~ 1.0)
    """
    np_vec1 = np.array(vec1)
    np_vec2 = np.array(vec2)
    
    dot_product = np.dot(np_vec1, np_vec2)
    norm1 = np.linalg.norm(np_vec1)
    norm2 = np.linalg.norm(np_vec2)
    
    if norm1 == 0 or norm2 == 0:
        return 0.0
    
    return dot_product / (norm1 * norm2)


def test_embedding_functionality():
    """基本的なベクトル化機能のテスト"""
    print("=== OpenAI API ベクトル化疎通確認 ===\n")
    
    try:
        # クライアント初期化
        print("1. OpenAI クライアントの初期化...")
        client = setup_openai_client()
        print("✅ クライアント初期化成功\n")
        
        # テスト用の文字列
        test_texts = [
            "こんにちは、私はAIアシスタントです。",
            "Hello, I am an AI assistant.",
            "商品の返品について教えてください。",
            "製品の返品手続きを知りたいです。",
            "今日の天気はいかがですか？"
        ]
        
        print("2. 文字列のベクトル化...")
        embeddings = []
        for i, text in enumerate(test_texts):
            print(f"  テキスト {i+1}: {text}")
            embedding = create_embedding(client, text)
            embeddings.append(embedding)
            print(f"    ベクトル次元: {len(embedding)}")
            print(f"    ベクトルサンプル: {embedding[:3]}...\n")
        
        print("3. 類似度の計算...")
        # 類似したテキスト同士の類似度をチェック
        similarity_pairs = [
            (0, 1),  # 日本語と英語のあいさつ
            (2, 3),  # 返品に関する類似した質問
            (0, 4),  # 全く異なる内容
        ]
        
        for i, j in similarity_pairs:
            similarity = cosine_similarity(embeddings[i], embeddings[j])
            print(f"  テキスト {i+1} vs テキスト {j+1}: {similarity:.4f}")
            print(f"    「{test_texts[i]}」")
            print(f"    「{test_texts[j]}」\n")
        
        print("4. 利用可能なモデルの確認...")
        models = ["text-embedding-3-small", "text-embedding-3-large", "text-embedding-ada-002"]
        
        sample_text = "サンプルテキスト"
        for model in models:
            try:
                embedding = create_embedding(client, sample_text, model)
                print(f"  ✅ {model}: 次元数 {len(embedding)}")
            except Exception as e:
                print(f"  ❌ {model}: エラー - {e}")
        
        print("\n=== 疎通確認完了 ===")
        print("✅ OpenAI Embeddings API の基本機能が正常に動作しています")
        
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        print("\n確認事項:")
        print("1. OPENAI_API_KEY 環境変数が設定されているか")
        print("2. OpenAI API キーが有効かどうか")
        print("3. インターネット接続が正常かどうか")


def batch_embedding_test():
    """複数テキストの一括ベクトル化テスト"""
    print("\n=== 一括ベクトル化テスト ===")
    
    try:
        client = setup_openai_client()
        
        # 複数テキストを一度に処理
        texts = [
            "メールでのお問い合わせ",
            "電話でのサポート",
            "チャットサポート",
            "商品の不具合報告",
            "配送に関する質問"
        ]
        
        print("一括ベクトル化実行中...")
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=texts
        )
        
        print(f"処理されたテキスト数: {len(response.data)}")
        
        for i, embedding_data in enumerate(response.data):
            print(f"テキスト {i+1}: {texts[i]}")
            print(f"  ベクトル次元: {len(embedding_data.embedding)}")
            print(f"  インデックス: {embedding_data.index}")
        
        print("✅ 一括ベクトル化テスト完了")
        
    except Exception as e:
        print(f"❌ 一括ベクトル化エラー: {e}")


if __name__ == "__main__":
    # 基本的な疎通確認
    test_embedding_functionality()
    
    # 一括処理テスト
    batch_embedding_test()