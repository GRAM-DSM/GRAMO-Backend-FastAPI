from fastapi import FastAPI

from project.apps import auth, notice

app = FastAPI()

app.include_router(auth.router)
app.include_router(notice.router)
