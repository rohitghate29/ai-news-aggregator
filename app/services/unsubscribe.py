import base64
import hashlib
import hmac
import os
from urllib.parse import quote

from dotenv import load_dotenv

load_dotenv()

UNSUBSCRIBE_SECRET = os.getenv("UNSUBSCRIBE_SECRET") or os.getenv("APP_PASSWORD") or "dev-unsubscribe-secret"
APP_BASE_URL = os.getenv("APP_BASE_URL", "http://127.0.0.1:8000").rstrip("/")


def _sign_email(email: str) -> str:
    return hmac.new(
        UNSUBSCRIBE_SECRET.encode("utf-8"),
        email.strip().lower().encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()


def create_unsubscribe_token(email: str) -> str:
    normalized_email = email.strip().lower()
    payload = f"{normalized_email}:{_sign_email(normalized_email)}"
    return base64.urlsafe_b64encode(payload.encode("utf-8")).decode("utf-8")


def parse_unsubscribe_token(token: str) -> str | None:
    try:
        payload = base64.urlsafe_b64decode(token.encode("utf-8")).decode("utf-8")
        email, signature = payload.rsplit(":", 1)
    except (ValueError, UnicodeDecodeError):
        return None

    expected_signature = _sign_email(email)
    if not hmac.compare_digest(signature, expected_signature):
        return None
    return email


def create_unsubscribe_url(email: str) -> str:
    token = create_unsubscribe_token(email)
    return f"{APP_BASE_URL}/unsubscribe?token={quote(token)}"
