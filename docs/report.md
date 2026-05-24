# GameVault 实验报告

## 1. 实验目的

本实验通过开发 GameVault 游戏愿望单与游玩进度分析系统，掌握 Web 应用系统的需求分析、数据库设计、后端接口开发、前端页面开发、数据库连接和功能测试流程。

## 2. 实验环境

- 操作系统：Windows、macOS 或 Linux
- 数据库：MySQL 8.0
- 后端：Python 3.12、FastAPI、SQLAlchemy
- 前端：React、Vite、TypeScript、Ant Design、ECharts
- 容器：Docker Compose

## 3. 系统功能

系统实现了用户注册登录、游戏信息管理、游戏详情查看、游戏记录编辑、个人游戏库管理、愿望单管理、平台类型标签管理、游玩日志管理、状态更新、个人资料维护、统计卡片、分布图和趋势图分析等功能。

## 4. 数据库设计

系统包含 `users`、`games`、`platforms`、`categories`、`tags`、`game_platforms`、`game_categories`、`game_tags`、`user_games`、`play_sessions` 等数据表，覆盖一对多和多对多关系。

## 5. 实验结果

通过 Docker Compose 可以一键启动系统。用户登录后可以新增和编辑游戏、设置游戏状态、维护分类数据、添加游玩日志、查看统计结果，并可通过 Adminer 观察 MySQL 数据变化。

## 6. 实验结论

本项目完成了一个具有完整数据库支撑的 Web 应用系统，满足课程对数据增删改查、逻辑展示、数据库设计和现场演示的要求。
