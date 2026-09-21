from fastapi import APIRouter, Depends, HTTPException, Request, status, BackgroundTasks
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.orm import Session
from app.services.notification_service import send_with_retry

from app.db import get_db
from app.models.submission import Submission
from app.models.widget import Widget
from app.schemas.submission import (
    SubmissionCreate,
    SubmissionResponse,
)
from app.services.geo_service import get_geo

router = APIRouter(
    prefix="/submissions",
    tags=["Submissions"],
)


limiter = Limiter(
    key_func=get_remote_address,
)


@router.post(
    "",
    response_model=SubmissionResponse,
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit("5/minute")
def create_submission(
    request: Request,
    submission_data: SubmissionCreate,
    background_tasks: BackgroundTasks,
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

    if submission_data.honeypot:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Spam submission detected",
        )

    client_ip = None

    if request.client:
        client_ip = request.client.host

    geo_data = get_geo(client_ip)

    submission = Submission(
        widget_id=submission_data.widget_id,
        name=submission_data.name,
        email=submission_data.email,
        message=submission_data.message,
        ip_address=client_ip,
        country=geo_data["country"],
        city=geo_data["city"],
        spam=False,
    )

    db.add(submission)
    db.commit()
    db.refresh(submission)
    background_tasks.add_task(
        send_with_retry,
        submission.id,
    )

    return submission