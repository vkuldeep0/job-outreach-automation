from datetime import date

from sqlalchemy import Date, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base

class Application(Base):
	__tablename__ = "applications"

	id: Mapped[int] = mapped_column(Integer, primary_key=True)
	company: Mapped[str] = mapped_column(String(255))
	job_title: Mapped[str] = mapped_column(String(255))
	job_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
	application_date: Mapped[date] = mapped_column(Date)
	status: Mapped[str] = mapped_column(String(50), default="applied")

