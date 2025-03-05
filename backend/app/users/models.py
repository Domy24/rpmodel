from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declarative_base, relationship

from ..base import Base
from ..routes.models import Route

class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "user"

    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    route: Mapped[list["Route"]] = relationship("Route", back_populates="user", cascade="all, delete-orphan")
