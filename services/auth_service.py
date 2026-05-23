from database.connection import SessionLocal
from database.models import User

from utils.security import verify_password


def authenticate_user(
    email: str,
    password: str
):

    db = SessionLocal()

    user = db.query(User).filter(
        User.email == email
    ).first()

    db.close()

    if not user:
        return None

    if not verify_password(
        password,
        user.senha
    ):
        return None

    return user