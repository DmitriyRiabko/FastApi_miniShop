from fastapi import FastAPI,Path
from pydantic import BaseModel, EmailStr
from typing import Annotated
from items_views import router as items_router
from users.views import router as users_router



app = FastAPI(title='FastAPI_try_2')
app.include_router(items_router,tags=['Items'])
app.include_router(users_router,tags=['Users'])







@app.get('/')
async def hello_index():
    return {'message':f'Hello'}



@app.get('/hello')
async def hello(name:str = ''):
    name = name.title()
    return {'message':f'Hello {name}'}






   
   
@app.post('/calc/add')
async def add(a: int ,b: int):
    return {
        'a':a,
        'b':b,
        'res': a+b
    }
    


@app.get('/items/{id}')
async def list_items(id: Annotated[int, Path(ge=1)]):
    return {
        'items':
            {'id':id}
        }


