from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import uvicorn

from project.apps import auth, notice


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(notice.router)

if __name__ == '__main__':
    uvicorn.run("project.main:app", host="0.0.0.0")
