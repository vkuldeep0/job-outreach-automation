from datetime import date

from pydantic import BaseModel, Field


class ApplicationCreate(BaseModel):
    company: str = Field(min_length=1)
    job_title: str = Field(min_length=1)
    job_url: str | None = None
    application_date: date
    status: str = "applied"


class ApplicationUpdate(BaseModel):
    status: str
