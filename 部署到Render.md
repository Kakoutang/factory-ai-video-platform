# 工厂 AI 视频工厂 后端部署到 Render

## 适用场景

这个方案用于：

- 前端放 `Netlify`
- 后端放 `Render`

最终效果：

- 客户只打开一个网页链接
- 前端页面由 Netlify 提供
- 接口和素材由 Render 提供

## 当前版本说明

当前仓库里的 Render 配置是：

- `免费演示版`

也就是说：

- 可以先跑通演示
- 不挂持久盘
- 不适合作为长期正式生产版

如果服务休眠、重启或重新部署，本地文件和 SQLite 数据可能重置。

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
- `free` 实例

默认环境变量：

- `CORS_ORIGINS`

数据库和演示数据直接使用仓库里的默认内容。

## 你需要手动补的环境变量

在 Render 后台补：

- `CORS_ORIGINS`

值示例：

```bash
https://your-netlify-site.netlify.app
```

参考文件：

- [.env.render.example](/Users/jennytang/Desktop/AI%20Video/ai-growth-platform/.env.render.example)

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

- 免费版只适合演示
- 服务可能休眠
- 本地数据和素材不保证长期保存
- 如果后期正式给客户用，再切回付费版并挂持久盘
