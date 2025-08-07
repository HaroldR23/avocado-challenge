from typing import Generator
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from infrastructure.src.adapters.sql_alchemy.session import get_db
from infrastructure.src.adapters.sql_alchemy.models.roles import Role

DEFAULT_ROLE_NAME = "admin"

def create_default_role():
    session_gen: Generator[Session, None, None] = get_db()

    session: Session = next(session_gen)
    try:
        result = session.execute(select(Role).where(Role.name == DEFAULT_ROLE_NAME))
        role = result.scalars().first()

        if role:
            print(f"Role '{DEFAULT_ROLE_NAME}' already exists.")
            return role.id

        print(f"Creating role '{DEFAULT_ROLE_NAME}'...")
        new_role = Role(name=DEFAULT_ROLE_NAME)
        session.add(new_role)
        session.commit()
        print(f"Role '{DEFAULT_ROLE_NAME}' created successfully.")
        return new_role.id

    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error creating role: {e}")
        return None
    finally:
        session.close()
