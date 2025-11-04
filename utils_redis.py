import redis
import secrets
from datetime import datetime
from typing import cast

# create a Redis connection
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def create_session(user_id: str, role: str, ttl: int = 3600):
    """Create a login session and return the token"""
    token = secrets.token_hex(16)
    key = f"session:{user_id}"
    r.hset(key, mapping={
        "token": token,
        "role": role,
        "login_time": datetime.now().isoformat()
    })
    r.expire(key, ttl) 
    return token

def verify_session(user_id: str, token: str) -> bool:
    """Verify if the session is valid"""
    key = f"session:{user_id}"
    stored_token = r.hget(key, "token")
    return stored_token == token
def get_user_role(user_id: str) -> str | None:
    """Get user role"""
    # redis-py hget may return an awaitable in some setups; cast to str | None for consistent typing
    return cast(str | None, r.hget(f"session:{user_id}", "role"))
    return r.hget(f"session:{user_id}", "role")

def delete_session(user_id: str):
    """Logout"""
    r.delete(f"session:{user_id}")
