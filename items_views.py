
from typing import Annotated

from fastapi import Path, APIRouter


router = APIRouter(prefix='/items')

@router.get('/latest')
async def get_latest_item():
    return {'item': {'id':'0','name':'latest'}}




@router.get('/{item_id}')
async def list_items(item_id: Annotated[int, Path(ge=1)]):
    return {
        'items':
            {'id':item_id}
        }
    
    

