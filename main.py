from fastapi import FastAPI, Path
from typing import Annotated

from core.config import settings
from core.models import Base, db_helper
from fastapi.concurrency import asynccontextmanager
from items_views import router as items_router
from users.views import router as users_router
from api_v1 import router as router_v1


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="FastAPI_try_2", lifespan=lifespan)
app.include_router(router=router_v1, prefix=settings.api_v1_prefix)

app.include_router(items_router, tags=["Items"])
app.include_router(users_router, tags=["Users"])


@app.get("/")
async def hello_index():
    return {"message": f"Hello"}


@app.get("/hello")
async def hello(name: str = ""):
    name = name.title()
    return {"message": f"Hello {name}"}


@app.post("/calc/add")
async def add(a: int, b: int):
    return {"a": a, "b": b, "res": a + b}


@app.get("/items/{id}")
async def list_items(id: Annotated[int, Path(ge=1)]):
    return {"items": {"id": id}}
