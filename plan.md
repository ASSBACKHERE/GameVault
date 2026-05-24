# GameVault 项目规划

## 1. 项目名称

**GameVault — Full-Stack Game Backlog & Analytics System (Python Edition)**

中文名称：**游戏愿望单与游玩进度分析系统**

本项目是一个面向游戏玩家的 Web 数据库应用系统，用于管理个人游戏愿望单、游戏库、游玩状态、平台信息、标签分类、评分评价与消费统计。系统支持用户登录、游戏记录的增删改查、分类筛选、详情展示和数据分析，满足数据库系统课程期末大作业对 Web 应用、数据库设计、前后端开发和现场演示的要求。

## 2. 项目目标

1. 完成一个可运行、可演示的数据库 Web 应用系统。
2. 使用 Python 后端和 MySQL 数据库完成核心业务数据管理。
3. 使用 Docker Compose 一键启动前端、后端、数据库等开发环境。
4. 实现游戏愿望单、游戏收藏、游玩进度、分类标签、平台、评分、消费金额等功能。
5. 提供高级、美观、现代化的前端页面，适合课程展示和 PPT 演示。
6. 输出实验报告所需的需求分析、数据库设计、系统设计、测试用例和源码。

## 3. 技术栈选型

### 3.1 后端

- 语言：Python 3.12
- Web 框架：FastAPI
- ORM：SQLAlchemy 2.x
- 数据校验：Pydantic
- 数据库迁移：Alembic
- 认证方式：JWT Token
- 密码加密：Passlib + bcrypt
- API 文档：FastAPI 自动生成 OpenAPI / Swagger 文档

选择 FastAPI 的原因：

- 开发速度快，代码简洁，适合课程项目快速落地。
- 自动生成接口文档，方便调试和演示。
- 类型提示清晰，适合维护和扩展。
- 与现代前端框架配合良好。

### 3.2 数据库

- 数据库：MySQL 8.0
- 管理工具：phpMyAdmin 或 Adminer
- 字符集：utf8mb4
- 排序规则：utf8mb4_unicode_ci

数据库原则：

- 保证实体完整性、参照完整性和基本数据依赖关系。
- 使用外键维护用户、游戏、分类、平台、标签、日志等表之间的关系。
- 关键字段添加索引，提高搜索、筛选和统计性能。

### 3.3 前端

- 框架：React + Vite + TypeScript
- UI 组件库：Ant Design
- 样式增强：Tailwind CSS
- 图表库：Apache ECharts 或 Recharts
- 请求库：Axios
- 路由：React Router
- 状态管理：Zustand

前端风格定位：

- 深色高级游戏风界面。
- 使用卡片、渐变背景、玻璃拟态、游戏封面墙、统计图表等视觉元素。
- 页面适配桌面端展示，保证课堂演示效果。

### 3.4 部署与环境

- 容器编排：Docker Compose
- 服务组成：
  - `frontend`：React 前端服务
  - `backend`：FastAPI 后端服务
  - `mysql`：MySQL 8.0 数据库
  - `adminer` 或 `phpmyadmin`：数据库可视化管理工具
- 一键启动命令：

```bash
docker compose up --build
```

## 4. 用户角色与权限

### 4.1 普通用户

普通用户可以：

- 注册和登录系统。
- 修改个人资料。
- 管理自己的游戏愿望单和游戏库。
- 添加、修改、删除游戏记录。
- 查看游戏详情、评分、游玩进度和统计分析。

### 4.2 管理员

管理员可以：

- 管理系统内的用户。
- 管理全局游戏平台、游戏类型、标签数据。
- 查看系统整体数据统计。

课程项目阶段可以先实现普通用户核心功能，管理员功能作为增强功能。

## 5. 核心业务功能

### 5.1 用户登录与个人资料

功能内容：

- 用户注册
- 用户登录
- JWT 身份验证
- 修改昵称、头像、简介
- 查看个人游戏数据概览

对应作业要求：

- 满足“用户登录及验证、个人信息设置”。

### 5.2 游戏愿望单管理

功能内容：

- 添加想玩的游戏
- 编辑游戏名称、封面、发行日期、开发商、发行商、简介
- 设置期望购买价格
- 设置优先级：低、中、高
- 设置是否已经购买
- 删除愿望单记录
- 按名称、平台、类型、标签、优先级搜索和筛选

### 5.3 游戏库与游玩状态管理

功能内容：

- 将游戏加入个人游戏库
- 设置游戏状态：
  - 想玩
  - 已购买
  - 正在玩
  - 已通关
  - 已搁置
  - 已放弃
- 记录游玩时长
- 记录开始游玩日期和通关日期
- 记录个人评分
- 编写个人评价
- 修改或删除游戏库记录

### 5.4 分类、平台与标签管理

功能内容：

- 游戏类型管理，例如 RPG、ACT、AVG、FPS、SLG、SIM、独立游戏等。
- 平台管理，例如 Steam、Epic、PlayStation、Xbox、Switch、PC、Mobile 等。
- 标签管理，例如 开放世界、剧情向、多人合作、肉鸽、像素风、二次元、恐怖等。
- 在分类下展示对应游戏列表。

对应作业要求：

- 满足“分类管理、分类下展示列表”。

### 5.5 游戏详情页

功能内容：

- 展示游戏基础信息。
- 展示所属平台、类型和标签。
- 展示用户个人状态、评分、游玩时长、购买价格。
- 展示相关游玩日志。
- 展示同类型或同标签游戏推荐。

### 5.6 游玩日志

功能内容：

- 添加单次游玩记录。
- 记录游玩日期、游玩时长、游戏进度、备注。
- 修改和删除日志。
- 按时间线展示游玩过程。

### 5.7 数据统计与分析

功能内容：

- 游戏总数统计。
- 愿望单数量统计。
- 已购买游戏数量统计。
- 已通关游戏数量统计。
- 总消费金额统计。
- 总游玩时长统计。
- 不同平台游戏数量占比。
- 不同类型游戏数量占比。
- 每月新增游戏数量趋势。
- 每月游玩时长趋势。
- 个人游戏完成率分析。

对应作业要求：

- 满足“详情、统计、分析”。

### 5.8 首页仪表盘

首页展示：

- 搜索框
- 游戏总数
- 愿望单数量
- 正在游玩数量
- 已通关数量
- 最近添加游戏
- 高优先级愿望单
- 平台分布图
- 类型分布图
- 最近游玩日志

对应作业要求：

- 满足“首页有搜索框、数量统计、分类展示”。

## 6. 页面规划

### 6.1 前台页面

1. 登录页
2. 注册页
3. 首页仪表盘
4. 游戏愿望单页面
5. 我的游戏库页面
6. 游戏添加页面
7. 游戏编辑页面
8. 游戏详情页面
9. 分类管理页面
10. 平台管理页面
11. 标签管理页面
12. 游玩日志页面
13. 数据统计分析页面
14. 个人资料页面

### 6.2 页面视觉设计

整体设计关键词：

- 深色主题
- 高级感
- 游戏封面卡片
- 数据可视化
- 玻璃拟态
- 渐变背景
- 响应式布局

建议主色：

- 背景色：`#0B1020`
- 卡片色：`#111827`
- 主题紫：`#7C3AED`
- 主题蓝：`#2563EB`
- 强调绿：`#22C55E`
- 警告橙：`#F97316`

## 7. 数据库设计初稿

### 7.1 用户表 users

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| id | BIGINT | 主键 |
| username | VARCHAR(50) | 用户名，唯一 |
| email | VARCHAR(100) | 邮箱，唯一 |
| password_hash | VARCHAR(255) | 加密密码 |
| nickname | VARCHAR(50) | 昵称 |
| avatar_url | VARCHAR(255) | 头像 |
| bio | TEXT | 个人简介 |
| role | VARCHAR(20) | 用户角色 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

### 7.2 游戏表 games

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| id | BIGINT | 主键 |
| title | VARCHAR(120) | 游戏名称 |
| original_title | VARCHAR(120) | 原始名称 |
| cover_url | VARCHAR(255) | 封面图 |
| developer | VARCHAR(120) | 开发商 |
| publisher | VARCHAR(120) | 发行商 |
| release_date | DATE | 发行日期 |
| description | TEXT | 游戏简介 |
| created_by | BIGINT | 创建用户 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

### 7.3 平台表 platforms

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| id | BIGINT | 主键 |
| name | VARCHAR(80) | 平台名称 |
| icon | VARCHAR(80) | 平台图标 |
| created_at | DATETIME | 创建时间 |

### 7.4 类型表 categories

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| id | BIGINT | 主键 |
| name | VARCHAR(80) | 类型名称 |
| description | TEXT | 类型说明 |
| created_at | DATETIME | 创建时间 |

### 7.5 标签表 tags

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| id | BIGINT | 主键 |
| name | VARCHAR(80) | 标签名称 |
| color | VARCHAR(20) | 标签颜色 |
| created_at | DATETIME | 创建时间 |

### 7.6 游戏与平台关联表 game_platforms

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| game_id | BIGINT | 游戏 ID |
| platform_id | BIGINT | 平台 ID |

### 7.7 游戏与类型关联表 game_categories

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| game_id | BIGINT | 游戏 ID |
| category_id | BIGINT | 类型 ID |

### 7.8 游戏与标签关联表 game_tags

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| game_id | BIGINT | 游戏 ID |
| tag_id | BIGINT | 标签 ID |

### 7.9 用户游戏库表 user_games

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| id | BIGINT | 主键 |
| user_id | BIGINT | 用户 ID |
| game_id | BIGINT | 游戏 ID |
| status | VARCHAR(30) | 游戏状态 |
| priority | VARCHAR(20) | 愿望单优先级 |
| purchase_price | DECIMAL(10,2) | 购买价格 |
| expected_price | DECIMAL(10,2) | 期望价格 |
| rating | DECIMAL(3,1) | 用户评分 |
| playtime_hours | DECIMAL(8,1) | 游玩时长 |
| started_at | DATE | 开始日期 |
| completed_at | DATE | 通关日期 |
| review | TEXT | 用户评价 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

### 7.10 游玩日志表 play_sessions

| 字段名 | 类型 | 说明 |
| --- | --- | --- |
| id | BIGINT | 主键 |
| user_game_id | BIGINT | 用户游戏库 ID |
| played_at | DATE | 游玩日期 |
| duration_hours | DECIMAL(6,1) | 本次游玩时长 |
| progress_note | VARCHAR(255) | 进度说明 |
| note | TEXT | 备注 |
| created_at | DATETIME | 创建时间 |

## 8. 主要 API 规划

### 8.1 认证接口

- `POST /api/auth/register`：用户注册
- `POST /api/auth/login`：用户登录
- `GET /api/auth/me`：获取当前用户
- `PUT /api/auth/me`：修改个人资料

### 8.2 游戏接口

- `GET /api/games`：查询游戏列表
- `POST /api/games`：新增游戏
- `GET /api/games/{id}`：获取游戏详情
- `PUT /api/games/{id}`：修改游戏
- `DELETE /api/games/{id}`：删除游戏

### 8.3 用户游戏库接口

- `GET /api/user-games`：获取我的游戏库
- `POST /api/user-games`：加入游戏库或愿望单
- `GET /api/user-games/{id}`：获取个人游戏详情
- `PUT /api/user-games/{id}`：修改个人游戏记录
- `DELETE /api/user-games/{id}`：删除个人游戏记录

### 8.4 分类、平台、标签接口

- `GET /api/categories`
- `POST /api/categories`
- `PUT /api/categories/{id}`
- `DELETE /api/categories/{id}`
- `GET /api/platforms`
- `POST /api/platforms`
- `PUT /api/platforms/{id}`
- `DELETE /api/platforms/{id}`
- `GET /api/tags`
- `POST /api/tags`
- `PUT /api/tags/{id}`
- `DELETE /api/tags/{id}`

### 8.5 游玩日志接口

- `GET /api/play-sessions`
- `POST /api/play-sessions`
- `PUT /api/play-sessions/{id}`
- `DELETE /api/play-sessions/{id}`

### 8.6 统计接口

- `GET /api/analytics/overview`：概览统计
- `GET /api/analytics/platforms`：平台分布
- `GET /api/analytics/categories`：类型分布
- `GET /api/analytics/monthly-added`：月度新增趋势
- `GET /api/analytics/monthly-playtime`：月度游玩时长趋势

## 9. Docker 环境规划

项目目录建议：

```text
Final_Project/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── main.py
│   ├── alembic/
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   ├── layouts/
│   │   ├── pages/
│   │   ├── stores/
│   │   └── main.tsx
│   ├── package.json
│   └── Dockerfile
├── database/
│   ├── init.sql
│   └── seed.sql
├── docs/
│   ├── requirements.md
│   ├── database-design.md
│   ├── test-cases.md
│   └── report.md
├── docker-compose.yml
├── .env.example
├── README.md
└── plan.md
```

Docker Compose 服务：

- `mysql`：提供 MySQL 数据库。
- `backend`：提供 FastAPI 后端 API。
- `frontend`：提供 React 前端页面。
- `adminer`：提供数据库管理界面。

开发访问地址：

- 前端页面：`http://localhost:5173`
- 后端接口：`http://localhost:8000`
- API 文档：`http://localhost:8000/docs`
- 数据库管理：`http://localhost:8080`
- MySQL：`localhost:3306`

## 10. 测试计划

### 10.1 功能测试

重点测试：

- 用户注册、登录、退出。
- 游戏新增、查询、修改、删除。
- 愿望单添加、状态切换、优先级修改。
- 分类、平台、标签管理。
- 游玩日志添加、修改、删除。
- 统计图表是否正确展示。

### 10.2 数据库测试

重点测试：

- 主键唯一性。
- 用户名和邮箱唯一性。
- 外键约束是否有效。
- 删除数据时是否符合业务规则。
- 查询筛选是否正确。

### 10.3 接口测试

重点测试：

- 正常请求返回正确数据。
- 未登录访问受保护接口会被拒绝。
- 非法参数返回合理错误。
- 删除不存在的数据返回合理提示。

### 10.4 页面测试

重点测试：

- 页面是否能正常加载。
- 表单校验是否生效。
- 搜索和筛选是否可用。
- 图表是否正确渲染。
- 不同屏幕宽度下布局是否正常。

## 11. 示例测试用例

| 编号 | 测试模块 | 测试内容 | 预期结果 |
| --- | --- | --- | --- |
| TC001 | 用户认证 | 使用新用户名注册 | 注册成功并写入用户表 |
| TC002 | 用户认证 | 使用正确账号密码登录 | 返回 JWT Token 并进入首页 |
| TC003 | 游戏管理 | 新增一条游戏记录 | 游戏出现在游戏列表中 |
| TC004 | 游戏管理 | 修改游戏名称和封面 | 详情页展示修改后的信息 |
| TC005 | 游戏管理 | 删除游戏记录 | 列表中不再显示该游戏 |
| TC006 | 愿望单 | 添加高优先级愿望游戏 | 首页高优先级区域显示该游戏 |
| TC007 | 游戏库 | 将游戏状态改为已通关 | 已通关数量统计增加 |
| TC008 | 游玩日志 | 添加一次 2 小时游玩记录 | 总游玩时长增加 2 小时 |
| TC009 | 分类管理 | 新增 RPG 分类 | 分类列表中显示 RPG |
| TC010 | 统计分析 | 查看平台分布图 | 图表按平台正确展示数量 |

## 12. 开发阶段安排

### 阶段一：需求分析与设计

任务：

- 明确系统功能范围。
- 编写需求文档。
- 设计数据库 ER 图和数据字典。
- 确定页面原型和接口列表。

产出：

- `docs/requirements.md`
- `docs/database-design.md`
- `plan.md`

### 阶段二：环境搭建

任务：

- 创建前后端项目结构。
- 编写 Dockerfile 和 docker-compose.yml。
- 配置 MySQL、FastAPI、React。
- 准备初始数据。

产出：

- 可一键启动的开发环境。

### 阶段三：后端开发

任务：

- 实现数据库模型。
- 实现用户认证。
- 实现游戏、分类、平台、标签、愿望单、游戏库、游玩日志接口。
- 实现统计分析接口。

产出：

- 完整 RESTful API。
- Swagger 接口文档。

### 阶段四：前端开发

任务：

- 实现登录注册页面。
- 实现首页仪表盘。
- 实现游戏列表、详情、添加、编辑页面。
- 实现分类、平台、标签管理页面。
- 实现统计分析图表页面。
- 完成高级视觉样式。

产出：

- 可演示的完整 Web 页面。

### 阶段五：测试与文档

任务：

- 编写测试用例。
- 执行功能测试。
- 编写实验报告。
- 准备演示 PPT。

产出：

- `docs/test-cases.md`
- `docs/report.md`
- 演示 PPT 内容大纲

## 13. 演示流程建议

课堂演示可以按以下顺序：

1. 展示系统首页和整体视觉效果。
2. 注册并登录用户。
3. 新增一款游戏，例如《Elden Ring》。
4. 给游戏添加平台、类型和标签。
5. 将游戏加入愿望单，设置高优先级和期望价格。
6. 修改状态为正在玩，添加游玩日志。
7. 修改状态为已通关，填写评分和评价。
8. 展示游戏详情页。
9. 展示分类筛选和搜索功能。
10. 展示统计分析图表。
11. 展示数据库中对应表的数据变化。

## 14. 项目亮点

1. 题目有个性，区别于常见的记账、库存、图书管理系统。
2. 数据库关系较完整，包含一对多、多对多、用户私有数据和统计分析。
3. 技术栈现代，FastAPI + React + MySQL 适合展示全栈能力。
4. Docker 一键启动，降低环境配置难度。
5. 页面视觉效果适合展示，容易在答辩中获得好印象。
6. 统计分析功能能体现数据库查询和数据聚合能力。

## 15. 最小可行版本范围

如果时间紧张，优先完成以下功能：

1. 用户注册登录。
2. 游戏信息增删改查。
3. 我的游戏库和愿望单管理。
4. 分类、平台、标签基础管理。
5. 首页搜索和统计卡片。
6. 游戏详情页。
7. 基础统计图表。
8. Docker Compose 一键启动。

增强功能可以放在后续：

1. 管理员后台。
2. 游戏推荐。
3. 更复杂的消费趋势分析。
4. 第三方游戏 API 数据导入。
5. 图片上传。

