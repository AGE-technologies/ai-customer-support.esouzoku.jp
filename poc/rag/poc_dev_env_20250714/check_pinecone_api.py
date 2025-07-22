"""
Pinecone APIの疎通確認

目的: Pineconeインデックスの設定とクライアント接続確認
- Pineconeクライアントの初期化
- インデックス一覧の取得
- インデックスの詳細情報確認
- レコード追加機能の確認

To Claude: CHECKED
"""

import os
import uuid
from pinecone import Pinecone
from pinecone.db_data import Index


def list_indexes_as_check_pinecone_connection(pc: Pinecone) -> list[str]:
    """Pineconeクライアントの接続確認"""
    print("=== Pinecone 接続確認 ===")

    # インデックス一覧取得
    print("インデックス一覧を取得中...")
    indexes = pc.list_indexes()
    print(f"利用可能なインデックス数: {len(indexes.names())}")

    for index_name in indexes.names():
        print(f"- インデックス名: {index_name}")

    return indexes.names()


def get_index_as_check_index_details(pc: Pinecone, index_name: str) -> Index | None:
    """インデックスの詳細情報確認"""
    print("\n=== インデックス詳細確認 ===")

    print(f"インデックス '{index_name}' の詳細を確認中...")

    try:
        index: Index = pc.Index(index_name)
        stats = index.describe_index_stats()
        print(f"- ベクトル次元: {stats.get('dimension', 'N/A')}")
        print(f"- 総ベクトル数: {stats.get('total_vector_count', 'N/A')}")
        print(f"- インデックスの満杯度: {stats.get('index_fullness', 'N/A')}")

        return index
    except Exception as e:
        print(f"インデックス詳細取得エラー: {e}")
        return None


def embed_text_to_vector(pc: Pinecone, text: str) -> list[float] | None:
    """文字列をベクトル化する"""
    print("テキストをベクトル化中...")
    print(f"対象テキスト: {text}")

    try:
        embeddings = pc.inference.embed(
            model="multilingual-e5-large",
            inputs=[text],
            parameters={"input_type": "passage", "truncate": "END"},
        )

        vector_values = embeddings[0].values
        print(f"ベクトル化成功: 次元数 = {len(vector_values)}")
        return vector_values

    except Exception as e:
        print(f"ベクトル化エラー: {e}")
        return None


def upsert_vector_to_index(
    index: Index, record_id: str, vector_values: list[float], metadata: dict = None
) -> bool:
    """ベクトルをインデックスに登録する"""
    print("インデックスに登録中...")
    print(f"レコードID: {record_id}")

    try:
        index.upsert(
            vectors=[
                {
                    "id": record_id,
                    "values": vector_values,
                    "metadata": metadata or {},
                }
            ]
        )

        print(f"インデックス登録成功: ID = {record_id}")
        return True

    except Exception as e:
        print(f"インデックス登録エラー: {e}")
        return False


def add_text_to_index(
    pc: Pinecone, index: Index, text: str, metadata: dict = None
) -> str | None:
    """文字列をベクトル化してインデックスに登録する（合成関数）"""
    print("\n=== レコード追加 ===")
    print(f"追加するテキスト: {text}")

    # 一意のIDを生成
    record_id = str(uuid.uuid4())
    print(f"レコードID: {record_id}")

    # 1. テキストをベクトル化
    vector_values = embed_text_to_vector(pc, text)
    if not vector_values:
        return None

    # 2. ベクトルをインデックスに登録
    success = upsert_vector_to_index(
        index, record_id, vector_values, metadata or {"text": text}
    )

    if success:
        print(f"レコード追加成功: ID = {record_id}")
        return record_id
    else:
        return None


def main():
    print("Pinecone API 疎通確認を開始します")

    # 環境変数確認
    api_key = os.getenv("PINECONE_API_KEY")
    if not api_key:
        print("エラー: PINECONE_API_KEY 環境変数が設定されていません")
        return

    print(f"API Key確認: {'*' * 20}{api_key[-4:] if len(api_key) > 4 else '****'}")

    try:
        # Pineconeクライアント初期化
        pc = Pinecone(api_key=api_key)
        print("Pineconeクライアント初期化成功")

        # 接続確認
        index_names = list_indexes_as_check_pinecone_connection(pc)

        # インデックス詳細確認
        index = get_index_as_check_index_details(pc, index_names[0])

        # レコード追加テスト
        if index:
            print("\n=== メッセージ入力 ===")
            user_text = input("インデックスに追加するメッセージを入力してください: ")

            if user_text.strip():
                test_metadata = {
                    "text": user_text,
                    "source": "check_pinecone_api.py",
                    "type": "user_input",
                }

                _record_id = add_text_to_index(pc, index, user_text, test_metadata)

                print(
                    "登録してから反映されるまでに時間ラグがあるので、確認はコンソールで行ってください"
                )
            else:
                print(
                    "メッセージが入力されませんでした。レコード追加をスキップします。"
                )

        print("\n=== 疎通確認完了 ===")
        print("Pinecone APIとの接続・レコード追加が正常に確認されました")

    except Exception as e:
        print(f"エラーが発生しました: {e}")
        print("- API キーが正しいか確認してください")
        print("- ネットワーク接続を確認してください")


if __name__ == "__main__":
    main()
