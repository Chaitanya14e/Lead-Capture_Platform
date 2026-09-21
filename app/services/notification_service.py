import time


def send_submission_notification(submission_id: int) -> None:
    print(
        f"Sending notification for submission {submission_id}"
    )

    print(
        f"Notification sent for submission {submission_id}"
    )


def send_with_retry(
    submission_id: int,
    max_retries: int = 3,
) -> None:

    for attempt in range(1, max_retries + 1):
        try:
            send_submission_notification(submission_id)
            return

        except Exception as error:
            print(
                f"Notification attempt {attempt} failed: {error}"
            )

            if attempt == max_retries:
                print(
                    f"Notification permanently failed "
                    f"for submission {submission_id}"
                )
                return

            time.sleep(1)