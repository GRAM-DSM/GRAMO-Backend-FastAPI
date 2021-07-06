from pyfcm import FCMNotification

from project.core.models import Session
from project.core.models.user import User_tbl

from project.config import ANDROID_APIKEY, IOS_APIKEY


android_push_service = FCMNotification(ANDROID_APIKEY)
ios_push_service = FCMNotification(IOS_APIKEY)


def set_user_fcm_token(session: Session, token: str, email: str):
    session.query(User_tbl).filter(User_tbl.email == email).update({"token": token})


def get_user_fcm_tokens(session: Session, email: str):
    users = session.query(User_tbl).filter(User_tbl.email != email).all()

    tokens = [user.token for user in users]

    return tokens


def send_message(tokens: list, title: str, body: str):
    android_push_service.notify_multiple_devices(
        registration_ids=tokens,
        message_title=title,
        message_body=body,
        click_action="notice"
    )
