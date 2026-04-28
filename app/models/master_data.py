from __future__ import annotations

from datetime import datetime

from sqlalchemy import BigInteger, Boolean, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Route(Base):
    __tablename__ = "route"
    __table_args__ = {"schema": "master_data"}

    route_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    route_code: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    route_name: Mapped[str | None] = mapped_column(String, nullable=True)
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, server_default="true"
    )
    created_at: Mapped[datetime] = mapped_column(
        nullable=False, server_default=func.now()
    )


class Vehicle(Base):
    __tablename__ = "vehicle"
    __table_args__ = {"schema": "master_data"}

    vehicle_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    vin: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    registration_number: Mapped[str | None] = mapped_column(String, nullable=True)
    fleet_number: Mapped[str | None] = mapped_column(String, nullable=True)
    operator_name: Mapped[str | None] = mapped_column(String, nullable=True)
    make: Mapped[str | None] = mapped_column(String, nullable=True)
    year: Mapped[str | None] = mapped_column(String, nullable=True)
    engine_number: Mapped[str | None] = mapped_column(String, nullable=True)
    gvm: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    tare: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    chassis_no: Mapped[str | None] = mapped_column(String, nullable=True)
    date_of_1st_registration: Mapped[datetime | None] = mapped_column(nullable=True)
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, server_default="true"
    )
    created_at: Mapped[datetime] = mapped_column(
        nullable=False, server_default=func.now()
    )
