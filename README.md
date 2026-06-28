# 新闻资讯 App

一个基于 **FastAPI + Vue 3** 的全栈新闻资讯移动端应用，功能覆盖新闻浏览、分类检索、收藏管理、浏览历史、AI 智能问答等。

## 技术栈

### 后端 (toutiao_backend)

| 技术 | 用途 |
|------|------|
| **FastAPI** | 异步 Web 框架 |
| **SQLAlchemy 2.0** | 异步 ORM（MySQL） |
| **aiomysql** | 异步 MySQL 驱动 |
| **Redis** | 缓存（新闻分类、新闻列表） |
| **httpx** | AI 对话流式 HTTP 请求 |
| **Passlib + bcrypt** | 密码加密 |
| **阿里云 DashScope (Qwen3)** | AI 问答接口 |

### 前端 (xwzx-news)

| 技术 | 用途 |
|------|------|
| **Vue 3** (Composition API) | 前端框架 |
| **Vite 7** | 构建工具 |
| **Vant 4** | 移动端 UI 组件库 |
| **Pinia** (持久化) | 状态管理 |
| **Vue Router 4** | 路由 |
| **vue-i18n** | 中英文国际化 |
| **Axios** | HTTP 请求 |

## 功能特性

- 新闻列表展示（分类切换、分页加载、下拉刷新）
- 新闻详情查看（相关推荐、浏览量统计）
- 用户注册 / 登录（Token 认证）
- 个人信息编辑、密码修改
- 新闻收藏（添加 / 取消 / 列表 / 清空）
- 浏览历史（自动记录 / 删除 / 清空）
- AI 智能问答（SSE 流式输出）
- 多主题切换（浅色 / 深色 / 蓝色 / 绿色）
- 中英文国际化

## 项目结构

```
news_project/
├── toutiao_backend/          # 后端
│   ├── cache/                # Redis 缓存操作
│   ├── config/               # 配置（数据库、Redis、AI、环境变量）
│   ├── crud/                 # 数据库 CRUD 操作
│   ├── models/               # SQLAlchemy ORM 模型
│   ├── routers/              # FastAPI 路由
│   ├── schemas/              # Pydantic 数据校验
│   ├── utils/                # 工具（认证、安全、响应、异常处理）
│   ├── main.py               # 应用入口
│   ├── requirements.txt      # Python 依赖
│   └── .env.example          # 环境变量模板
│
├── xwzx-news/                # 前端
│   ├── src/
│   │   ├── components/       # 公共组件
│   │   ├── config/           # API 配置
│   │   ├── i18n/             # 国际化
│   │   ├── router/           # 路由
│   │   ├── store/            # Pinia 状态管理
│   │   ├── views/            # 页面视图
│   │   ├── App.vue           # 根组件
│   │   ├── main.js           # 入口文件
│   │   └── style.css         # 全局样式
│   ├── package.json
│   └── vite.config.js
│
└── .gitignore
```

## 快速开始

### 环境要求

- Python 3.10+
- Node.js 18+
- MySQL 8.0+
- Redis 7.0+

### 1. 克隆项目

```bash
git clone <your-repo-url>
cd news_project
```

### 2. 准备基础设施

确保 MySQL 和 Redis 服务已启动，并创建数据库：

```bash
# 启动 Redis（Windows）
redis-server

# 启动 Redis（macOS/Linux）
redis-server

# 登录 MySQL 并创建数据库
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS news_app DEFAULT CHARACTER SET utf8"
```

### 3. 后端启动

```bash
# 进入后端目录
cd toutiao_backend

# 创建虚拟环境（可选，已有 .venv 可跳过）
python -m venv .venv

# 激活虚拟环境
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入实际的 MySQL 和 Redis 配置

# 启动服务（启动时自动创建数据库表）
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

服务启动后会自动创建数据库表，访问 http://127.0.0.1:8000/docs 查看 API 文档。

### 3. 前端启动

```bash
# 进入前端目录
cd xwzx-news

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

访问 http://localhost:5173 即可使用。

## 环境变量说明

参考 [.env.example](toutiao_backend/.env.example)：

| 变量 | 说明 |
|------|------|
| `DB_USER` / `DB_PASSWORD` / `DB_HOST` / `DB_PORT` / `DB_NAME` | MySQL 数据库配置 |
| `REDIS_HOST` / `REDIS_PORT` / `REDIS_DB` | Redis 缓存配置 |
| `AI_API_KEY` | 阿里云 DashScope API Key |
| `AI_API_ENDPOINT` | AI API 接口地址 |
| `AI_MODEL` | 通义千问模型名称 |

## API 概览

| 路径 | 方法 | 说明 |
|------|------|------|
| `/api/news/categories` | GET | 获取新闻分类 |
| `/api/news/list` | GET | 按分类获取新闻列表 |
| `/api/news/detail` | GET | 获取新闻详情 |
| `/api/user/register` | POST | 用户注册 |
| `/api/user/login` | POST | 用户登录 |
| `/api/user/info` | GET | 获取用户信息 |
| `/api/user/update` | PUT | 更新用户信息 |
| `/api/user/password` | PUT | 修改密码 |
| `/api/favorite/*` | GET/POST/DELETE | 收藏管理 |
| `/api/history/*` | GET/POST/DELETE | 浏览历史管理 |
| `/api/ai/chat` | POST | AI 对话（SSE 流式） |

## License

MIT
