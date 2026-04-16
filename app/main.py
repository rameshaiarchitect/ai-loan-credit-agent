from fastapi import FastAPI
from contextlib import asynccontextmanager
from threading import Thread
from app.consumer import consume_events


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    thread = Thread(target=consume_events)
    thread.daemon = True
    thread.start()

    yield

    # Shutdown logic (optional)
    print("Shutting down Credit Agent...")


app = FastAPI(lifespan=lifespan)


@app.get("/")
def health():
    return {"status": "Credit Agent Running"}