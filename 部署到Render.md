# 工厂 AI 视频工厂 后端部署到 Render

## 适用场景

这个方案用于：

- 前端放 `Netlify`
- 后端放 `Render`

最终效果：

- 客户只打开一个网页链接
- 前端页面由 Netlify 提供
- 接口和素材由 Render 提供

## 项目里已经准备好的文件

- [render.yaml](/Users/jennytang/Desktop/AI%20Video/ai-growth-platform/render.yaml)
- [.env.render.example](/Users/jennytang/Desktop/AI%20Video/ai-growth-platform/.env.render.example)

## Render 部署方式

推荐用 `Blueprint` 方式导入：

1. 把项目推到 Git 仓库
2. 在 Render 里选择 `New +`
3. 选择 `Blueprint`
4. 连接你的仓库
5. Render 会自动读取：

```bash
render.yaml
```

## Render 服务说明

后端会使用：

- `rootDir=backend`
- `FastAPI + uvicorn`
- 持久化磁盘挂载到 `/var/data`

默认环境变量：

- `DATABASE_URL=sqlite:////var/data/app.db`
- `CLIENT_ASSET_ROOT=/var/data/client-assets`

这意味着：

- 数据库会保存在 Render 持久盘
- 客户素材也会保存在 Render 持久盘

## 你需要手动补的环境变量

在 Render 后台补：

- `CORS_ORIGINS`

值示例：

```bash
https://your-netlify-site.netlify.app
```

参考文件：

- [.env.render.example](/Users/jennytang/Desktop/AI%20Video/ai-growth-platform/.env.render.example)

## 素材怎么放

后端默认从这里读取素材：

```bash
/var/data/client-assets
```

所以你需要把客户素材上传到 Render 服务器的这个目录，或者登录实例后同步进去。

## 部署完成后会得到什么

你会拿到一个 Render 后端地址，例如：

```bash
https://factory-video-backend.onrender.com
```

然后把这个地址填到 Netlify 的：

```bash
NEXT_PUBLIC_API_BASE_URL
```

## 最终连接方式

1. Render 部署后端
2. 得到 Render 域名
3. 在 Netlify 设置：

```bash
NEXT_PUBLIC_API_BASE_URL=https://factory-video-backend.onrender.com
```

4. 重新部署 Netlify

完成后客户直接打开 Netlify 链接即可使用。

## 注意事项

- 如果你不挂持久盘，SQLite 和素材都会丢
- 所以 Render 必须保留磁盘挂载
- 如果后期客户量更大，再考虑 PostgreSQL 和对象存储
