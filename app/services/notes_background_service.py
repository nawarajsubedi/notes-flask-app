from datetime import datetime
from celery import shared_task


@shared_task(ignore_result=False)
def schedule_notes_email_remainder(email: str, title: str, content: str) -> bool:
    print("Inside celery function")
