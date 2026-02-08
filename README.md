# 周易卜卦 & 紫微斗数 API

这是一个基于 Python FastAPI 构建的周易卜卦与紫微斗数排盘系统。

## 功能特性
- **周易卜卦**：测字、号码吉凶、起名分析。
- **诸葛神数**：384签完整版测字。
- **紫微斗数**：专业命盘生成（十二宫、主星、五行局等）。
- **时间起卦**：梅花易数时间卦。
- **随机起卦**：心诚则灵。

## 部署指南 (免费服务器)

本项目已配置好适配主流免费托管平台的文件 (`Procfile`, `vercel.json`)。

### 推荐平台 1: Vercel (推荐，速度快)
1. 将本项目上传至您的 GitHub 仓库。
2. 登录 [Vercel](https://vercel.com)。
3. 点击 "Add New..." -> "Project"，导入您的 GitHub 仓库。
4. Vercel 会自动识别 `vercel.json`，直接点击 "Deploy" 即可。
5. 部署完成后，您将获得一个免费的 `https://your-project.vercel.app` 域名。

### 推荐平台 2: Render (适合作为 Web Service)
1. 将本项目上传至您的 GitHub 仓库。
2. 登录 [Render](https://render.com)。
3. 点击 "New +" -> "Web Service"。
4. 连接您的 GitHub 仓库。
5. Runtime 选择 "Python 3"。
6. Build Command: `pip install -r requirements.txt`
7. Start Command: `uvicorn server:app --host 0.0.0.0 --port $PORT`
8. 选择 "Free" 计划，点击 "Create Web Service"。

## 本地运行

```bash
pip install -r requirements.txt
python server.py
```

访问: `http://localhost:8000`
