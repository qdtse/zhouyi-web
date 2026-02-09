# Vercel 部署指南

## 修复内容

1. **vercel.json** - 添加了正确的构建配置和路由规则
2. **api/index.py** - 使用 Mangum 适配器包装 FastAPI 应用
3. **requirements.txt** - 添加 mangum，移除 uvicorn（serverless 不需要）
4. **runtime.txt** - 指定 Python 3.9 运行时
5. **.vercelignore** - 排除不必要的文件以减小部署包大小
6. **api/server.py** - 移除静态文件挂载（由 Vercel 处理）

## 部署步骤

1. 提交所有更改到 Git：
   ```bash
   git add .
   git commit -m "Fix Vercel deployment configuration"
   git push
   ```

2. 在 Vercel 控制台重新部署或等待自动部署

3. 检查部署日志，确认没有错误

## 测试 API

部署成功后，测试以下端点：

- `https://your-domain.vercel.app/api/health` - 健康检查
- `https://your-domain.vercel.app/` - 静态页面

## 常见问题

### 如果仍然出现 500 错误：

1. 检查 Vercel 函数日志（Dashboard > Functions > Logs）
2. 确认所有依赖都正确安装
3. 检查是否有依赖包超过 50MB 限制

### 如果依赖包太大：

考虑移除不常用的功能或使用更轻量的替代库。

## 注意事项

- Vercel serverless 函数有 50MB 大小限制
- 函数执行超时设置为 10 秒
- 内存限制为 1024MB
