from pydantic import BaseModel

from fastapi_jwt_auth import AuthJWT

from project.config import SECRET_KEY


class Settings(BaseModel):
    authjwt_secret_key: str = SECRET_KEY


@AuthJWT.load_config
def get_config():
    return Settings()
