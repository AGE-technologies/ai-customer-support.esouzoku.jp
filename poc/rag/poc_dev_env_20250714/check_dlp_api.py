"""
GCP DLP API疎通確認用コード

ローカルで利用する際は、下記の環境が用意されていることが前提です

1. gcloug cli がインストールされている
2. gcloud auth application-default login を実行して認証し、ローカルに認証情報が保存されている
  - https://cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=ja
3. DLP APIを実行するための権限が付与されている。ロールは下記です。
  - DLP Administrator (roles/dlp.admin) - DLP APIの全機能を使用
  - DLP User (roles/dlp.user) - DLP APIの検査・匿名化機能を使用
  - DLP Inspect Templates Reader (roles/dlp.inspectTemplatesReader) - テンプレートの読み取り専用
  - 主に以下の権限が必要です：
    - dlp.deidentifyTemplates.list（匿名化テンプレート一覧取得）
    - dlp.content.inspect（テキスト検査）
    - dlp.content.deidentify（テキスト匿名化）
4. 下記の環境変数が必要です
  - GOOGLE_CLOUD_PROJECT : プロジェクト名(str)

To Claude: CHECKED

---

得られた知見:
- 匿名化サービスと並んで、「検査サービス」という概念がある。（BigQuery内のデータを検査して結果をレポート、リスク分析用途など）
  - https://cloud.google.com/sensitive-data-protection/docs/sensitive-data-protection-overview?hl=ja
- 匿名化のために、検査サービスの設定を利用する
- 「匿名化テンプレート」という構成のテンプレートを設定可能で、カスタマイズ可能
  - https://cloud.google.com/sensitive-data-protection/docs/creating-templates-deid?hl=ja
- emailの匿名化が苦手かもしれない
  - 結果「匿名化後テキスト: ******の電話番号は*************です。メールアドレスはtaro.yamada@example.comです。」
  - メールアドレスの前後にスペースを入れたらうまくマスキングされました。
"""

import os
from google.cloud import dlp_v2

INSPECT_CONFIG = {
    "info_types": [
        {"name": "PHONE_NUMBER"},
        {"name": "EMAIL_ADDRESS"},
        {"name": "PERSON_NAME"},
    ],
    "min_likelihood": dlp_v2.Likelihood.POSSIBLE,
    "include_quote": True,
}

DEIDENTIFICATION_CONFIG = {
    "info_type_transformations": {
        "transformations": [
            {
                "info_types": [
                    {"name": "PHONE_NUMBER"},
                    {"name": "EMAIL_ADDRESS"},
                    {"name": "PERSON_NAME"},
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


def dlp_inspect(
    dlp_client: dlp_v2.DlpServiceClient, parent: str, text
) -> dlp_v2.InspectContentResponse:
    # 検査設定

    # 検査リクエスト
    request = {
        "parent": parent,
        "inspect_config": INSPECT_CONFIG,
        "item": {"value": text},
    }

    # 検査実行
    return dlp_client.inspect_content(request=request)


def dlp_deidentification(
    dlp_client: dlp_v2.DlpServiceClient, parent: str, text: str
) -> dlp_v2.DeidentifyContentResponse:
    # 匿名化設定（マスキング）

    # 匿名化リクエスト
    deidentify_request = {
        "parent": parent,
        "deidentify_config": DEIDENTIFICATION_CONFIG,
        "inspect_config": INSPECT_CONFIG,
        "item": {"value": text},
    }

    # 匿名化実行
    return dlp_client.deidentify_content(request=deidentify_request)


def check_dlp_deidentification(
    dlp_client: dlp_v2.DlpServiceClient, parent: str
) -> bool:
    """DLP APIのテキスト検査と匿名化機能確認"""
    try:
        print("\nDLP APIテキスト検査と匿名化機能確認開始...")

        # テスト用のサンプルテキスト（個人情報を含む）
        sample_text = "山田太郎さんの電話番号は090-1234-5678です。メールアドレスはtaro.yamada@example.comです。"

        # 検査
        inspect_response = dlp_inspect(dlp_client, parent, sample_text)

        print("✅ DLP APIテキスト検査成功")
        print(f"検査対象テキスト: {sample_text}")
        print(f"検出された個人情報数: {len(inspect_response.result.findings)}")

        # 検出結果を表示
        for finding in inspect_response.result.findings:
            print(f"  - 種類: {finding.info_type.name}")
            print(f"    内容: {finding.quote}")
            print(f"    信頼度: {finding.likelihood.name}")

        deidentification_response = dlp_deidentification(
            dlp_client, parent, sample_text
        )

        print("✅ DLP APIテキスト匿名化成功")
        print(f"匿名化後テキスト: {deidentification_response.item.value}")

        return True

    except Exception as e:
        print(f"❌ DLP APIテキスト検査・匿名化失敗: {e}")
        return False


def check_dlp_deidentify_templates(
    dlp_client: dlp_v2.DlpServiceClient, parent: str
) -> bool:
    """DLP APIの匿名化テンプレート確認"""
    try:
        print("\nDLP API匿名化テンプレート確認開始...")

        # 匿名化テンプレートの一覧を取得
        deidentify_templates = dlp_client.list_deidentify_templates(parent=parent)
        template_list = list(deidentify_templates)

        print("✅ DLP API匿名化テンプレート確認成功")
        print(f"利用可能な匿名化テンプレート数(デフォルトは0): {len(template_list)}")

        # テンプレートの詳細表示
        for template in template_list:
            print(f"  - テンプレート名: {template.name}")
            print(f"    作成日: {template.create_time}")

        return True

    except Exception as e:
        print(f"❌ DLP API匿名化テンプレート確認失敗: {e}")
        return False


def main():
    """メイン処理"""
    print("=== GCP DLP API疎通確認 ===")

    # プロジェクトID取得
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        print("❌ GOOGLE_CLOUD_PROJECT環境変数が設定されていません")
        return

    print(f"プロジェクトID: {project_id}")

    # プロジェクトパスを構築
    parent = f"projects/{project_id}"

    # DLPクライアント初期化
    try:
        dlp_client = dlp_v2.DlpServiceClient()
        print("✅ DLPクライアント初期化成功")
    except Exception as e:
        print(f"❌ DLPクライアント初期化失敗: {e}")
        return

    # APIの疎通確認として、匿名化テンプレートを確認
    # プロジェクトで設定するので、初期は0個です
    template_check = check_dlp_deidentify_templates(dlp_client, parent)

    # テンプレート確認が失敗した場合は後続処理を中止
    if not template_check:
        print("❌ テンプレート確認に失敗したため、後続処理を中止します")
        return

    # テキスト検査と匿名化機能確認
    deidentification_check = check_dlp_deidentification(dlp_client, parent)

    # 結果まとめ
    print("\n=== 疎通確認結果 ===")
    print(f"匿名化テンプレート: {'✅ 成功' if template_check else '❌ 失敗'}")
    print(f"テキスト検査・匿名化: {'✅ 成功' if deidentification_check else '❌ 失敗'}")

    if template_check and deidentification_check:
        print("🎉 DLP API疎通確認完了！")
    else:
        print("⚠️ 一部の機能で問題が発生しました")


if __name__ == "__main__":
    main()
