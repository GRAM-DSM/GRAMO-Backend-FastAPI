from pydantic import BaseModel, constr


class CreateNotice(BaseModel):
    title: constr(min_length=1, max_length=50)
    content: constr(min_length=1, max_length=1000)
