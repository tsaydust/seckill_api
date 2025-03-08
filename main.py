from fastapi import FastAPI
from hooks.middlewares import db_session_middleware
from starlette.middleware.base import BaseHTTPMiddleware
from routers import seckill, order

app = FastAPI()

# 添加路由
app.include_router(seckill.router)
app.include_router(order.router)

app.add_middleware(BaseHTTPMiddleware, dispatch=db_session_middleware)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
