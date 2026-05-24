# GameVault 数据库设计

## 1. 设计目标

数据库用于保存用户、游戏、平台、类型、标签、个人游戏库和游玩日志数据。设计重点是保证实体完整性、参照完整性和多对多关系的正确表达。

## 2. 主要数据表

### users

保存用户登录和个人资料信息。

关键字段：`id`、`username`、`email`、`password_hash`、`nickname`、`role`。

### games

保存游戏基础信息。

关键字段：`id`、`title`、`cover_url`、`developer`、`publisher`、`release_date`、`description`、`created_by`。

### platforms

保存游戏平台，例如 Steam、Epic、PlayStation、Switch。

### categories

保存游戏类型，例如 RPG、ACT、AVG、SLG、独立游戏。

### tags

保存游戏标签，例如 开放世界、剧情向、高难度、多人合作。

### game_platforms

游戏与平台的多对多关联表。

### game_categories

游戏与类型的多对多关联表。

### game_tags

游戏与标签的多对多关联表。

### user_games

保存用户个人游戏库数据，是系统核心业务表。

关键字段：`user_id`、`game_id`、`status`、`priority`、`purchase_price`、`expected_price`、`rating`、`playtime_hours`、`review`。

### play_sessions

保存单次游玩日志。

关键字段：`user_game_id`、`played_at`、`duration_hours`、`progress_note`、`note`。

## 3. 表关系

- 一个用户可以拥有多条个人游戏库记录。
- 一个游戏可以被多个用户加入个人游戏库。
- 一个游戏可以属于多个平台、多个类型和多个标签。
- 一个个人游戏库记录可以拥有多条游玩日志。

## 4. 完整性约束

- `users.username` 和 `users.email` 唯一。
- `user_games` 对 `user_id` 和 `game_id` 设置联合唯一约束，避免同一用户重复加入同一游戏。
- 关联表使用联合主键避免重复关联。
- 外键保证用户、游戏、分类、平台、标签和日志之间的引用关系。
