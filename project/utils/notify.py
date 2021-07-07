from pyfcm import FCMNotification

from project.core.models import Session
from project.core.models.user import User_tbl

from project.config import APIKEY


push_service = FCMNotification(APIKEY)


def set_user_fcm_token(session: Session, token: str, email: str):
    session.query(User_tbl).filter(User_tbl.email == email).update({"token": token})


def get_user_fcm_tokens(session: Session, email: str):
    users = session.query(User_tbl).filter(User_tbl.email != email).all()

    tokens = [user.token for user in users]

    return tokens


def send_message(tokens: list, title: str, body: str):
    message = {
        "title": title,
        "body": body,
        "click_action": "notice"
    }

    push_service.notify_multiple_devices(
        registration_ids=tokens,
        data_message=message
    )
