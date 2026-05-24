from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
from decimal import Decimal
import base64
import hashlib
import hmac
import json
import os
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, ConfigDict
from sqlalchemy import (
    Date,
    DateTime,
    DECIMAL,
    ForeignKey,
    String,
    Text,
    UniqueConstraint,
    create_engine,
    func,
    select,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship, sessionmaker


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://gamevault:gamevault@localhost:3306/gamevault?charset=utf8mb4",
)
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))
CORS_ORIGINS = [origin.strip() for origin in os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")]

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    nickname: Mapped[str | None] = mapped_column(String(50), default=None)
    avatar_url: Mapped[str | None] = mapped_column(String(255), default=None)
    bio: Mapped[str | None] = mapped_column(Text, default=None)
    role: Mapped[str] = mapped_column(String(20), default="user")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    games: Mapped[list["UserGame"]] = relationship(back_populates="user", cascade="all, delete-orphan")


class Game(Base):
    __tablename__ = "games"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(120), index=True)
    original_title: Mapped[str | None] = mapped_column(String(120), default=None)
    cover_url: Mapped[str | None] = mapped_column(String(500), default=None)
    developer: Mapped[str | None] = mapped_column(String(120), default=None)
    publisher: Mapped[str | None] = mapped_column(String(120), default=None)
    release_date: Mapped[date | None] = mapped_column(Date, default=None)
    description: Mapped[str | None] = mapped_column(Text, default=None)
    created_by: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    platforms: Mapped[list["GamePlatform"]] = relationship(back_populates="game", cascade="all, delete-orphan")
    categories: Mapped[list["GameCategory"]] = relationship(back_populates="game", cascade="all, delete-orphan")
    tags: Mapped[list["GameTag"]] = relationship(back_populates="game", cascade="all, delete-orphan")
    user_games: Mapped[list["UserGame"]] = relationship(back_populates="game", cascade="all, delete-orphan")


class Platform(Base):
    __tablename__ = "platforms"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(80), unique=True)
    icon: Mapped[str | None] = mapped_column(String(80), default=None)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    games: Mapped[list["GamePlatform"]] = relationship(back_populates="platform", cascade="all, delete-orphan")


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(80), unique=True)
    description: Mapped[str | None] = mapped_column(Text, default=None)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    games: Mapped[list["GameCategory"]] = relationship(back_populates="category", cascade="all, delete-orphan")


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(80), unique=True)
    color: Mapped[str | None] = mapped_column(String(20), default="#7C3AED")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    games: Mapped[list["GameTag"]] = relationship(back_populates="tag", cascade="all, delete-orphan")


class GamePlatform(Base):
    __tablename__ = "game_platforms"
    __table_args__ = (UniqueConstraint("game_id", "platform_id"),)

    game_id: Mapped[int] = mapped_column(ForeignKey("games.id"), primary_key=True)
    platform_id: Mapped[int] = mapped_column(ForeignKey("platforms.id"), primary_key=True)

    game: Mapped[Game] = relationship(back_populates="platforms")
    platform: Mapped[Platform] = relationship(back_populates="games")


class GameCategory(Base):
    __tablename__ = "game_categories"
    __table_args__ = (UniqueConstraint("game_id", "category_id"),)

    game_id: Mapped[int] = mapped_column(ForeignKey("games.id"), primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), primary_key=True)

    game: Mapped[Game] = relationship(back_populates="categories")
    category: Mapped[Category] = relationship(back_populates="games")


class GameTag(Base):
    __tablename__ = "game_tags"
    __table_args__ = (UniqueConstraint("game_id", "tag_id"),)

    game_id: Mapped[int] = mapped_column(ForeignKey("games.id"), primary_key=True)
    tag_id: Mapped[int] = mapped_column(ForeignKey("tags.id"), primary_key=True)

    game: Mapped[Game] = relationship(back_populates="tags")
    tag: Mapped[Tag] = relationship(back_populates="games")


class UserGame(Base):
    __tablename__ = "user_games"
    __table_args__ = (UniqueConstraint("user_id", "game_id"),)

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    game_id: Mapped[int] = mapped_column(ForeignKey("games.id"), index=True)
    status: Mapped[str] = mapped_column(String(30), default="wishlist", index=True)
    priority: Mapped[str] = mapped_column(String(20), default="medium")
    purchase_price: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), default=0)
    expected_price: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), default=0)
    rating: Mapped[Decimal | None] = mapped_column(DECIMAL(3, 1), default=None)
    playtime_hours: Mapped[Decimal] = mapped_column(DECIMAL(8, 1), default=0)
    started_at: Mapped[date | None] = mapped_column(Date, default=None)
    completed_at: Mapped[date | None] = mapped_column(Date, default=None)
    review: Mapped[str | None] = mapped_column(Text, default=None)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user: Mapped[User] = relationship(back_populates="games")
    game: Mapped[Game] = relationship(back_populates="user_games")
    sessions: Mapped[list["PlaySession"]] = relationship(back_populates="user_game", cascade="all, delete-orphan")


class PlaySession(Base):
    __tablename__ = "play_sessions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_game_id: Mapped[int] = mapped_column(ForeignKey("user_games.id"), index=True)
    played_at: Mapped[date] = mapped_column(Date)
    duration_hours: Mapped[Decimal] = mapped_column(DECIMAL(6, 1), default=0)
    progress_note: Mapped[str | None] = mapped_column(String(255), default=None)
    note: Mapped[str | None] = mapped_column(Text, default=None)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user_game: Mapped[UserGame] = relationship(back_populates="sessions")


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: "UserOut"


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    nickname: str | None = None


class UserLogin(BaseModel):
    username: str
    password: str


class UserUpdate(BaseModel):
    nickname: str | None = None
    avatar_url: str | None = None
    bio: str | None = None


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: str
    nickname: str | None
    avatar_url: str | None
    bio: str | None
    role: str


class LookupCreate(BaseModel):
    name: str
    description: str | None = None
    icon: str | None = None
    color: str | None = None


class LookupOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None = None
    icon: str | None = None
    color: str | None = None


class GameCreate(BaseModel):
    title: str
    original_title: str | None = None
    cover_url: str | None = None
    developer: str | None = None
    publisher: str | None = None
    release_date: date | None = None
    description: str | None = None
    platform_ids: list[int] = []
    category_ids: list[int] = []
    tag_ids: list[int] = []


class GameUpdate(GameCreate):
    pass


class GameOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    original_title: str | None
    cover_url: str | None
    developer: str | None
    publisher: str | None
    release_date: date | None
    description: str | None
    platforms: list[LookupOut]
    categories: list[LookupOut]
    tags: list[LookupOut]


class UserGameCreate(BaseModel):
    game_id: int
    status: str = "wishlist"
    priority: str = "medium"
    purchase_price: Decimal = Decimal("0")
    expected_price: Decimal = Decimal("0")
    rating: Decimal | None = None
    playtime_hours: Decimal = Decimal("0")
    started_at: date | None = None
    completed_at: date | None = None
    review: str | None = None


class UserGameUpdate(BaseModel):
    status: str | None = None
    priority: str | None = None
    purchase_price: Decimal | None = None
    expected_price: Decimal | None = None
    rating: Decimal | None = None
    playtime_hours: Decimal | None = None
    started_at: date | None = None
    completed_at: date | None = None
    review: str | None = None


class UserGameOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    status: str
    priority: str
    purchase_price: Decimal
    expected_price: Decimal
    rating: Decimal | None
    playtime_hours: Decimal
    started_at: date | None
    completed_at: date | None
    review: str | None
    created_at: datetime
    game: GameOut


class PlaySessionCreate(BaseModel):
    user_game_id: int
    played_at: date
    duration_hours: Decimal
    progress_note: str | None = None
    note: str | None = None


class PlaySessionUpdate(BaseModel):
    played_at: date | None = None
    duration_hours: Decimal | None = None
    progress_note: str | None = None
    note: str | None = None


class PlaySessionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_game_id: int
    played_at: date
    duration_hours: Decimal
    progress_note: str | None
    note: str | None


class OverviewOut(BaseModel):
    total_games: int
    wishlist_count: int
    playing_count: int
    completed_count: int
    purchased_count: int
    total_spent: Decimal
    total_playtime: Decimal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


Db = Annotated[Session, Depends(get_db)]


def verify_password(plain_password: str, password_hash: str) -> bool:
    return hmac.compare_digest(hash_password(plain_password), password_hash)


def hash_password(password: str) -> str:
    salt = SECRET_KEY.encode("utf-8")
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 120000).hex()


def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("utf-8")


def _b64url_decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


def create_access_token(subject: str) -> str:
    header = {"alg": ALGORITHM, "typ": "JWT"}
    expire = int((datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)).timestamp())
    payload = {"sub": subject, "exp": expire}
    signing_input = ".".join([
        _b64url_encode(json.dumps(header, separators=(",", ":")).encode("utf-8")),
        _b64url_encode(json.dumps(payload, separators=(",", ":")).encode("utf-8")),
    ])
    signature = hmac.new(SECRET_KEY.encode("utf-8"), signing_input.encode("utf-8"), hashlib.sha256).digest()
    return f"{signing_input}.{_b64url_encode(signature)}"


def decode_access_token(token: str) -> dict:
    header_part, payload_part, signature_part = token.split(".")
    signing_input = f"{header_part}.{payload_part}"
    expected_signature = _b64url_encode(
        hmac.new(SECRET_KEY.encode("utf-8"), signing_input.encode("utf-8"), hashlib.sha256).digest()
    )
    if not hmac.compare_digest(signature_part, expected_signature):
        raise ValueError("invalid signature")
    payload = json.loads(_b64url_decode(payload_part))
    if int(payload.get("exp", 0)) < int(datetime.now(timezone.utc).timestamp()):
        raise ValueError("token expired")
    return payload


def current_user(db: Db, token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="登录已过期，请重新登录",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        user_id = int(payload.get("sub"))
    except (TypeError, ValueError):
        raise credentials_error
    user = db.get(User, user_id)
    if not user:
        raise credentials_error
    return user


CurrentUser = Annotated[User, Depends(current_user)]


def lookup_out(item) -> LookupOut:
    return LookupOut(
        id=item.id,
        name=item.name,
        description=getattr(item, "description", None),
        icon=getattr(item, "icon", None),
        color=getattr(item, "color", None),
    )


def serialize_game(game: Game) -> GameOut:
    return GameOut(
        id=game.id,
        title=game.title,
        original_title=game.original_title,
        cover_url=game.cover_url,
        developer=game.developer,
        publisher=game.publisher,
        release_date=game.release_date,
        description=game.description,
        platforms=[lookup_out(link.platform) for link in game.platforms],
        categories=[lookup_out(link.category) for link in game.categories],
        tags=[lookup_out(link.tag) for link in game.tags],
    )


def serialize_user_game(item: UserGame) -> UserGameOut:
    return UserGameOut(
        id=item.id,
        status=item.status,
        priority=item.priority,
        purchase_price=item.purchase_price,
        expected_price=item.expected_price,
        rating=item.rating,
        playtime_hours=item.playtime_hours,
        started_at=item.started_at,
        completed_at=item.completed_at,
        review=item.review,
        created_at=item.created_at,
        game=serialize_game(item.game),
    )


def sync_game_links(db: Session, game: Game, data: GameCreate) -> None:
    game.platforms.clear()
    game.categories.clear()
    game.tags.clear()
    db.flush()
    for platform_id in data.platform_ids:
        if db.get(Platform, platform_id):
            game.platforms.append(GamePlatform(platform_id=platform_id))
    for category_id in data.category_ids:
        if db.get(Category, category_id):
            game.categories.append(GameCategory(category_id=category_id))
    for tag_id in data.tag_ids:
        if db.get(Tag, tag_id):
            game.tags.append(GameTag(tag_id=tag_id))


def seed_data(db: Session) -> None:
    demo = db.scalar(select(User).where(User.username == "demo"))
    if not demo:
        demo = User(
            username="demo",
            email="demo@gamevault.local",
            password_hash=hash_password("demo123456"),
            nickname="Demo 玩家",
            bio="欢迎来到 GameVault。",
        )
        db.add(demo)
        db.flush()

    platform_specs = [
        ("Steam", "desktop"),
        ("Epic", "thunderbolt"),
        ("PlayStation", "crown"),
        ("Switch", "rocket"),
        ("PC", "code"),
        ("Xbox", "appstore"),
    ]
    category_specs = [
        ("RPG", "角色扮演与成长体验"),
        ("ACT", "动作与操作挑战"),
        ("AVG", "剧情冒险与叙事"),
        ("SLG", "策略规划与资源管理"),
        ("独立游戏", "创意驱动的小体量作品"),
        ("FPS", "第一人称射击与战术对抗"),
        ("SIM", "模拟经营与生活体验"),
    ]
    tag_specs = [
        ("开放世界", "#22C55E"),
        ("剧情向", "#60A5FA"),
        ("高难度", "#F97316"),
        ("多人合作", "#A78BFA"),
        ("像素风", "#FACC15"),
        ("科幻", "#38BDF8"),
        ("治愈", "#34D399"),
        ("探索", "#818CF8"),
    ]

    platforms = {}
    for name, icon in platform_specs:
        item = db.scalar(select(Platform).where(Platform.name == name))
        if not item:
            item = Platform(name=name, icon=icon)
            db.add(item)
            db.flush()
        platforms[name] = item

    categories = {}
    for name, description in category_specs:
        item = db.scalar(select(Category).where(Category.name == name))
        if not item:
            item = Category(name=name, description=description)
            db.add(item)
            db.flush()
        categories[name] = item

    tags = {}
    for name, color in tag_specs:
        item = db.scalar(select(Tag).where(Tag.name == name))
        if not item:
            item = Tag(name=name, color=color)
            db.add(item)
            db.flush()
        tags[name] = item

    game_specs = [
        ("Elden Ring", "ELDEN RING", "https://cdn.akamai.steamstatic.com/steam/apps/1245620/header.jpg", "FromSoftware", "Bandai Namco", date(2022, 2, 25), "辽阔开放世界与高难度战斗结合的奇幻动作 RPG。", ["Steam", "PlayStation"], ["RPG", "ACT"], ["开放世界", "高难度", "探索"], "playing", "high", "298", "0", "9.5", "46.5"),
        ("Hades", "Hades", "https://cdn.akamai.steamstatic.com/steam/apps/1145360/header.jpg", "Supergiant Games", "Supergiant Games", date(2020, 9, 17), "快节奏肉鸽动作游戏，拥有优秀叙事与美术风格。", ["Steam", "Switch"], ["ACT", "独立游戏"], ["高难度", "剧情向"], "completed", "medium", "80", "0", "9.0", "32.0"),
        ("Stardew Valley", "Stardew Valley", "https://cdn.akamai.steamstatic.com/steam/apps/413150/header.jpg", "ConcernedApe", "ConcernedApe", date(2016, 2, 26), "轻松治愈的农场经营与社区生活模拟游戏。", ["Steam", "Switch"], ["SIM", "独立游戏"], ["像素风", "治愈"], "wishlist", "high", "0", "28", None, "0"),
        ("Cyberpunk 2077", "Cyberpunk 2077", "https://cdn.akamai.steamstatic.com/steam/apps/1091500/header.jpg", "CD Projekt Red", "CD Projekt", date(2020, 12, 10), "霓虹都市、角色成长与开放世界叙事结合的科幻 RPG。", ["Steam", "PlayStation", "Xbox"], ["RPG"], ["开放世界", "剧情向", "科幻"], "playing", "high", "198", "0", "8.8", "24.0"),
        ("Celeste", "Celeste", "https://cdn.akamai.steamstatic.com/steam/apps/504230/header.jpg", "Maddy Makes Games", "Maddy Makes Games", date(2018, 1, 25), "高难度平台跳跃和自我成长主题结合的独立游戏。", ["Steam", "Switch"], ["ACT", "独立游戏"], ["像素风", "高难度"], "completed", "medium", "48", "0", "9.2", "18.5"),
        ("The Witcher 3", "The Witcher 3: Wild Hunt", "https://cdn.akamai.steamstatic.com/steam/apps/292030/header.jpg", "CD Projekt Red", "CD Projekt", date(2015, 5, 19), "开放世界奇幻 RPG，以剧情任务和角色塑造见长。", ["Steam", "PlayStation", "Switch"], ["RPG"], ["开放世界", "剧情向"], "completed", "high", "128", "0", "9.7", "86.0"),
        ("Hollow Knight", "Hollow Knight", "https://cdn.akamai.steamstatic.com/steam/apps/367520/header.jpg", "Team Cherry", "Team Cherry", date(2017, 2, 24), "地下王国探索、动作战斗与精致关卡设计。", ["Steam", "Switch"], ["ACT", "独立游戏"], ["探索", "高难度"], "paused", "medium", "48", "0", "8.9", "21.5"),
        ("Baldur's Gate 3", "Baldur's Gate 3", "https://cdn.akamai.steamstatic.com/steam/apps/1086940/header.jpg", "Larian Studios", "Larian Studios", date(2023, 8, 3), "高自由度队伍冒险与回合制策略 RPG。", ["Steam", "PlayStation"], ["RPG", "SLG"], ["剧情向", "多人合作"], "wishlist", "high", "0", "238", None, "0"),
        ("DOOM Eternal", "DOOM Eternal", "https://cdn.akamai.steamstatic.com/steam/apps/782330/header.jpg", "id Software", "Bethesda", date(2020, 3, 20), "高速战斗、资源循环和强烈节奏感的 FPS。", ["Steam", "Xbox", "PlayStation"], ["FPS", "ACT"], ["高难度", "科幻"], "purchased", "medium", "99", "0", "8.6", "12.0"),
        ("Disco Elysium", "Disco Elysium", "https://cdn.akamai.steamstatic.com/steam/apps/632470/header.jpg", "ZA/UM", "ZA/UM", date(2019, 10, 15), "文字驱动的侦探 RPG，强调选择、心理和叙事。", ["Steam"], ["RPG", "AVG"], ["剧情向", "探索"], "wishlist", "medium", "0", "58", None, "0"),
        ("No Man's Sky", "No Man's Sky", "https://cdn.akamai.steamstatic.com/steam/apps/275850/header.jpg", "Hello Games", "Hello Games", date(2016, 8, 12), "宇宙探索、生存建造与持续更新的科幻冒险。", ["Steam", "PlayStation", "Xbox"], ["AVG", "SIM"], ["开放世界", "科幻", "探索"], "playing", "low", "120", "0", "8.1", "15.0"),
        ("Animal Crossing", "Animal Crossing: New Horizons", "https://images.igdb.com/igdb/image/upload/t_cover_big/co3wls.jpg", "Nintendo", "Nintendo", date(2020, 3, 20), "岛屿生活、装饰收集和轻松社交的治愈模拟游戏。", ["Switch"], ["SIM"], ["治愈", "多人合作"], "completed", "medium", "299", "0", "8.7", "64.0"),
    ]

    for spec in game_specs:
        title, original_title, cover_url, developer, publisher, release_date, description, platform_names, category_names, tag_names, status_value, priority, purchase_price, expected_price, rating, playtime = spec
        game = db.scalar(select(Game).where(Game.title == title))
        if not game:
            game = Game(
                title=title,
                original_title=original_title,
                cover_url=cover_url,
                developer=developer,
                publisher=publisher,
                release_date=release_date,
                description=description,
                created_by=demo.id,
            )
            db.add(game)
            db.flush()
        else:
            game.original_title = original_title
            game.cover_url = cover_url
            game.developer = developer
            game.publisher = publisher
            game.release_date = release_date
            game.description = description
        if not game.platforms:
            game.platforms.extend([GamePlatform(platform_id=platforms[name].id) for name in platform_names])
        if not game.categories:
            game.categories.extend([GameCategory(category_id=categories[name].id) for name in category_names])
        if not game.tags:
            game.tags.extend([GameTag(tag_id=tags[name].id) for name in tag_names])

        user_game = db.scalar(select(UserGame).where(UserGame.user_id == demo.id, UserGame.game_id == game.id))
        if not user_game:
            db.add(UserGame(
                user_id=demo.id,
                game_id=game.id,
                status=status_value,
                priority=priority,
                purchase_price=Decimal(purchase_price),
                expected_price=Decimal(expected_price),
                rating=Decimal(rating) if rating else None,
                playtime_hours=Decimal(playtime),
                completed_at=date(2024, 8, 12) if status_value == "completed" else None,
                review="这条记录用于展示游戏库、愿望单和统计分析效果。",
            ))
    db.commit()


app = FastAPI(title="GameVault API", description="游戏愿望单与游玩进度分析系统", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        seed_data(db)


@app.get("/api/health")
def health():
    return {"status": "ok", "name": "GameVault"}


@app.post("/api/auth/register", response_model=TokenOut)
def register(data: UserCreate, db: Db):
    exists = db.scalar(select(User).where((User.username == data.username) | (User.email == data.email)))
    if exists:
        raise HTTPException(status_code=400, detail="用户名或邮箱已存在")
    user = User(
        username=data.username,
        email=data.email,
        password_hash=hash_password(data.password),
        nickname=data.nickname or data.username,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return TokenOut(access_token=create_access_token(str(user.id)), user=UserOut.model_validate(user))


@app.post("/api/auth/login", response_model=TokenOut)
def login(data: UserLogin, db: Db):
    user = db.scalar(select(User).where(User.username == data.username))
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="用户名或密码错误")
    return TokenOut(access_token=create_access_token(str(user.id)), user=UserOut.model_validate(user))


@app.get("/api/auth/me", response_model=UserOut)
def me(user: CurrentUser):
    return user


@app.put("/api/auth/me", response_model=UserOut)
def update_me(data: UserUpdate, db: Db, user: CurrentUser):
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user


@app.get("/api/games", response_model=list[GameOut])
def list_games(db: Db, q: str | None = None):
    stmt = select(Game).order_by(Game.created_at.desc())
    if q:
        stmt = stmt.where(Game.title.like(f"%{q}%"))
    return [serialize_game(game) for game in db.scalars(stmt).unique().all()]


@app.post("/api/games", response_model=GameOut)
def create_game(data: GameCreate, db: Db, user: CurrentUser):
    game = Game(**data.model_dump(exclude={"platform_ids", "category_ids", "tag_ids"}), created_by=user.id)
    db.add(game)
    db.flush()
    sync_game_links(db, game, data)
    db.commit()
    db.refresh(game)
    return serialize_game(game)


@app.get("/api/games/{game_id}", response_model=GameOut)
def get_game(game_id: int, db: Db):
    game = db.get(Game, game_id)
    if not game:
        raise HTTPException(status_code=404, detail="游戏不存在")
    return serialize_game(game)


@app.put("/api/games/{game_id}", response_model=GameOut)
def update_game(game_id: int, data: GameUpdate, db: Db, user: CurrentUser):
    game = db.get(Game, game_id)
    if not game:
        raise HTTPException(status_code=404, detail="游戏不存在")
    for field, value in data.model_dump(exclude={"platform_ids", "category_ids", "tag_ids"}).items():
        setattr(game, field, value)
    sync_game_links(db, game, data)
    db.commit()
    db.refresh(game)
    return serialize_game(game)


@app.delete("/api/games/{game_id}")
def delete_game(game_id: int, db: Db, user: CurrentUser):
    game = db.get(Game, game_id)
    if not game:
        raise HTTPException(status_code=404, detail="游戏不存在")
    db.delete(game)
    db.commit()
    return {"message": "删除成功"}


def list_lookup(db: Session, model):
    return [lookup_out(item) for item in db.scalars(select(model).order_by(model.name)).all()]


@app.get("/api/platforms", response_model=list[LookupOut])
def platforms(db: Db):
    return list_lookup(db, Platform)


@app.post("/api/platforms", response_model=LookupOut)
def create_platform(data: LookupCreate, db: Db, user: CurrentUser):
    item = Platform(name=data.name, icon=data.icon)
    db.add(item)
    db.commit()
    db.refresh(item)
    return lookup_out(item)


@app.put("/api/platforms/{item_id}", response_model=LookupOut)
def update_platform(item_id: int, data: LookupCreate, db: Db, user: CurrentUser):
    item = db.get(Platform, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="平台不存在")
    item.name = data.name
    item.icon = data.icon
    db.commit()
    db.refresh(item)
    return lookup_out(item)


@app.delete("/api/platforms/{item_id}")
def delete_platform(item_id: int, db: Db, user: CurrentUser):
    item = db.get(Platform, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="平台不存在")
    if item.games:
        raise HTTPException(status_code=400, detail="该平台已关联游戏，不能直接删除")
    db.delete(item)
    db.commit()
    return {"message": "删除成功"}


@app.get("/api/categories", response_model=list[LookupOut])
def categories(db: Db):
    return list_lookup(db, Category)


@app.post("/api/categories", response_model=LookupOut)
def create_category(data: LookupCreate, db: Db, user: CurrentUser):
    item = Category(name=data.name, description=data.description)
    db.add(item)
    db.commit()
    db.refresh(item)
    return lookup_out(item)


@app.put("/api/categories/{item_id}", response_model=LookupOut)
def update_category(item_id: int, data: LookupCreate, db: Db, user: CurrentUser):
    item = db.get(Category, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="类型不存在")
    item.name = data.name
    item.description = data.description
    db.commit()
    db.refresh(item)
    return lookup_out(item)


@app.delete("/api/categories/{item_id}")
def delete_category(item_id: int, db: Db, user: CurrentUser):
    item = db.get(Category, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="类型不存在")
    if item.games:
        raise HTTPException(status_code=400, detail="该类型已关联游戏，不能直接删除")
    db.delete(item)
    db.commit()
    return {"message": "删除成功"}


@app.get("/api/tags", response_model=list[LookupOut])
def tags(db: Db):
    return list_lookup(db, Tag)


@app.post("/api/tags", response_model=LookupOut)
def create_tag(data: LookupCreate, db: Db, user: CurrentUser):
    item = Tag(name=data.name, color=data.color or "#7C3AED")
    db.add(item)
    db.commit()
    db.refresh(item)
    return lookup_out(item)


@app.put("/api/tags/{item_id}", response_model=LookupOut)
def update_tag(item_id: int, data: LookupCreate, db: Db, user: CurrentUser):
    item = db.get(Tag, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="标签不存在")
    item.name = data.name
    item.color = data.color or item.color
    db.commit()
    db.refresh(item)
    return lookup_out(item)


@app.delete("/api/tags/{item_id}")
def delete_tag(item_id: int, db: Db, user: CurrentUser):
    item = db.get(Tag, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="标签不存在")
    if item.games:
        raise HTTPException(status_code=400, detail="该标签已关联游戏，不能直接删除")
    db.delete(item)
    db.commit()
    return {"message": "删除成功"}


@app.get("/api/user-games", response_model=list[UserGameOut])
def list_user_games(
    db: Db,
    user: CurrentUser,
    status_filter: Annotated[str | None, Query(alias="status")] = None,
    q: str | None = None,
):
    stmt = select(UserGame).join(Game).where(UserGame.user_id == user.id).order_by(UserGame.updated_at.desc())
    if status_filter:
        stmt = stmt.where(UserGame.status == status_filter)
    if q:
        stmt = stmt.where(Game.title.like(f"%{q}%"))
    return [serialize_user_game(item) for item in db.scalars(stmt).unique().all()]


@app.post("/api/user-games", response_model=UserGameOut)
def create_user_game(data: UserGameCreate, db: Db, user: CurrentUser):
    if not db.get(Game, data.game_id):
        raise HTTPException(status_code=404, detail="游戏不存在")
    exists = db.scalar(select(UserGame).where(UserGame.user_id == user.id, UserGame.game_id == data.game_id))
    if exists:
        raise HTTPException(status_code=400, detail="该游戏已在你的库中")
    item = UserGame(**data.model_dump(), user_id=user.id)
    db.add(item)
    db.commit()
    db.refresh(item)
    return serialize_user_game(item)


@app.get("/api/user-games/{item_id}", response_model=UserGameOut)
def get_user_game(item_id: int, db: Db, user: CurrentUser):
    item = db.get(UserGame, item_id)
    if not item or item.user_id != user.id:
        raise HTTPException(status_code=404, detail="记录不存在")
    return serialize_user_game(item)


@app.put("/api/user-games/{item_id}", response_model=UserGameOut)
def update_user_game(item_id: int, data: UserGameUpdate, db: Db, user: CurrentUser):
    item = db.get(UserGame, item_id)
    if not item or item.user_id != user.id:
        raise HTTPException(status_code=404, detail="记录不存在")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(item, field, value)
    db.commit()
    db.refresh(item)
    return serialize_user_game(item)


@app.delete("/api/user-games/{item_id}")
def delete_user_game(item_id: int, db: Db, user: CurrentUser):
    item = db.get(UserGame, item_id)
    if not item or item.user_id != user.id:
        raise HTTPException(status_code=404, detail="记录不存在")
    db.delete(item)
    db.commit()
    return {"message": "删除成功"}


@app.get("/api/play-sessions", response_model=list[PlaySessionOut])
def list_sessions(db: Db, user: CurrentUser, user_game_id: int | None = None):
    stmt = select(PlaySession).join(UserGame).where(UserGame.user_id == user.id).order_by(PlaySession.played_at.desc())
    if user_game_id:
        stmt = stmt.where(PlaySession.user_game_id == user_game_id)
    return db.scalars(stmt).all()


@app.post("/api/play-sessions", response_model=PlaySessionOut)
def create_session(data: PlaySessionCreate, db: Db, user: CurrentUser):
    user_game = db.get(UserGame, data.user_game_id)
    if not user_game or user_game.user_id != user.id:
        raise HTTPException(status_code=404, detail="游戏库记录不存在")
    item = PlaySession(**data.model_dump())
    user_game.playtime_hours = Decimal(user_game.playtime_hours or 0) + data.duration_hours
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@app.put("/api/play-sessions/{session_id}", response_model=PlaySessionOut)
def update_session(session_id: int, data: PlaySessionUpdate, db: Db, user: CurrentUser):
    item = db.get(PlaySession, session_id)
    if not item or item.user_game.user_id != user.id:
        raise HTTPException(status_code=404, detail="日志不存在")
    old_duration = Decimal(item.duration_hours or 0)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(item, field, value)
    if data.duration_hours is not None:
        item.user_game.playtime_hours = Decimal(item.user_game.playtime_hours or 0) - old_duration + data.duration_hours
    db.commit()
    db.refresh(item)
    return item


@app.delete("/api/play-sessions/{session_id}")
def delete_session(session_id: int, db: Db, user: CurrentUser):
    item = db.get(PlaySession, session_id)
    if not item or item.user_game.user_id != user.id:
        raise HTTPException(status_code=404, detail="日志不存在")
    item.user_game.playtime_hours = max(Decimal("0"), Decimal(item.user_game.playtime_hours or 0) - Decimal(item.duration_hours or 0))
    db.delete(item)
    db.commit()
    return {"message": "删除成功"}


@app.get("/api/analytics/overview", response_model=OverviewOut)
def overview(db: Db, user: CurrentUser):
    rows = db.scalars(select(UserGame).where(UserGame.user_id == user.id)).all()
    return OverviewOut(
        total_games=len(rows),
        wishlist_count=sum(1 for row in rows if row.status == "wishlist"),
        playing_count=sum(1 for row in rows if row.status == "playing"),
        completed_count=sum(1 for row in rows if row.status == "completed"),
        purchased_count=sum(1 for row in rows if row.status in {"purchased", "playing", "completed", "paused", "dropped"}),
        total_spent=sum((row.purchase_price or Decimal("0")) for row in rows),
        total_playtime=sum((row.playtime_hours or Decimal("0")) for row in rows),
    )


@app.get("/api/analytics/platforms")
def platform_stats(db: Db, user: CurrentUser):
    stmt = (
        select(Platform.name, func.count(UserGame.id))
        .join(GamePlatform, GamePlatform.platform_id == Platform.id)
        .join(Game, Game.id == GamePlatform.game_id)
        .join(UserGame, UserGame.game_id == Game.id)
        .where(UserGame.user_id == user.id)
        .group_by(Platform.name)
    )
    return [{"name": name, "value": count} for name, count in db.execute(stmt).all()]


@app.get("/api/analytics/categories")
def category_stats(db: Db, user: CurrentUser):
    stmt = (
        select(Category.name, func.count(UserGame.id))
        .join(GameCategory, GameCategory.category_id == Category.id)
        .join(Game, Game.id == GameCategory.game_id)
        .join(UserGame, UserGame.game_id == Game.id)
        .where(UserGame.user_id == user.id)
        .group_by(Category.name)
    )
    return [{"name": name, "value": count} for name, count in db.execute(stmt).all()]


@app.get("/api/analytics/monthly-playtime")
def monthly_playtime(db: Db, user: CurrentUser):
    stmt = (
        select(func.date_format(PlaySession.played_at, "%Y-%m"), func.sum(PlaySession.duration_hours))
        .join(UserGame, UserGame.id == PlaySession.user_game_id)
        .where(UserGame.user_id == user.id)
        .group_by(func.date_format(PlaySession.played_at, "%Y-%m"))
        .order_by(func.date_format(PlaySession.played_at, "%Y-%m"))
    )
    return [{"month": month, "hours": float(hours or 0)} for month, hours in db.execute(stmt).all()]


@app.get("/api/analytics/statuses")
def status_stats(db: Db, user: CurrentUser):
    stmt = (
        select(UserGame.status, func.count(UserGame.id))
        .where(UserGame.user_id == user.id)
        .group_by(UserGame.status)
    )
    return [{"name": status_name, "value": count} for status_name, count in db.execute(stmt).all()]


@app.get("/api/analytics/monthly-added")
def monthly_added(db: Db, user: CurrentUser):
    stmt = (
        select(func.date_format(UserGame.created_at, "%Y-%m"), func.count(UserGame.id))
        .where(UserGame.user_id == user.id)
        .group_by(func.date_format(UserGame.created_at, "%Y-%m"))
        .order_by(func.date_format(UserGame.created_at, "%Y-%m"))
    )
    return [{"month": month, "count": count} for month, count in db.execute(stmt).all()]


@app.get("/api/analytics/top-rated")
def top_rated(db: Db, user: CurrentUser):
    rows = db.scalars(
        select(UserGame)
        .where(UserGame.user_id == user.id, UserGame.rating.is_not(None))
        .order_by(UserGame.rating.desc())
        .limit(5)
    ).all()
    return [{"title": row.game.title, "value": float(row.rating or 0)} for row in rows]


@app.get("/api/analytics/top-playtime")
def top_playtime(db: Db, user: CurrentUser):
    rows = db.scalars(
        select(UserGame)
        .where(UserGame.user_id == user.id)
        .order_by(UserGame.playtime_hours.desc())
        .limit(5)
    ).all()
    return [{"title": row.game.title, "value": float(row.playtime_hours or 0)} for row in rows]


@app.get("/api/analytics/spending-by-platform")
def spending_by_platform(db: Db, user: CurrentUser):
    stmt = (
        select(Platform.name, func.sum(UserGame.purchase_price))
        .join(GamePlatform, GamePlatform.platform_id == Platform.id)
        .join(Game, Game.id == GamePlatform.game_id)
        .join(UserGame, UserGame.game_id == Game.id)
        .where(UserGame.user_id == user.id)
        .group_by(Platform.name)
    )
    return [{"name": name, "value": float(value or 0)} for name, value in db.execute(stmt).all()]


@app.post("/api/demo/reset")
def reset_demo_data(db: Db, user: CurrentUser):
    if user.username != "demo":
        raise HTTPException(status_code=403, detail="仅演示账号允许重置演示数据")
    demo = db.scalar(select(User).where(User.username == "demo"))
    if demo:
        for item in list(demo.games):
            db.delete(item)
        db.flush()
    seed_data(db)
    return {"message": "演示数据已重置"}
