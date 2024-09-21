from celery import shared_task
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content
from app import config


@shared_task(ignore_result=False)
def schedule_notes_email_remainder(email: str, title: str, content: str) -> bool:
    try:
        sg = sendgrid.SendGridAPIClient(api_key=config.Config.SENDGRID_SECRET_KEY)
        from_email = Email(config.Config.MAIL_DEFAULT_SENDER)
        to_email = To(email)
        subject = f"Remainder note:{title}"
        content = Content("text/plain", content)
        mail = Mail(from_email, to_email, subject, content)

        mail_json = mail.get()

        sg.client.mail.send.post(request_body=mail_json)
    except Exception as e:
        print(f"exception on sending mail email:{email}")
