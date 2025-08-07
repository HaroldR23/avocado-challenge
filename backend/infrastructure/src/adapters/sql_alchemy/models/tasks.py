from typing import TYPE_CHECKING, List
from infrastructure.src.adapters.sql_alchemy.models.base import Base

from enum import Enum

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Priority(Enum):
    LOW = "baja"
    MEDIUM = "media"
    HIGH = "alta"

if TYPE_CHECKING:
    from infrastructure.src.adapters.sql_alchemy.models.users import User
    from infrastructure.src.adapters.sql_alchemy.models.comments import Comment

class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    completed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    due_date: Mapped[str] = mapped_column(DateTime, nullable=True)
    priority: Mapped[Priority] = mapped_column(SqlEnum(Priority), nullable=False, default=Priority.LOW)

    created_by_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    assigned_to_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)

    created_by: Mapped["User"] = relationship("User", foreign_keys=[created_by_id])
    assigned_to: Mapped["User"] = relationship("User", foreign_keys=[assigned_to_id])
    comments: Mapped[List["Comment"]] = relationship(cascade="all, delete-orphan")

    created_at: Mapped[str] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[str] = mapped_column(DateTime, nullable=False)
