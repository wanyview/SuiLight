#!/bin/bash
# SuiLight GitHub Pages 部署脚本

echo "🚀 开始部署 SuiLight 到 GitHub Pages..."
echo ""

# 检查 ui 目录是否存在
if [ ! -d "ui" ]; then
    echo "❌ 错误: ui 目录不存在"
    exit 1
fi

# 构建静态文件
echo "📦 验证前端文件..."
ls -la ui/

# 创建 .nojekyll (GitHub Pages 需要)
touch ui/.nojekyll

# 创建 _redirects (SPA 路由支持)
cat > ui/_redirects << 'EOF'
/*  /index.html  200
EOF

echo ""
echo "✅ 前端文件准备完成"
echo ""

# 安装 gh-pages (如果没有)
if ! command -v npx &> /dev/null; then
    echo "❌ 需要安装 npx (Node.js)"
    exit 1
fi

# 部署到 GitHub Pages
echo "📤 部署到 GitHub Pages..."
npx gh-pages -d ui -t true

echo ""
echo "🎉 部署完成！"
echo ""
echo "访问地址: https://wanyview.github.io/SuiLight/"
echo ""
echo "注意: API 需要单独部署 (Railway/Render/Fly.io)"
