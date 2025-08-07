from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from infrastructure.src.adapters.sql_alchemy.session import get_db
from infrastructure.src.adapters.sql_alchemy.models.users import User
from scripts.create_default_role import create_default_role

DEFAULT_USER = {
    "id": 256,
    "username": "admin",
    "email": "admin@example.com",
    "password_hash": "admin123" 
}

def create_default_user():
    session: Session = next(get_db())

    try:
        result = session.execute(
            select(User).where(User.username == DEFAULT_USER["username"])
        )
        user = result.scalars().first()
        if user:
            print("Default user already exists.")
            return

        role_id = create_default_role()
        if role_id is None:
            print("Cannot create user without role.")
            return

        print("Creating default user...")
        new_user = User(**DEFAULT_USER, role_id=role_id)
        session.add(new_user)
        session.commit()
        print("Default user created successfully.")

    except SQLAlchemyError as e:
        session.rollback()
        print(f"An error occurred while creating default user: {e}")
    finally:
        session.close()
