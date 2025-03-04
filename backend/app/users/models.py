from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declarative_base

Base = declarative_base()


class User(SQLAlchemyBaseUserTableUUID, Base):
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
