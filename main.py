from fastapi import FastAPI
from routes.user_routes import user_router


app = FastAPI()


@app.get("/")
def home():
    return {"hello": "world"}


app.include_router(prefix="/users", router=user_router)
