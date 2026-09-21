from pydantic import BaseModel, Field


class WidgetCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    widget_type: str = Field(min_length=1, max_length=50)
    description: str | None = None


class WidgetUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    widget_type: str | None = Field(default=None, min_length=1, max_length=50)
    description: str | None = None
    is_active: bool | None = None


class WidgetResponse(BaseModel):
    id: int
    owner_id: int
    name: str
    widget_type: str
    description: str | None
    public_key: str
    is_active: bool

    model_config = {
        "from_attributes": True
    }