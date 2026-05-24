# 数据库展示说明

## 展示工具

访问 `http://localhost:8080` 打开 Adminer。

登录信息：

- System：MySQL
- Server：mysql
- Username：gamevault
- Password：gamevault
- Database：gamevault

## 建议展示顺序

1. 打开 `users` 表，展示 demo 用户。
2. 打开 `games` 表，展示游戏基础信息和封面地址。
3. 打开 `user_games` 表，展示用户与游戏的个人状态、价格、评分和时长。
4. 打开 `platforms`、`categories`、`tags` 表，展示分类数据。
5. 打开 `game_platforms`、`game_categories`、`game_tags` 表，展示多对多关系。
6. 在系统页面添加一条游玩日志。
7. 回到 Adminer 打开 `play_sessions` 表，展示新增记录。
8. 回到系统页面查看统计卡片和趋势图变化。

## 重点讲解

- `user_games` 是核心业务表，连接用户和游戏。
- 关联表体现了数据库多对多关系设计。
- 外键约束保证了数据之间的引用完整性。
- 统计接口基于聚合查询实现图表展示。
