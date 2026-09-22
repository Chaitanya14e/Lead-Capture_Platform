from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db import get_db
from app.dependencies import get_current_user
from app.models.submission import Submission
from app.models.widget import Widget
from app.models.user import User

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/submissions")
def get_dashboard_submissions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    submissions = (
        db.query(Submission)
        .join(Widget, Submission.widget_id == Widget.id)
        .filter(Widget.owner_id == current_user.id)
        .order_by(Submission.created_at.desc())
        .all()
    )

    return submissions


@router.get("/stats")
def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    total_submissions = (
        db.query(func.count(Submission.id))
        .join(Widget, Submission.widget_id == Widget.id)
        .filter(Widget.owner_id == current_user.id)
        .scalar()
    )

    spam_submissions = (
        db.query(func.count(Submission.id))
        .join(Widget, Submission.widget_id == Widget.id)
        .filter(
            Widget.owner_id == current_user.id,
            Submission.spam == True
        )
        .scalar()
    )

    total_widgets = (
        db.query(func.count(Widget.id))
        .filter(Widget.owner_id == current_user.id)
        .scalar()
    )

    active_widgets = (
        db.query(func.count(Widget.id))
        .filter(
            Widget.owner_id == current_user.id,
            Widget.is_active == True
        )
        .scalar()
    )

    return {
        "total_widgets": total_widgets,
        "active_widgets": active_widgets,
        "total_submissions": total_submissions,
        "spam_submissions": spam_submissions
    }


@router.get("/widgets/{widget_id}/stats")
def get_widget_stats(
    widget_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    widget = (
        db.query(Widget)
        .filter(
            Widget.id == widget_id,
            Widget.owner_id == current_user.id
        )
        .first()
    )

    if not widget:
        raise HTTPException(
            status_code=404,
            detail="Widget not found"
        )

    total_submissions = (
        db.query(func.count(Submission.id))
        .filter(Submission.widget_id == widget_id)
        .scalar()
    )

    spam_submissions = (
        db.query(func.count(Submission.id))
        .filter(
            Submission.widget_id == widget_id,
            Submission.spam == True
        )
        .scalar()
    )

    return {
        "widget_id": widget.id,
        "widget_name": widget.name,
        "total_submissions": total_submissions,
        "spam_submissions": spam_submissions
    }