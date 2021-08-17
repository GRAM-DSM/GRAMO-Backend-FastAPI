from sqlalchemy.orm.session import Session

def create(cls, session: Session, auto_commit=True, **kwargs):
    obj = cls()
    for column, value in kwargs.items():
        setattr(obj, column, value)

    session.add(obj)
    session.flush()
    if auto_commit:
        session.commit()

def delete(session: Session, del_thing, auto_commit=True):
    session.delete(del_thing)
    session.flush()
    if auto_commit:
        session.commit()
