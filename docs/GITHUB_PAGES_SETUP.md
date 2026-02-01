# SuiLight GitHub Pages 部署配置

## 当前状态

✅ **gh-pages 分支已创建** - 包含前端静态文件  
✅ **文件已推送到 GitHub**  
⏳ **需要手动配置 Pages 设置**

---

## 快速配置 (1分钟)

### 步骤 1: 访问设置页面

🔗 **点击链接**: https://github.com/wanyview/SuiLight/settings/pages

### 步骤 2: 配置 Pages

在页面上选择：

| 设置项 | 选择 |
|--------|------|
| **Source** | ✅ `Deploy from a branch` |
| **Branch** | `gh-pages` |
| **Folder** | `/ (root)` |
| **Click** | 💾 `Save` |

### 步骤 3: 等待部署

- 部署需要 1-2 分钟
- 刷新页面后显示绿色 ✓

---

## 部署成功 ✅

**访问地址**: https://wanyview.github.io/SuiLight/

---

## 验证部署

```bash
# 本地测试
cd SuiLight
python3 -m http.server 8080 -d dist
# 访问 http://localhost:8080
```

---

## 文件结构

```
SuiLight/
├── ui/              # 源代码 (HTML/CSS/JS)
├── dist/            # 编译后的静态文件
│   ├── index.html   # 主页面
│   ├── salon.html   # 沙龙页面
│   ├── graph.html   # 知识图谱
│   ├── coffee.html  # Coffee 页面
│   ├── share.html   # 分享页面
│   ├── .nojekyll    # 禁用 Jekyll
│   └── _redirects   # SPA 路由支持
└── api/             # API (需要 Railway/Render)
```

---

## 手动更新部署

如果修改了前端文件，重新部署：

```bash
cd SuiLight

# 1. 更新 dist 目录
cp -r ui/* dist/

# 2. 提交到 gh-pages 分支
git checkout gh-pages
git add -A
git commit -m "Update: $(date '+%Y-%m-%d %H:%M')"
git push origin gh-pages --force

# 3. 切回 main
git checkout main
```

---

## 自动化部署 (可选)

### GitHub Actions

1. 创建 `.github/workflows/deploy.yml`
2. 每次 push 自动部署到 Pages

### 脚本部署

```bash
./deploy_github_pages.sh
```

---

## 常见问题

### Q: 显示 404 错误？

A: 等待 2-3 分钟让 GitHub 部署完成，然后刷新。

### Q: 样式丢失？

A: 检查 `dist/_redirects` 是否存在：
```
/*  /index.html  200
```

### Q: API 不工作？

A: 前端已部署，但 API 需要单独部署到 Railway/Render。

---

## 相关信息

- **GitHub 仓库**: https://github.com/wanyview/SuiLight
- **gh-pages 分支**: https://github.com/wanyview/SuiLight/tree/gh-pages
- **部署文档**: `docs/GITHUB_PAGES_SETUP.md`
