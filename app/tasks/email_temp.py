from email.message import EmailMessage
from pydantic import EmailStr
from app.config import settings



def creat_booking_confirmation_template(
    booking: dict,
    email_to: EmailStr,

):
    email = EmailMessage()

    email["Subject"] = "Подтверждение бронирования"
    email["From"] = settings.SMTP_USER
    email["To"] = email_to

    email.set_content(
        f"""
            <h1>Подтвердите бронирование</h1>
            Вы забранировали отель с {booking["data_from"]} по {booking["data_to"]}
        """,
        subtype="html"
    )
    
    return email