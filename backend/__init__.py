import uvicorn
from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from . import routes

app = APIRouter()

templates = Jinja2Templates(directory="templates")
app.include_router(router=routes.router)


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, host="localhost", reload=True)
