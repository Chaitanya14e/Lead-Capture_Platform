from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class SubmissionCreate(BaseModel):
    widget_id: int
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    message: str = Field(min_length=1, max_length=5000)
    honeypot: str | None = None


class SubmissionResponse(BaseModel):
    id: int
    widget_id: int
    name: str
    email: EmailStr
    message: str
    country: str | None
    city: str | None
    spam: bool
    created_at: datetime

    model_config = {
        "from_attributes": True
    }