# GameVault

GameVault 是一个基于 Python、MySQL 和 React 的游戏愿望单与游玩进度分析系统，适合作为数据库系统课程期末 Web 应用大作业。

## 技术栈

- 后端：FastAPI、SQLAlchemy、MySQL、HMAC Token
- 前端：React、Vite、TypeScript、Ant Design、ECharts
- 环境：Docker Compose、MySQL 8、Adminer

## 一键启动

```bash
docker compose up --build
```

启动后访问：

- 前端页面：http://localhost:5173
- 后端接口：http://localhost:8000
- API 文档：http://localhost:8000/docs
- 数据库管理：http://localhost:8080

演示账号：

- 用户名：`demo`
- 密码：`demo123456`

Adminer 登录信息：

- System：`MySQL`
- Server：`mysql`
- Username：`gamevault`
- Password：`gamevault`
- Database：`gamevault`

## 核心功能

- 用户注册、登录和 JWT 身份验证
- 游戏信息增删改查
- 我的游戏库和愿望单管理
- 游戏详情查看和游戏记录编辑
- 游戏状态管理：想玩、已购买、正在玩、已通关、已搁置、已放弃
- 平台、类型、标签分类展示、新增和删除
- 游玩时长、评分、购买价格、个人评价记录
- 游玩日志添加、查看和删除
- 个人资料查看和修改
- 首页搜索、状态筛选、统计卡片、平台分布图、类型分布图、状态分布图
- 月度新增游戏趋势和月度游玩时长趋势
- MySQL 数据持久化和 Docker 一键环境

## 测试覆盖率

后端使用 `pytest` 和 `pytest-cov` 进行接口测试与覆盖率统计。

```bash
cd backend
python3.11 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python -m pytest
```

当前后端覆盖率：`94.64%`。

## 项目结构

```text
Final_Project/
├── backend/
│   ├── app/main.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/main.tsx
│   ├── src/styles.css
│   ├── package.json
│   └── Dockerfile
├── database/init.sql
├── docs/
├── docker-compose.yml
├── plan.md
└── README.md
```

## 课堂演示建议

1. 使用演示账号登录系统。
2. 展示首页统计卡片、愿望单、平台/类型/状态图表。
3. 在游戏库中搜索、筛选、查看详情、编辑游戏记录。
4. 新增一款游戏，选择平台、类型和标签。
5. 修改游戏状态，例如从愿望单改为正在玩或已通关。
6. 添加一条游玩日志，观察总游玩时长变化。
7. 新增或删除平台、类型、标签。
8. 展示统计分析页面中的趋势图。
9. 修改个人资料。
10. 打开 Adminer 查看 MySQL 中的数据表和记录变化。
