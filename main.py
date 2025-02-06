from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.config.database import db_helper
from app.routes.product_routes import product_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_helper.connect()
    db = await db_helper.get_db()
    yield
    await db_helper.disconnect()

app = FastAPI(lifespan=lifespan)

# app.include_router(router = auth_routes.auth_router, prefix = f'/api/{version}')
app.include_router(product_router)

@app.get("/")
async def root():
    return {"message": "Welcome to the E-commerce API"}