"""
DLPで個人情報を匿名化したデータをPineconeインデックスに追加する確認用コード

このファイルは下記の機能の連携確認を行います：
1. DLP APIによる個人情報の匿名化
2. 匿名化されたデータのPineconeインデックスへの追加

前提条件:
- GCP DLP APIが利用可能（check_dlp_api.py参照）
- Pinecone APIが利用可能（check_pinecone_api.py参照）
- 必要な環境変数が設定済み

To Claude: 作成中

---

得られた知見:
- infoTypeいろいろカスタマイズできる。メールちゃんといろいろ見て、どんな機密情報があるか確認しないといけなさそう
  - https://cloud.google.com/sensitive-data-protection/docs/infotypes-reference?utm_source=chatgpt.com&hl=ja
  - ゆうちょの記号番号、口座番号など
  - 一般的な銀行の口座番号は未検証
- 日本語や中国語、韓国語などは、emailの検知が難しいので、カスタムinfoTypeを採用する方向性
  - https://techdocs.broadcom.com/us/en/symantec-security-software/information-security/data-loss-prevention/16-0-1/about-data-loss-prevention-policies-v27576413-d327e9/detecting-non-english-language-content-v27895102-d327e126361/enable-token-validation-to-match-chinese-japanese-v87221850-d327e129608.html?utm_source=chatgpt.com
"""

import os
import json
from typing import List
from google.cloud import dlp_v2

# カスタムinfoType定義
CUSTOM_INFO_TYPES = [
    {
        "info_type": {"name": "EMAIL_ADDRESS_JP"},
        "regex": {"pattern": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"},
    },
    {
        "info_type": {"name": "JAPAN_POST_BANK_SYMBOL"},
        "regex": {"pattern": r"\b\d{5}\b"},
    },
]

INSPECT_CONFIG = {
    "info_types": [
        {"name": "PHONE_NUMBER"},
        {"name": "PERSON_NAME"},
        {"name": "STREET_ADDRESS"},
        {"name": "LOCATION"},
        {"name": "JAPAN_BANK_ACCOUNT"},
    ],
    "custom_info_types": CUSTOM_INFO_TYPES,
    "min_likelihood": dlp_v2.Likelihood.POSSIBLE,
    "include_quote": True,
}


DEIDENTIFICATION_CONFIG = {
    "info_type_transformations": {
        "transformations": [
            {
                "info_types": [
                    {"name": "PHONE_NUMBER"},
                    {"name": "EMAIL_ADDRESS_JP"},
                    {"name": "PERSON_NAME"},
                    {"name": "LOCATION"},
                    {"name": "STREET_ADDRESS"},
                    {"name": "JAPAN_POST_BANK_SYMBOL"},
                ],
                "primitive_transformation": {
                    "character_mask_config": {
                        "masking_character": "*",
                        "number_to_mask": 0,
                    }
                },
            }
        ]
    }
}

TEST_DATA_PATH = "./data_check_dlp_pinecone/test_data.json"


def anonymize_text_with_dlp(
    dlp_client: dlp_v2.DlpServiceClient, parent: str, text: str
) -> str:
    """
    DLP APIを使用してテキスト内の個人情報を匿名化する

    Args:
        dlp_client: DLP APIクライアント
        parent: GCPプロジェクトパス（例: "projects/your-project-id"）
        text: 匿名化対象のテキスト

    Returns:
        str: 匿名化されたテキスト

    Raises:
        Exception: DLP API呼び出しでエラーが発生した場合
    """
    try:
        # 匿名化リクエスト
        deidentify_request = {
            "parent": parent,
            "deidentify_config": DEIDENTIFICATION_CONFIG,
            "inspect_config": INSPECT_CONFIG,
            "item": {"value": text},
        }

        # 匿名化実行
        response = dlp_client.deidentify_content(request=deidentify_request)
        return response.item.value

    except Exception as e:
        raise Exception(f"DLP匿名化処理でエラーが発生しました: {e}")


def anonymize_texts_batch(
    dlp_client: dlp_v2.DlpServiceClient,
    parent: str,
    texts: List[str],
    split_delimiter: str = "<<<SPLIT_LINE>>>",
    max_texts: int = 10,
) -> List[str]:
    """
    複数のテキストを連結して一括匿名化する

    Args:
        dlp_client: DLP APIクライアント
        parent: GCPプロジェクトパス
        texts: 匿名化対象のテキストリスト
        split_delimiter: テキスト分割用の区切り文字
        max_texts: 処理可能な最大テキスト数

    Returns:
        List[str]: 匿名化されたテキストリスト

    Raises:
        Exception: 匿名化処理でエラーが発生した場合、またはテキスト数が上限を超えた場合
    """
    if not texts:
        return []

    # テキスト数制限チェック
    if len(texts) > max_texts:
        raise Exception(f"テキスト数が上限を超えています: {len(texts)} > {max_texts}")

    # 空でないテキストのみ処理
    valid_texts = [text for text in texts if text.strip()]

    if not valid_texts:
        print("⚠️ 処理対象のテキストがありません")
        return []

    # テキストを区切り文字で連結
    combined_text = split_delimiter.join(valid_texts)

    print(f"📦 {len(valid_texts)}個のテキストを連結して一括匿名化実行...")
    print(f"   連結後テキスト長: {len(combined_text)}文字")

    try:
        # 一括匿名化実行
        anonymized_combined_text = anonymize_text_with_dlp(
            dlp_client, parent, combined_text
        )

        # 匿名化結果を分割
        anonymized_texts = anonymized_combined_text.split(split_delimiter)

        # 分割数の整合性確認
        if len(anonymized_texts) != len(valid_texts):
            raise Exception(
                f"分割数不一致: 期待値{len(valid_texts)}, 実際{len(anonymized_texts)}"
            )

        print(f"✅ 一括匿名化完了: {len(anonymized_texts)}テキスト処理")
        return anonymized_texts

    except Exception as e:
        raise Exception(f"一括匿名化処理でエラーが発生しました: {e}")


def load_texts_from_json(json_file_path: str) -> List[str]:
    """
    JSONファイルから実データのテキストリストを読み込む

    Args:
        json_file_path: JSONファイルのパス

    Returns:
        List[str]: テキストのリスト

    Raises:
        Exception: ファイル読み込みまたはJSONパースでエラーが発生した場合
    """
    try:
        with open(json_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

            return [item["text"] for item in data]

    except FileNotFoundError:
        raise Exception(f"ファイルが見つかりません: {json_file_path}")
    except json.JSONDecodeError as e:
        raise Exception(f"JSON解析エラー: {e}")
    except Exception as e:
        raise Exception(f"ファイル読み込みエラー: {e}")


def main():
    """メイン処理"""
    print("=== DLP匿名化機能確認 ===")

    # プロジェクトID取得
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        print("❌ GOOGLE_CLOUD_PROJECT環境変数が設定されていません")
        return

    print(f"プロジェクトID: {project_id}")
    parent = f"projects/{project_id}"

    # DLPクライアント初期化
    try:
        dlp_client = dlp_v2.DlpServiceClient()
        print("✅ DLPクライアント初期化成功")
    except Exception as e:
        print(f"❌ DLPクライアント初期化失敗: {e}")
        return

    # 単一テキストの匿名化テスト
    print("\n--- 単一テキスト匿名化テスト ---")
    sample_text = "田中一郎さんの電話番号は090-1111-2222です。"
    try:
        anonymized_text = anonymize_text_with_dlp(dlp_client, parent, sample_text)
        print(f"元テキスト: {sample_text}")
        print(f"匿名化後: {anonymized_text}")
        print("✅ 単一テキスト匿名化成功")
    except Exception as e:
        print(f"❌ 単一テキスト匿名化失敗: {e}")
        return

    # 実データを使った匿名化テスト
    print("\n--- 実データ匿名化テスト ---")

    try:
        # JSONファイルからテキスト読み込み
        real_texts = load_texts_from_json(TEST_DATA_PATH)
        print(f"実データ読み込み: {len(real_texts)}件のテキスト")

        # 10件制限のため、最初の10件のみ処理
        if len(real_texts) > 10:
            print("⚠️ 10件制限のため、最初の10件のみ処理します")
            real_texts = real_texts[:10]

        # 実データの匿名化実行
        anonymized_real_texts = anonymize_texts_batch(dlp_client, parent, real_texts)
        print(f"✅ 実データ匿名化完了: {len(anonymized_real_texts)}件処理")

        # 結果サンプル表示
        for i in range(len(anonymized_real_texts)):
            print(f"\n--- 実データサンプル[{i}] ---")
            print(f"元テキスト: {real_texts[i][:256]}...")
            print(f"匿名化後: {anonymized_real_texts[i][:256]}...")

    except Exception as e:
        print(f"❌ 実データ匿名化失敗: {e}")

    print("\n🎉 DLP匿名化機能確認完了！")


if __name__ == "__main__":
    main()
