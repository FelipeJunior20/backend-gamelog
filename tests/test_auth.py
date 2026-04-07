import pytest
from httpx import AsyncClient

REGISTER_URL = "/api/v1/auth/register"
LOGIN_URL = "/api/v1/auth/login"
ME_URL = "/api/v1/auth/me"
HEALTH_URL = "/api/v1/health"

USER_PAYLOAD = {
    "email": "gamer@example.com",
    "username": "gamer1",
    "password": "senha1234",
}


# ---------------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------------

async def test_health(client: AsyncClient):
    response = await client.get(HEALTH_URL)
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "database": "ok"}


# ---------------------------------------------------------------------------
# Register
# ---------------------------------------------------------------------------

async def test_register_success(client: AsyncClient):
    response = await client.post(REGISTER_URL, json=USER_PAYLOAD)
    assert response.status_code == 201
    body = response.json()
    assert body["email"] == USER_PAYLOAD["email"]
    assert body["username"] == USER_PAYLOAD["username"]
    assert body["is_active"] is True
    assert "hashed_password" not in body


async def test_register_duplicate_email(client: AsyncClient):
    await client.post(REGISTER_URL, json=USER_PAYLOAD)
    response = await client.post(REGISTER_URL, json=USER_PAYLOAD)
    assert response.status_code == 409


async def test_register_invalid_email(client: AsyncClient):
    response = await client.post(REGISTER_URL, json={**USER_PAYLOAD, "email": "nao-e-email"})
    assert response.status_code == 422


async def test_register_short_password(client: AsyncClient):
    response = await client.post(REGISTER_URL, json={**USER_PAYLOAD, "password": "123"})
    assert response.status_code == 422


async def test_register_short_username(client: AsyncClient):
    response = await client.post(REGISTER_URL, json={**USER_PAYLOAD, "username": "ab"})
    assert response.status_code == 422


# ---------------------------------------------------------------------------
# Login
# ---------------------------------------------------------------------------

async def test_login_success(client: AsyncClient):
    await client.post(REGISTER_URL, json=USER_PAYLOAD)
    response = await client.post(LOGIN_URL, json={
        "email": USER_PAYLOAD["email"],
        "password": USER_PAYLOAD["password"],
    })
    assert response.status_code == 200
    body = response.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"


async def test_login_wrong_password(client: AsyncClient):
    await client.post(REGISTER_URL, json=USER_PAYLOAD)
    response = await client.post(LOGIN_URL, json={
        "email": USER_PAYLOAD["email"],
        "password": "senhaerrada",
    })
    assert response.status_code == 401


async def test_login_nonexistent_user(client: AsyncClient):
    response = await client.post(LOGIN_URL, json={
        "email": "fantasma@example.com",
        "password": "qualquercoisa",
    })
    assert response.status_code == 401


# ---------------------------------------------------------------------------
# Me
# ---------------------------------------------------------------------------

async def test_me_authenticated(client: AsyncClient):
    await client.post(REGISTER_URL, json=USER_PAYLOAD)
    login = await client.post(LOGIN_URL, json={
        "email": USER_PAYLOAD["email"],
        "password": USER_PAYLOAD["password"],
    })
    token = login.json()["access_token"]

    response = await client.get(ME_URL, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    body = response.json()
    assert body["email"] == USER_PAYLOAD["email"]
    assert "hashed_password" not in body


async def test_me_without_token(client: AsyncClient):
    response = await client.get(ME_URL)
    assert response.status_code == 401


async def test_me_invalid_token(client: AsyncClient):
    response = await client.get(ME_URL, headers={"Authorization": "Bearer token.falso.aqui"})
    assert response.status_code == 401
