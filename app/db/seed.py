import uuid

from app.core.config import settings
from app.core.security import get_password_hash
from app.db.base import SessionLocal
from app.models.user import User


def seed():
    if settings.DISPATCHER_USERNAME in [None, ""] or settings.DISPATCHER_PASSWORD in [None, ""]:
        raise Exception("You must specify a username or password.")

    db = SessionLocal()
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(User.username == settings.DISPATCHER_USERNAME).first()
        if existing_user:
            print("User already exists, skipping seeding.")
            return

        user = User(
            id=uuid.uuid4(),
            username=settings.DISPATCHER_USERNAME,
            email=settings.DISPATCHER_EMAIL,
            hashed_password=get_password_hash(settings.DISPATCHER_PASSWORD),
            role="dispatcher",
            is_active=True,
        )
        db.add(user)
        db.commit()
        print("User seeded successfully")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
