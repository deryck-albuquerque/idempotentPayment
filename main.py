import uvicorn
from fastapi import FastAPI

from api.router import router

def init_app() -> FastAPI:
    app = FastAPI(
        title="idempotentPayment",
        version="1.0.0"
    )

    app.include_router(router)

    return app

app = init_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)