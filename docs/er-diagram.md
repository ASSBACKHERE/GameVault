# GameVault ER 图与关系说明

## ER 图

```mermaid
erDiagram
    users ||--o{ user_games : owns
    games ||--o{ user_games : collected_as
    user_games ||--o{ play_sessions : has
    games ||--o{ game_platforms : maps
    platforms ||--o{ game_platforms : maps
    games ||--o{ game_categories : maps
    categories ||--o{ game_categories : maps
    games ||--o{ game_tags : maps
    tags ||--o{ game_tags : maps

    users {
        bigint id PK
        varchar username UK
        varchar email UK
        varchar password_hash
        varchar nickname
        varchar role
    }

    games {
        bigint id PK
        varchar title
        varchar cover_url
        varchar developer
        varchar publisher
        date release_date
        text description
    }

    user_games {
        bigint id PK
        bigint user_id FK
        bigint game_id FK
        varchar status
        varchar priority
        decimal purchase_price
        decimal expected_price
        decimal rating
        decimal playtime_hours
    }

    play_sessions {
        bigint id PK
        bigint user_game_id FK
        date played_at
        decimal duration_hours
        varchar progress_note
    }
```

## 关系说明

- 用户和个人游戏库是一对多关系。
- 游戏和个人游戏库是一对多关系，同一游戏可被多个用户收藏。
- 游戏和平台、类型、标签是多对多关系，通过关联表实现。
- 个人游戏库和游玩日志是一对多关系。
- `user_games` 使用 `user_id + game_id` 联合唯一约束，防止同一用户重复添加同一游戏。
