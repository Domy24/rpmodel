from sqlalchemy import Float, String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from ..base import Base


class Vehicle(Base):
    __tablename__ = 'vehicle'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    model: Mapped[str] = mapped_column(String, nullable=False)
    weight_kg: Mapped[float] = mapped_column(Float, nullable=False)
    cd_area: Mapped[float] = mapped_column(Float, nullable=False)
    velocity_mps: Mapped[float] = mapped_column(Float, nullable=False)
    motor_efficiency: Mapped[float] = mapped_column(Float, nullable=False)
    front_area: Mapped[float] = mapped_column(Float, nullable=False)
    mu_r: Mapped[float] = mapped_column(Float, nullable=False)
    vtype: Mapped[str] = mapped_column(String, nullable=False)
    energy_usable: Mapped[float] = mapped_column(Float, nullable=False)
