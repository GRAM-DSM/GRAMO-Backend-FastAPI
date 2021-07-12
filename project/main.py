from fastapi import FastAPI

import uvicorn

from project.apps import auth, notice

from project.config import WORKERS


app = FastAPI()
app.include_router(auth.router)
app.include_router(notice.router)

if __name__ == '__main__':
    uvicorn.run("project.main:app", host="0.0.0.0", port=8000, workers=WORKERS)
