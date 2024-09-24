from fastapi import FastAPI
from routers import chat
from database import Base, engine
import uvicorn

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(chat.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
