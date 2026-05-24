import importlib
import os

os.environ["DATABASE_URL"] = "sqlite+pysqlite:///:memory:"
os.environ["SECRET_KEY"] = "test-secret"

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy import event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

main = importlib.import_module("app.main")

engine = create_engine(
    "sqlite+pysqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


@event.listens_for(engine, "connect")
def add_sqlite_functions(dbapi_connection, connection_record):
    def date_format(value, fmt):
        return str(value)[:7]

    dbapi_connection.create_function("date_format", 2, date_format)


TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def override_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


main.app.dependency_overrides[main.get_db] = override_db
client = TestClient(main.app)


def setup_module():
    main.Base.metadata.create_all(bind=engine)
    with TestingSessionLocal() as db:
        main.seed_data(db)


def auth_headers(username="demo", password="demo123456"):
    res = client.post("/api/auth/login", json={"username": username, "password": password})
    assert res.status_code == 200
    return {"Authorization": f"Bearer {res.json()['access_token']}"}


def test_auth_register_login_and_profile():
    res = client.post("/api/auth/register", json={
        "username": "alice",
        "email": "alice@example.com",
        "password": "password123",
        "nickname": "Alice",
    })
    assert res.status_code == 200
    token = res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    assert client.get("/api/auth/me", headers=headers).json()["username"] == "alice"
    updated = client.put("/api/auth/me", json={"nickname": "A 玩家", "bio": "hello"}, headers=headers)
    assert updated.status_code == 200
    assert updated.json()["nickname"] == "A 玩家"
    assert client.post("/api/auth/login", json={"username": "alice", "password": "bad"}).status_code == 400


def test_games_user_games_and_detail_flow():
    headers = auth_headers()
    lookups = {
        "platform_ids": [client.get("/api/platforms").json()[0]["id"]],
        "category_ids": [client.get("/api/categories").json()[0]["id"]],
        "tag_ids": [client.get("/api/tags").json()[0]["id"]],
    }
    game_payload = {
        "title": "Test Game",
        "original_title": "Test Game",
        "cover_url": "https://example.com/cover.jpg",
        "developer": "Tester",
        "publisher": "Tester",
        "release_date": "2024-01-01",
        "description": "A test game",
        **lookups,
    }
    game = client.post("/api/games", json=game_payload, headers=headers)
    assert game.status_code == 200
    game_id = game.json()["id"]
    assert client.get(f"/api/games/{game_id}").json()["title"] == "Test Game"
    assert client.put(f"/api/games/{game_id}", json={**game_payload, "title": "Test Game 2"}, headers=headers).status_code == 200
    user_game = client.post("/api/user-games", json={"game_id": game_id, "status": "wishlist"}, headers=headers)
    assert user_game.status_code == 200
    user_game_id = user_game.json()["id"]
    assert client.post("/api/user-games", json={"game_id": game_id}, headers=headers).status_code == 400
    assert client.put(f"/api/user-games/{user_game_id}", json={"status": "playing", "rating": "8.5"}, headers=headers).json()["status"] == "playing"
    assert client.get(f"/api/user-games/{user_game_id}", headers=headers).status_code == 200
    assert client.delete(f"/api/user-games/{user_game_id}", headers=headers).status_code == 200
    assert client.delete("/api/games/999999", headers=headers).status_code == 404


def test_lookup_create_update_delete_and_protection():
    headers = auth_headers()
    platform = client.post("/api/platforms", json={"name": "GOG", "icon": "shop"}, headers=headers).json()
    assert client.put(f"/api/platforms/{platform['id']}", json={"name": "GOG Galaxy", "icon": "shop"}, headers=headers).status_code == 200
    assert client.delete(f"/api/platforms/{platform['id']}", headers=headers).status_code == 200
    category = client.post("/api/categories", json={"name": "PUZ", "description": "Puzzle"}, headers=headers).json()
    assert client.put(f"/api/categories/{category['id']}", json={"name": "Puzzle", "description": "Puzzle"}, headers=headers).status_code == 200
    assert client.delete(f"/api/categories/{category['id']}", headers=headers).status_code == 200
    tag = client.post("/api/tags", json={"name": "测试标签", "color": "#ffffff"}, headers=headers).json()
    assert client.put(f"/api/tags/{tag['id']}", json={"name": "测试标签2", "color": "#000000"}, headers=headers).status_code == 200
    assert client.delete(f"/api/tags/{tag['id']}", headers=headers).status_code == 200
    protected_id = client.get("/api/platforms").json()[0]["id"]
    assert client.delete(f"/api/platforms/{protected_id}", headers=headers).status_code == 400


def test_play_sessions_and_analytics():
    headers = auth_headers()
    user_game = client.get("/api/user-games", headers=headers).json()[0]
    user_game_id = user_game["id"]
    created = client.post("/api/play-sessions", json={
        "user_game_id": user_game_id,
        "played_at": "2025-01-01",
        "duration_hours": "2.5",
        "progress_note": "chapter 1",
        "note": "fun",
    }, headers=headers)
    assert created.status_code == 200
    session_id = created.json()["id"]
    assert client.get("/api/play-sessions", headers=headers).status_code == 200
    updated = client.put(f"/api/play-sessions/{session_id}", json={"duration_hours": "3.0", "note": "updated"}, headers=headers)
    assert updated.status_code == 200
    for path in [
        "/api/analytics/overview",
        "/api/analytics/platforms",
        "/api/analytics/categories",
        "/api/analytics/statuses",
        "/api/analytics/monthly-playtime",
        "/api/analytics/monthly-added",
        "/api/analytics/top-rated",
        "/api/analytics/top-playtime",
        "/api/analytics/spending-by-platform",
    ]:
        assert client.get(path, headers=headers).status_code == 200
    assert client.delete(f"/api/play-sessions/{session_id}", headers=headers).status_code == 200


def test_demo_reset_and_auth_errors():
    headers = auth_headers()
    assert client.post("/api/demo/reset", headers=headers).status_code == 200
    bad = {"Authorization": "Bearer bad.token.value"}
    assert client.get("/api/auth/me", headers=bad).status_code == 401
    alice_headers = auth_headers("alice", "password123")
    assert client.post("/api/demo/reset", headers=alice_headers).status_code == 403
    assert client.get("/api/user-games/999999", headers=headers).status_code == 404
    assert client.put("/api/play-sessions/999999", json={"note": "x"}, headers=headers).status_code == 404
