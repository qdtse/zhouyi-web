# Vercel 部署故障排查

## 当前问题
`FUNCTION_INVOCATION_FAILED` - API 函数无法启动

## 可能原因

### 1. Python 依赖安装失败
某些库（如 `sxtwl`, `ephem`, `lunar-python`）可能需要编译，在 Vercel serverless 环境中可能失败。

### 2. 导入错误
模块导入路径问题或循环依赖。

### 3. 文件大小超限
部署包超过 50MB 限制。

## 排查步骤

### 步骤 1: 测试最小配置

1. 临时重命名 `requirements.txt`:
   ```bash
   mv requirements.txt requirements-full.txt
   mv requirements-minimal.txt requirements.txt
   ```

2. 重新部署到 Vercel

3. 访问 `https://your-domain.vercel.app/api/health`

如果成功，说明是依赖问题。继续步骤 2。

### 步骤 2: 逐个添加依赖

编辑 `requirements.txt`，逐个添加依赖并测试：

```txt
# 第一次测试
fastapi==0.104.1
pydantic==2.5.0
mangum==0.17.0
requests

# 第二次测试 - 添加简单的库
fastapi==0.104.1
pydantic==2.5.0
mangum==0.17.0
requests
cn2an
strokes

# 第三次测试 - 添加可能有问题的库
fastapi==0.104.1
pydantic==2.5.0
mangum==0.17.0
requests
cn2an
strokes
ichingshifa

# 继续测试其他库...
```

### 步骤 3: 查看详细错误日志

在 Vercel Dashboard:
1. 进入你的项目
2. 点击 "Functions" 标签
3. 点击失败的函数
4. 查看完整的错误堆栈

### 步骤 4: 检查构建日志

在 Vercel Dashboard:
1. 进入 "Deployments"
2. 点击最新的部署
3. 查看 "Building" 阶段的日志
4. 查找任何 pip install 失败的信息

## 常见解决方案

### 方案 A: 使用预编译的轮子
某些库需要编译。在 `requirements.txt` 中指定特定版本：

```txt
sxtwl==2.0.2
ephem==4.1.4
```

### 方案 B: 移除有问题的依赖
如果某个功能不是必需的，暂时注释掉相关代码和依赖。

### 方案 C: 使用 Docker 部署
如果依赖问题无法解决，考虑使用 Vercel 的 Docker 支持或切换到其他平台（如 Railway, Render）。

## 快速测试命令

本地测试 API:
```bash
pip install -r requirements.txt
cd api
python -c "from server import app; print('Import successful')"
```

如果本地导入失败，说明代码本身有问题。

## 联系支持

如果以上步骤都无法解决，请提供：
1. 完整的 Vercel 函数日志
2. 构建日志
3. 本地测试结果
