# 工厂 AI 视频工厂

这是可直接交付给客户的网页版 / 本地版视频生产系统，用来完成：

1. 资料素材整理
2. 视频任务创建
3. 脚本生成
4. 视频生成
5. 成片查看与审核

## 推荐交付方式

### 网页版

推荐你自己部署到服务器后，把网址直接发给客户使用。

部署说明见：

- [网页部署说明.md](/Users/jennytang/Desktop/AI%20Video/ai-growth-platform/%E7%BD%91%E9%A1%B5%E9%83%A8%E7%BD%B2%E8%AF%B4%E6%98%8E.md)
- [部署到Netlify.md](/Users/jennytang/Desktop/AI%20Video/ai-growth-platform/%E9%83%A8%E7%BD%B2%E5%88%B0Netlify.md)
- [部署到Render.md](/Users/jennytang/Desktop/AI%20Video/ai-growth-platform/%E9%83%A8%E7%BD%B2%E5%88%B0Render.md)

### 本地版

如需本地试运行或内网演示，可使用下面的安装和启动脚本。

## 交付包内文件

- [install_factory_console.command](/Users/jennytang/Desktop/AI%20Video/ai-growth-platform/install_factory_console.command)
  首次安装依赖
- [start_factory_console.command](/Users/jennytang/Desktop/AI%20Video/ai-growth-platform/start_factory_console.command)
  启动系统
- [stop_factory_console.command](/Users/jennytang/Desktop/AI%20Video/ai-growth-platform/stop_factory_console.command)
  停止系统
- [客户使用说明.md](/Users/jennytang/Desktop/AI%20Video/ai-growth-platform/%E5%AE%A2%E6%88%B7%E4%BD%BF%E7%94%A8%E8%AF%B4%E6%98%8E.md)
  客户使用说明
- [网页部署说明.md](/Users/jennytang/Desktop/AI%20Video/ai-growth-platform/%E7%BD%91%E9%A1%B5%E9%83%A8%E7%BD%B2%E8%AF%B4%E6%98%8E.md)
  网页部署说明
- [docker-compose.web.yml](/Users/jennytang/Desktop/AI%20Video/ai-growth-platform/docker-compose.web.yml)
  网页版部署配置
- [netlify.toml](/Users/jennytang/Desktop/AI%20Video/ai-growth-platform/netlify.toml)
  Netlify 前端部署配置
- [render.yaml](/Users/jennytang/Desktop/AI%20Video/ai-growth-platform/render.yaml)
  Render 后端部署配置

## 客户使用方式

### 首次安装

双击：

- [install_factory_console.command](/Users/jennytang/Desktop/AI%20Video/ai-growth-platform/install_factory_console.command)

### 日常启动

双击：

- [start_factory_console.command](/Users/jennytang/Desktop/AI%20Video/ai-growth-platform/start_factory_console.command)

启动后打开浏览器访问：

- [http://127.0.0.1:3001](http://127.0.0.1:3001)

### 日常关闭

双击：

- [stop_factory_console.command](/Users/jennytang/Desktop/AI%20Video/ai-growth-platform/stop_factory_console.command)

## 默认地址

- 前端：`http://127.0.0.1:3001`
- 后端：`http://127.0.0.1:8001`

## 当前支持方式

- 网页版部署
- 本地部署
- 本地 SQLite 数据库
- 本地素材同步
- 客户自带视频生成 API

## 目录说明

- `frontend`
  客户工作台前端
- `backend`
  本地接口服务、数据库和素材同步逻辑
- `runtime/logs`
  启动后的运行日志
- `docs`
  内部资料，不需要给客户直接看
