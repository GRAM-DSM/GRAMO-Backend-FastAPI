from fastapi import HTTPException, status

import smtplib

from email.mime.text import MIMEText

from project.core.models import Redis

from project.config import EMAIL, EMAIL_PASSWORD


async def send_code(code: str, address: str):
    session = smtplib.SMTP(host='smtp.gmail.com', port=587)

    session.starttls()

    session.login(user=EMAIL, password=EMAIL_PASSWORD)

    title = "GRAMO 이메일 인증 메일"
    content = f"이메일 인증 코드는 {code}입니다."

    mail = MIMEText(content)
    mail['Subject'] = title

    session.sendmail(from_addr=EMAIL, to_addrs=address, msg=mail.as_string())

    session.quit()


def code_check(email: str, code: int):
    stored_code = Redis.get(email)

    if not stored_code:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="this email does not exist")

    if int(stored_code) != code:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="email and code does not match")
