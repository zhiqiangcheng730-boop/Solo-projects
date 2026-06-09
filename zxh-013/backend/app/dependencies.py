from fastapi import Query


def get_current_user_id(user_id: int = Query(1, description="当前用户ID")):
    """Placeholder: returns hardcoded user_id=1 until auth is implemented."""
    return user_id
