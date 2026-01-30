# Vercel 部署配置

## 方式一: GitHub 集成部署 (推荐)

### 1. 推送代码到 GitHub

```bash
cd /Users/wanyview/SuiLight
git add .
git commit -m "feat: 准备 Vercel 部署"
git push origin main
```

### 2. Vercel 导入

1. 访问 https://vercel.com
2. 点击 "Add New..." → "Project"
3. 选择 "Import Git Repository"
4. 选择 "wanyview/SuiLight"
5. 配置项目:
   - Framework Preset: Other
   - Build Command: `pip install -r requirements.txt`
   - Output Directory: `ui`
6. 点击 "Deploy"

### 3. 访问

部署完成后，Vercel 会提供一个域名，例如:
- https://suilight.vercel.app

## 方式二: Vercel CLI

```bash
# 安装 Vercel CLI
npm i -g vercel

# 登录
vercel login

# 部署
cd /Users/wanyview/SuiLight
vercel --prod
```

## API 访问

部署后，API 地址为:
- https://suilight.vercel.app/api/

示例:
```bash
# 获取 Agent 列表
curl https://suilight.vercel.app/api/agents

# 创建 Agent
curl -X POST https://suilight.vercel.app/api/agents \
  -H "Content-Type: application/json" \
  -d '{"name":"牛顿","domain":"physics"}'
```

## 限制

### Vercel Serverless 限制

| 限制 | 值 |
|------|-----|
| 最大执行时间 | 30 秒 |
| 请求体大小 | 4.5 MB |
| 内存 | 1024 MB |

### 不支持的功能

- WebSocket
- 长连接
- Celery 任务队列 (需要 Redis)

## 完整部署方案

如果需要完整功能 (Celery + Redis)，建议使用:

| 平台 | 适合 |
|------|------|
| **Railway** | Docker 部署 |
| **Render** | Python 后端 |
| **Fly.io** | Docker 持久化 |
| **Heroku** | Python 应用 |

## 前端单独部署

如果只需前端:

```bash
# 部署 ui/ 目录到 Vercel
cd ui
vercel --prod
```

前端会自动访问同源的 API。
