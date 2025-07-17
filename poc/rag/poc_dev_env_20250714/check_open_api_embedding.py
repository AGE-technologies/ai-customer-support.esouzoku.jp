"""
OpenAI API疎通確認とコサイン類似度計算

To Claude: CHECKED

---

得られた知見:
- ベクトル化のモデルはいくつかある。text-embedding-3-small, text-embedding-3-large など。
- 実行コスト等で決める必要がありそう
- largeのほうがベクトルの要素数は多いが、類似度計算では、確かに大きいほうがより類似していることを確認した。
"""

import os
import numpy as np
from openai import OpenAI


def get_embeddings(client: OpenAI, model: str, texts: list[str]):
    """テキストをベクトル化する"""
    response = client.embeddings.create(model=model, input=texts)
    return [np.array(data.embedding) for data in response.data]


def cosine_similarity(vec1, vec2):
    """2つのベクトル間のコサイン類似度を計算"""
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))


def check_open_ai_embedding(client: OpenAI, model: str = "text-embedding-3-small"):
    # 類似した文章
    text1 = "商品の返品について教えてください。"
    text2 = "製品の返品手続きを知りたいです。"

    # 異なる文章
    text3 = "今日の天気はいかがですか？"

    print(f"文章1: {text1}")
    print(f"文章2: {text2}")
    print(f"文章3: {text3}")

    # ベクトル化
    print("\nベクトル化実行...")
    vectors = get_embeddings(client, model, [text1, text2, text3])
    vec1, vec2, vec3 = vectors

    print(f"ベクトル次元: {len(vec1)}")

    # コサイン類似度計算
    print("\nコサイン類似度計算...")
    similarity_1_2 = cosine_similarity(vec1, vec2)
    similarity_1_3 = cosine_similarity(vec1, vec3)

    print(f"類似文章の類似度: {similarity_1_2:.4f}")
    print(f"異なる文章の類似度: {similarity_1_3:.4f}")

    # 検証
    if similarity_1_2 > similarity_1_3:
        print("✅ 類似した文章の類似度が高く、正しく計算されています")
    else:
        print("❌ 類似度計算に問題があります")


def main():
    # OpenAI API接続テスト
    print("OpenAI API接続テスト...")
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    check_open_ai_embedding(client, "text-embedding-3-small")
    check_open_ai_embedding(client, "text-embedding-3-large")


if __name__ == "__main__":
    main()
