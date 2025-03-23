from __future__ import annotations


from sqlalchemy import Integer, String, JSON, ForeignKey
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship

from ..base import Base



class Route(Base):
    __tablename__ = "route"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    edges: Mapped[dict] = mapped_column(JSON, nullable=False)
    start: Mapped[str] = mapped_column(String, nullable=False)
    end: Mapped[str] = mapped_column(String, nullable=False)
    stations: Mapped[list] = mapped_column(JSON, default=[])
    user_id: Mapped[str] = mapped_column(ForeignKey(column="user.id"), nullable=False)

    user: Mapped["user"] = relationship("User", back_populates="route")
