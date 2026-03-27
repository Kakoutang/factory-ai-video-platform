# 工厂 AI 视频工厂 部署到 Netlify

## 结论

这套项目可以部署到 Netlify，但推荐方式是：

- `Netlify`
  只部署前端页面
- `后端服务`
  单独部署到 Render / Railway / Fly.io / 你自己的服务器

原因：

- 当前后端是 `FastAPI + SQLite + 本地素材目录`
- Netlify 更适合托管前端，而不是这类长期运行的 Python 接口服务

## 你应该怎么配

### 1. Netlify 部署前端

项目里已经准备好：

- [netlify.toml](/Users/jennytang/Desktop/AI%20Video/ai-growth-platform/netlify.toml)

Netlify 会使用：

- base: `frontend`
- build command: `npm run build`

### 2. Netlify 环境变量

在 Netlify 后台添加：

- `NEXT_PUBLIC_API_BASE_URL`

值示例：

```bash
https://your-backend-domain.com
```

参考文件：

- [.env.netlify.example](/Users/jennytang/Desktop/AI%20Video/ai-growth-platform/.env.netlify.example)

### 3. 后端单独部署

后端请不要放 Netlify。

建议使用：

- Render
- Railway
- Fly.io
- 云服务器 Docker

后端部署完成后，你会得到一个地址，例如：

```bash
https://api.yourdomain.com
```

然后把这个地址填进 Netlify 的：

- `NEXT_PUBLIC_API_BASE_URL`

## Netlify 后台建议设置

### Build settings

- Base directory: `frontend`
- Build command: `npm run build`

如果 Netlify 自动识别到 `netlify.toml`，这里通常不需要再手改。

### Environment variables

- `NEXT_PUBLIC_API_BASE_URL=https://your-backend-domain.com`

## 现在的前端访问方式

前端页面会直接请求：

- `${NEXT_PUBLIC_API_BASE_URL}/api/...`
- `${NEXT_PUBLIC_API_BASE_URL}/client-assets/...`

所以：

- 后端地址必须可公网访问
- 后端必须允许前端域名跨域访问

## 后端需要同步调整的地方

后端环境变量建议设置：

- `CORS_ORIGINS=https://你的netlify域名`
- `CLIENT_ASSET_ROOT=/你的服务器素材目录`

## 最适合你的实际交付方式

1. 你把前端放 Netlify
2. 你把后端放 Render 或云服务器
3. 你给客户一个网页链接
4. 客户直接打开网页使用

这样客户完全不用安装。
