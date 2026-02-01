"""
推送历史复现知识胶囊到 CapsuleHub
2026-01-31 新增
"""

import sys
import os
import json
import requests
import base64

sys.path.insert(0, '/Users/wanyview/clawd/SuiLight/src')
os.chdir('/Users/wanyview/clawd/SuiLight')

from historical_replication import HistoricalReplicationSystem


def get_github_token():
    """获取 GitHub Token"""
    try:
        import keyring
        token = keyring.get_password("github", "wanyview")
        if token:
            return token
    except:
        pass
    
    # 备选：从环境变量获取
    return os.environ.get("GITHUB_TOKEN", "")


def create_capsule_payload(capsule):
    """创建胶囊负载"""
    return {
        "title": capsule.title,
        "content": capsule.insight,
        "domain": capsule.domains[0] if capsule.domains else "interdisciplinary",
        "topics": capsule.topics,
        "authors": capsule.authors,
        "datm_score": capsule.datm_score,
        "metadata": {
            "type": capsule.type,
            "original_experiment": capsule.original_experiment,
            "replication_experiment": capsule.replication_experiment,
            "new_discovery": capsule.new_discovery,
            "connection": capsule.connection
        }
    }


def push_to_capsulehub(capsules):
    """推送到 CapsuleHub"""
    
    base_url = "http://localhost:8000"
    
    print("="*70)
    print("🚀 推送到 CapsuleHub")
    print("="*70)
    print()
    
    results = []
    
    for i, capsule in enumerate(capsules, 1):
        print(f"📤 推送胶囊 {i}/{len(capsules)}: {capsule.id}")
        print(f"   标题: {capsule.title[:50]}...")
        
        payload = create_capsule_payload(capsule)
        
        try:
            response = requests.post(
                f"{base_url}/api/capsules",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code in [200, 201]:
                result = response.json()
                print(f"   ✅ 成功! ID: {result.get('id', 'N/A')}")
                results.append({"id": capsule.id, "status": "success", "result": result})
            else:
                print(f"   ❌ 失败: {response.status_code} - {response.text[:100]}")
                results.append({"id": capsule.id, "status": "failed", "error": response.text})
                
        except requests.exceptions.ConnectionError:
            print(f"   ⚠️  连接 CapsuleHub 失败，保存到本地文件")
            results.append({"id": capsule.id, "status": "saved_locally"})
        except Exception as e:
            print(f"   ❌ 错误: {e}")
            results.append({"id": capsule.id, "status": "error", "error": str(e)})
        
        print()
    
    return results


def save_to_json(capsules, filename="historical_replication_capsules_for_push.json"):
    """保存胶囊数据到 JSON 文件"""
    
    capsules_data = []
    for c in capsules:
        data = c.to_dict()
        # 添加洞察内容
        data["insight"] = c.insight
        capsules_data.append(data)
    
    filepath = f"/Users/wanyview/clawd/SuiLight/{filename}"
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(capsules_data, f, ensure_ascii=False, indent=2)
    
    print(f"💾 已保存到: {filepath}")
    return filepath


def main():
    """主函数"""
    
    print("="*70)
    print("📦 历史复现知识胶囊 - 推送工具 v1.0")
    print("="*70)
    print()
    
    # 生成所有胶囊
    system = HistoricalReplicationSystem()
    
    print("🔄 生成历史复现胶囊...")
    print()
    
    capsule1 = system.create_tour_graphene_capsule()
    print(f"  ✅ {capsule1.id}: {capsule1.title}")
    
    capsule2 = system.create_newton_prism_capsule()
    print(f"  ✅ {capsule2.id}: {capsule2.title}")
    
    capsule3 = system.create_pavlov_conditioning_capsule()
    print(f"  ✅ {capsule3.id}: {capsule3.title}")
    
    capsule4 = system.create_pasteur_flask_capsule()
    print(f"  ✅ {capsule4.id}: {capsule4.title}")
    
    capsule5 = system.create_mendel_peas_capsule()
    print(f"  ✅ {capsule5.id}: {capsule5.title}")
    
    capsules = system.get_all_capsules()
    
    print()
    print("="*70)
    print("📊 胶囊统计")
    print("="*70)
    
    print(f"\n总胶囊数: {len(capsules)}")
    
    total_span = sum(c.connection['temporal_span'] for c in capsules)
    avg_span = total_span / len(capsules)
    
    avg_truth = sum(c.datm_score['truth'] for c in capsules) / len(capsules)
    avg_goodness = sum(c.datm_score['goodness'] for c in capsules) / len(capsules)
    avg_beauty = sum(c.datm_score['beauty'] for c in capsules) / len(capsules)
    avg_intelligence = sum(c.datm_score['intelligence'] for c in capsules) / len(capsules)
    
    print(f"平均时间跨度: {avg_span:.1f} 年")
    print(f"\n平均 DATM 评分:")
    print(f"  - Truth: {avg_truth:.1f}")
    print(f"  - Goodness: {avg_goodness:.1f}")
    print(f"  - Beauty: {avg_beauty:.1f}")
    print(f"  - Intelligence: {avg_intelligence:.1f}")
    
    # 保存到本地文件
    print()
    local_file = save_to_json(capsules)
    
    # 尝试推送到 CapsuleHub
    print()
    results = push_to_capsulehub(capsules)
    
    # 统计结果
    success_count = len([r for r in results if r['status'] == 'success'])
    failed_count = len([r for r in results if r['status'] == 'failed'])
    
    print("="*70)
    print("📊 推送结果")
    print("="*70)
    print(f"\n成功: {success_count}")
    print(f"失败: {failed_count}")
    print(f"本地保存: {local_file}")
    
    print()
    print("✨ 完成！")


if __name__ == "__main__":
    main()
