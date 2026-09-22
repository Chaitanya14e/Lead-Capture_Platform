from pydantic import ValidationError
import pytest

from app.schemas.submission import SubmissionCreate


def test_valid_submission():
    submission = SubmissionCreate(
        widget_id=1,
        idempotency_key="test-key-123",
        name="Chaitanya",
        email="test@example.com",
        message="This is a valid submission.",
        honeypot=None,
    )

    assert submission.widget_id == 1
    assert submission.email == "test@example.com"


def test_invalid_email():
    with pytest.raises(ValidationError):
        SubmissionCreate(
            widget_id=1,
            idempotency_key="test-key-123",
            name="Chaitanya",
            email="invalid-email",
            message="Test message",
        )


def test_empty_name():
    with pytest.raises(ValidationError):
        SubmissionCreate(
            widget_id=1,
            idempotency_key="test-key-123",
            name="",
            email="test@example.com",
            message="Test message",
        )


def test_empty_message():
    with pytest.raises(ValidationError):
        SubmissionCreate(
            widget_id=1,
            idempotency_key="test-key-123",
            name="Chaitanya",
            email="test@example.com",
            message="",
        )


def test_message_too_long():
    with pytest.raises(ValidationError):
        SubmissionCreate(
            widget_id=1,
            idempotency_key="test-key-123",
            name="Chaitanya",
            email="test@example.com",
            message="x" * 5001,
        )


def test_idempotency_key_required():
    with pytest.raises(ValidationError):
        SubmissionCreate(
            widget_id=1,
            name="Chaitanya",
            email="test@example.com",
            message="Test message",
        )