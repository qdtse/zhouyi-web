# zhouyi-web

**Description:** 周易占卜系统 - I Ching divination web application deployed on Cloudflare Workers

## Overview

这是一个基于周易（易经）的占卜系统，提供梅花易数、八字分析、紫微斗数、诸葛神数等多种占卜功能。应用部署在 Cloudflare Workers 上，具有全球边缘计算能力，响应速度快。

## Deployment

### Platform
- **Cloudflare Workers** - 全球边缘计算平台
- **URL:** https://zhouyi-web.15996221599.workers.dev

### GitHub Actions CI/CD
- **Workflow:** `.github/workflows/deploy.yml`
- **Secrets Required:** `CLOUDFLARE_API_TOKEN`
- **Environment Variables:** `CLOUDFLARE_ACCOUNT_ID`

### Local Development
```bash
cd js
npm install
npm run dev  # wrangler dev
```

### Deploy
```bash
cd js
npm run deploy  # wrangler deploy
```

## API Endpoints

| Path | Method | Parameters | Description |
|------|--------|------------|-------------|
| `/` | GET | - | 首页 |
| `/health` | GET | - | 健康检查 |
| `/divine/text` | GET/POST | text, focus | 文字起卦 |
| `/divine/bazi` | GET/POST | year, month, day, hour | 八字分析 |
| `/divine/ziwei` | GET/POST | year, month, day, hour | 紫微斗数 |
| `/divine/random` | GET | - | 随机占卜 |
| `/divine/zhuge` | GET/POST | text | 诸葛神数 |
| `/divine/pair` | GET/POST | num1, num2 | 数字起卦 |
| `/divine/match` | GET/POST | male_year, male_month, etc. | 八字合婚 |

### Request Format
- **GET:** 使用 URL 查询参数
- **POST:** 使用 JSON body

### Response Format
- **Browser:** HTML 页面（美化展示）
- **API Client:** JSON 格式

## Architecture

```
js/
├── src/
│   ├── index.js    # Worker 入口，路由处理
│   ├── utils.js    # 周易核心算法（梅花易数等）
│   ├── bazi.js     # 八字分析
│   └── ziwei.js    # 紫微斗数
├── public/
│   └── index.html  # 静态前端页面
├── package.json
└── wrangler.toml   # Cloudflare Workers 配置
```

## Code Patterns

### Worker Entry Point
```javascript
export default {
  async fetch(request, env, ctx) {
    return handleRequest(request);
  }
};
```

### CORS Headers
```javascript
const CORS_HEADERS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type'
};
```

### Browser/API Dual Format Response
```javascript
const accept = request?.headers?.get('Accept') || '';
const isBrowser = accept.includes('text/html');
if (isBrowser) {
  return new Response(renderHtml(data), { headers: { 'Content-Type': 'text/html' } });
}
return new Response(JSON.stringify(data), { headers: CORS_HEADERS });
```

---

## User-Learned Best Practices & Constraints

> **Auto-Generated Section**: This section is maintained by `skill-evolution-manager`. Do not edit manually.

### User Preferences
- 优先使用 JavaScript 实现 Worker，避免 Python 的启动时间问题
- API 应同时支持 GET 和 POST 请求以便测试
- 浏览器访问应返回美化的 HTML 页面
- 使用 GitHub Actions 自动部署