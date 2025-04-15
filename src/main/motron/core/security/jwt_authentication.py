import jwt
from flask import request, g
from jwt import InvalidTokenError
from motron.core.config_loader import get_config
import os

PUBLIC_KEY = None


def load_public_key():
    config = get_config().get("motron", {}).get("security", {}).get("oauth2", {}).get("resourceserver", {}).get("jwt", {})
    path = config.get("public-key-location")
    if not path:
        return None

    if path.startswith("classpath:"):
        rel_path = path.replace("classpath:", "src/main/resources/")
    else:
        rel_path = path

    try:
        with open(os.path.abspath(rel_path), "r") as f:
            return f.read()
    except FileNotFoundError:
        print(f"[Motron] Public key file not found at {rel_path}")
        return None


PUBLIC_KEY = load_public_key()


def jwt_authentication_middleware(app):
    if not PUBLIC_KEY:
        print("[Motron] JWT authentication not enabled (no public key found in application.yml)")
        return

    @app.before_request
    def authenticate():
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header.replace("Bearer ", "")
            try:
                decoded = jwt.decode(token, PUBLIC_KEY, algorithms=["RS256"])
                g.user = decoded
            except InvalidTokenError:
                g.user = None
        else:
            g.user = None
