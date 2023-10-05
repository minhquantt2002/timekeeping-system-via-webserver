from fastapi import FastAPI
import backend

app = FastAPI()

app.include_router(backend.app)
