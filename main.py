from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.config.database import db_helper
from app.routes.product_routes import product_router
from app.routes.auth_routes import auth_router
from app.routes.user_routes import user_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_helper.connect()
    db = await db_helper.get_db()
    yield
    await db_helper.disconnect()

app = FastAPI(lifespan=lifespan)

app.include_router(product_router)
app.include_router(auth_router)
app.include_router(user_router)

@app.get("/")
async def root():
    return {"message": "Welcome to the E-commerce API"}