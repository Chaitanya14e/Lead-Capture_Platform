import secrets

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.widget import Widget
from app.schemas.widget import (
    WidgetCreate,
    WidgetResponse,
    WidgetUpdate,
    PublicWidgetConfig
)

router = APIRouter(
    prefix="/widgets",
    tags=["Widgets"],
)


def generate_public_key() -> str:
    return secrets.token_urlsafe(32)


@router.post(
    "",
    response_model=WidgetResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_widget(
    widget_data: WidgetCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    widget = Widget(
        owner_id=current_user.id,
        name=widget_data.name,
        widget_type=widget_data.widget_type,
        description=widget_data.description,
        public_key=generate_public_key(),
        is_active=True,
    )

    db.add(widget)
    db.commit()
    db.refresh(widget)

    return widget


@router.get(
    "",
    response_model=list[WidgetResponse],
)
def get_widgets(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return (
        db.query(Widget)
        .filter(Widget.owner_id == current_user.id)
        .all()
    )


@router.get(
    "/{widget_id}",
    response_model=WidgetResponse,
)
def get_widget(
    widget_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    widget = (
        db.query(Widget)
        .filter(
            Widget.id == widget_id,
            Widget.owner_id == current_user.id,
        )
        .first()
    )

    if not widget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Widget not found",
        )

    return widget


@router.patch(
    "/{widget_id}",
    response_model=WidgetResponse,
)
def update_widget(
    widget_id: int,
    widget_data: WidgetUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    widget = (
        db.query(Widget)
        .filter(
            Widget.id == widget_id,
            Widget.owner_id == current_user.id,
        )
        .first()
    )

    if not widget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Widget not found",
        )

    update_data = widget_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(widget, field, value)

    db.commit()
    db.refresh(widget)

    return widget


@router.delete(
    "/{widget_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_widget(
    widget_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    widget = (
        db.query(Widget)
        .filter(
            Widget.id == widget_id,
            Widget.owner_id == current_user.id,
        )
        .first()
    )

    if not widget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Widget not found",
        )

    db.delete(widget)
    db.commit()

    return None

@router.get(
    "/public/{public_key}/config",
    response_model=PublicWidgetConfig
)
def get_public_widget_config(
    public_key: str,
    db: Session = Depends(get_db)
):
    widget = (
        db.query(Widget)
        .filter(
            Widget.public_key == public_key,
            Widget.is_active == True
        )
        .first()
    )

    if not widget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Widget not found or inactive"
        )

    return widget