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

> 以下经验来自实际部署过程中的问题解决，由 Skill Evolution Manager 自动生成。

### 成功的解决方案

1. **Cloudflare Python Workers 启动超时**
   - 问题：Python Workers 使用 Pyodide，启动时间约 2 秒，超过 Cloudflare 1000ms CPU 限制
   - 解决方案：使用 JavaScript 重写 Worker，启动时间约 50ms
   - 日期：2026-02-20

2. **GitHub HTTPS 连接被阻止**
   - 问题：网络环境限制导致 GitHub 443 端口无法访问
   - 解决方案：使用 SSH over 443 端口绕过网络限制
   ```bash
   git remote set-url origin git@ssh.github.com:user/repo.git
   $env:GIT_SSH_COMMAND="ssh -p 443"
   ```
   - 日期：2026-02-20

3. **Cloudflare API Token 权限不足**
   - 问题：多次部署失败，提示 Authentication error
   - 解决方案：API Token 需要以下权限：
     - Workers Scripts: Edit
     - Account Settings: Read
     - User Details: Read
     - User Memberships: Read
   - 最简单的解决方案是使用 Global API Key
   - 日期：2026-02-20

4. **Worker API 只支持 POST 请求**
   - 问题：浏览器直接访问 API 返回 404
   - 解决方案：修改路由逻辑，同时支持 GET（URL 参数）和 POST（JSON body）请求
   - 日期：2026-02-20

5. **浏览器访问 API 显示纯 JSON**
   - 问题：用户体验不佳
   - 解决方案：通过检查 Accept header 判断请求来源，浏览器返回 HTML，API 返回 JSON
   - 日期：2026-02-20

### 失败的尝试

1. **尝试优化 Python Worker 启动时间**
   - 原因：Pyodide 本身需要约 2 秒初始化，无法通过代码优化解决
   - 教训：Cloudflare Python Workers 不适合需要快速启动的应用
   - 日期：2026-02-20

2. **使用 lunar-python 库**
   - 原因：该库只有 .tar.gz 源码包，Pyodide 需要 wheel 包
   - 教训：Cloudflare Python Workers 只支持 wheel 格式的依赖包
   - 日期：2026-02-20

### 用户偏好

- 优先使用 JavaScript 实现 Worker，避免 Python 的启动时间问题
- API 应同时支持 GET 和 POST 请求以便测试
- 浏览器访问应返回美化的 HTML 页面
- 使用 GitHub Actions 自动部署

---

*Last updated: 2026-02-20 by Skill Evolution Manager*
