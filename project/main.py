from fastapi import FastAPI

import uvicorn

from project.apps import auth, notice


if __name__ == '__main__':
    app = FastAPI()

    app.include_router(auth.router)
    app.include_router(notice.router)

    uvicorn.run(app, host="0.0.0.0", port=8000)
