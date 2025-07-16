#!/usr/bin/env python3
"""
GCP DLP API疎通確認用の最低限のコード
"""

import os
from google.cloud import dlp_v2


def check_dlp_basic_connection(dlp_client: dlp_v2.DlpServiceClient, project_id: str) -> bool:
    """DLP APIの基本的な疎通確認"""
    try:
        print("DLP API疎通確認開始...")
        
        # プロジェクトパスを構築
        parent = f"projects/{project_id}"
        
        # 基本的なリクエストでAPIが動作するかを確認
        inspect_templates = dlp_client.list_inspect_templates(parent=parent)
        
        print("✅ DLP API疎通確認成功")
        print(f"プロジェクト: {project_id}")
        print(f"利用可能なInspect Templates数: {len(list(inspect_templates))}")
        
        return True
        
    except Exception as e:
        print(f"❌ DLP API疎通確認失敗: {e}")
        return False


def check_dlp_inspection(dlp_client: dlp_v2.DlpServiceClient, project_id: str) -> bool:
    """DLP APIのテキスト検査機能確認"""
    try:
        print("\nDLP APIテキスト検査機能確認開始...")
        
        # テスト用のサンプルテキスト（個人情報を含む）
        sample_text = "山田太郎さんの電話番号は090-1234-5678です。メールアドレスはtaro.yamada@example.comです。"
        
        # プロジェクトパスを構築
        parent = f"projects/{project_id}"
        
        # 検査設定
        inspect_config = {
            "info_types": [
                {"name": "PHONE_NUMBER"},
                {"name": "EMAIL_ADDRESS"},
                {"name": "PERSON_NAME"}
            ],
            "min_likelihood": dlp_v2.Likelihood.POSSIBLE,
            "include_quote": True,
        }
        
        # 検査リクエスト
        request = {
            "parent": parent,
            "inspect_config": inspect_config,
            "item": {"value": sample_text}
        }
        
        # 検査実行
        response = dlp_client.inspect_content(request=request)
        
        print("✅ DLP APIテキスト検査成功")
        print(f"検査対象テキスト: {sample_text}")
        print(f"検出された個人情報数: {len(response.result.findings)}")
        
        # 検出結果を表示
        for finding in response.result.findings:
            print(f"  - 種類: {finding.info_type.name}")
            print(f"    内容: {finding.quote}")
            print(f"    信頼度: {finding.likelihood.name}")
        
        return True
        
    except Exception as e:
        print(f"❌ DLP APIテキスト検査失敗: {e}")
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
    
    # DLPクライアント初期化
    try:
        dlp_client = dlp_v2.DlpServiceClient()
        print("✅ DLPクライアント初期化成功")
    except Exception as e:
        print(f"❌ DLPクライアント初期化失敗: {e}")
        return
    
    # 基本的な疎通確認
    basic_check = check_dlp_basic_connection(dlp_client, project_id)
    
    # テキスト検査機能確認
    inspection_check = check_dlp_inspection(dlp_client, project_id)
    
    # 結果まとめ
    print("\n=== 疎通確認結果 ===")
    print(f"基本疎通確認: {'✅ 成功' if basic_check else '❌ 失敗'}")
    print(f"テキスト検査: {'✅ 成功' if inspection_check else '❌ 失敗'}")
    
    if basic_check and inspection_check:
        print("🎉 DLP API疎通確認完了！")
    else:
        print("⚠️ 一部の機能で問題が発生しました")


if __name__ == "__main__":
    main()
