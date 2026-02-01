#!/bin/bash
# SuiLight GitHub Pages 自动配置脚本

set -e

REPO="wanyview/SuiLight"
BRANCH="gh-pages"

echo "🚀 SuiLight GitHub Pages 配置"
echo "=============================="
echo ""

# 获取 GitHub Token
echo "📝 需要 GitHub Personal Access Token"
echo "   Token 需要 'repo' 和 'admin:repo_hook' 权限"
echo ""
read -p "请输入 Token (或直接按 Enter 打开手动配置): " TOKEN

if [ -z "$TOKEN" ]; then
    echo ""
    echo "🔗 请手动配置:"
    echo "   https://github.com/$REPO/settings/pages"
    echo ""
    echo "   1. Source: Deploy from a branch"
    echo "   2. Branch: gh-pages / (root)"
    echo "   3. 点击 Save"
    echo ""
    exit 0
fi

# 配置 GitHub Pages
echo ""
echo "⚙️  配置 GitHub Pages..."

RESPONSE=$(curl -s -X PUT \
  -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/$REPO/pages \
  -d "{\"source\":{\"branch\":\"$BRANCH\",\"path\":\"/\"}}")

echo "$RESPONSE" | jq '.'

# 检查状态
STATUS=$(echo "$RESPONSE" | jq -r '.status // empty')
if [ "$STATUS" == "built" ] || [ "$STATUS" == "queued" ]; then
    echo ""
    echo "✅ 配置成功！"
    echo ""
    echo "📱 访问地址: https://wanyview.github.io/SuiLight/"
    echo ""
    echo "⏳ 等待部署完成 (可能需要 1-2 分钟)"
else
    echo ""
    echo "⚠️  可能需要手动配置"
    echo "🔗 https://github.com/$REPO/settings/pages"
fi
