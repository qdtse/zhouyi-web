# zhouyi-web

**Description:** 周易占卜系统 - I Ching divination web application with Python FastAPI backend

## Overview

这是一个基于周易（易经）的占卜系统，提供梅花易数、八字分析、紫微斗数、诸葛神数等多种占卜功能。应用使用 Python FastAPI 构建，支持多种部署平台（Vercel、Cloudflare Workers、本地开发）。

## Deployment

### Platforms
- **Vercel** - Serverless deployment (Primary)
- **Cloudflare Workers** - Python Workers support
- **Local Development** - FastAPI with Uvicorn

### GitHub Actions CI/CD
- **Workflow:** `.github/workflows/deploy.yml`
- **Vercel:** Automatic deployment on push to master
- **Cloudflare:** Manual deployment with `wrangler deploy`

### Local Development
```bash
# Install dependencies
pip install workers-py numpy ichingshifa strokes cn2an fastapi uvicorn lunar_python

# Run server
uvicorn api.server:app --host 0.0.0.0 --port 8000

# Or use the script
python api/server.py
```

### Deploy to Vercel
```bash
# Automatic deployment via GitHub Actions
git push origin master
```

### Deploy to Cloudflare Workers
```bash
cd js
npm install
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
api/
├── server.py       # FastAPI 应用入口，路由处理
├── index.py        # Vercel serverless 入口
├── utils.py        # 周易核心算法（梅花易数、诸葛神数等）
├── bazi.py        # 八字分析
├── ziwei.py       # 紫微斗数
├── simple_lunar.py # 农历计算
└── *.json         # 数据文件（易经卦象、诸葛神数等）
public/
├── index.html      # 静态前端页面
├── style.css       # 样式文件
└── *.png          # 支付二维码图片
src/
└── worker.py       # Cloudflare Workers 入口
js/
├── src/           # JavaScript 版本（备用）
├── public/
└── package.json
pyproject.toml      # Python 项目配置
requirements.txt    # Python 依赖
vercel.json        # Vercel 配置
wrangler.toml      # Cloudflare Workers 配置
```

## Code Patterns

### FastAPI Server Entry
```python
app = FastAPI(title="Zhouyi Divination API")

@app.get("/health")
async def health_check():
    return {"status": "ok"}
```

### CORS Middleware
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Dual Route Support (GET/POST)
```python
@app.post("/divine/text")
@app.get("/divine/text")
async def divine_text(req: TextRequest):
    # 支持 GET (URL参数) 和 POST (JSON body)
    return result
```

---

## User-Learned Best Practices & Constraints

> **Auto-Generated Section**: This section is maintained by `skill-evolution-manager`. Do not edit manually.

### User Preferences
- 使用 Python FastAPI 作为主要后端，支持本地开发和 Vercel 部署
- API 应同时支持 GET 和 POST 请求以便测试
- 使用 GitHub Actions 自动部署到 Vercel
- 非必需的文件（测试脚本、文档、虚拟环境）移到 Backup 文件夹
- 项目结构保持简洁，只保留必要的源代码和配置文件