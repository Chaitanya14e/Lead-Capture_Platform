from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.submission import Submission
from app.models.widget import Widget
from app.schemas.submission import (
    SubmissionCreate,
    SubmissionResponse,
)

router = APIRouter(
    prefix="/submissions",
    tags=["Submissions"],
)


@router.post(
    "",
    response_model=SubmissionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_submission(
    submission_data: SubmissionCreate,
    request: Request,
    db: Session = Depends(get_db),
):
    widget = (
        db.query(Widget)
        .filter(
            Widget.id == submission_data.widget_id,
            Widget.is_active == True,
        )
        .first()
    )

    if not widget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Widget not found or inactive",
        )

    client_ip = None

    if request.client:
        client_ip = request.client.host

    submission = Submission(
        widget_id=submission_data.widget_id,
        name=submission_data.name,
        email=submission_data.email,
        message=submission_data.message,
        ip_address=client_ip,
        country=None,
        city=None,
        spam=False,
    )

    db.add(submission)
    db.commit()
    db.refresh(submission)

    return submission