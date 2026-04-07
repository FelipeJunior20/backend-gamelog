from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token,
)


def test_hash_password_returns_different_string():
    hashed = hash_password("mysecret")
    assert hashed != "mysecret"


def test_verify_password_correct():
    hashed = hash_password("mysecret")
    assert verify_password("mysecret", hashed) is True


def test_verify_password_wrong():
    hashed = hash_password("mysecret")
    assert verify_password("wrongpassword", hashed) is False


def test_create_access_token_returns_string():
    token = create_access_token(subject=1)
    assert isinstance(token, str)
    assert len(token) > 0


def test_decode_access_token_valid():
    token = create_access_token(subject=42)
    result = decode_access_token(token)
    assert result == "42"


def test_decode_access_token_invalid():
    result = decode_access_token("token.invalido.qualquer")
    assert result is None


def test_decode_access_token_tampered():
    token = create_access_token(subject=1)
    tampered = token[:-5] + "XXXXX"
    result = decode_access_token(tampered)
    assert result is None
