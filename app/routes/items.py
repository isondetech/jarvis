from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional
from ..schemas import ItemCreate, ItemUpdate, ItemOut
from ..crud import ItemCRUD
from ..db import get_collection

router = APIRouter(prefix="/items", tags=["items"])

def get_crud() -> ItemCRUD:
    return ItemCRUD(get_collection())

@router.post("", response_model=ItemOut, status_code=201)
async def create_item(payload: ItemCreate, crud: ItemCRUD = Depends(get_crud)):
    created = await crud.create(payload.model_dump())
    return created

@router.get("", response_model=List[ItemOut])
async def list_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    q: Optional[str] = Query(None),
    crud: ItemCRUD = Depends(get_crud),
):
    items = await crud.list(skip=skip, limit=limit, q=q)
    return items

@router.get("/{item_id}", response_model=ItemOut)
async def get_item(item_id: str, crud: ItemCRUD = Depends(get_crud)):
    doc = await crud.get(item_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Item not found")
    return doc

@router.put("/{item_id}", response_model=ItemOut)
async def replace_item(item_id: str, payload: ItemCreate, crud: ItemCRUD = Depends(get_crud)):
    replaced = await crud.replace(item_id, payload.model_dump())
    if not replaced:
        raise HTTPException(status_code=404, detail="Item not found")
    return replaced

@router.patch("/{item_id}", response_model=ItemOut)
async def update_item(item_id: str, payload: ItemUpdate, crud: ItemCRUD = Depends(get_crud)):
    update_data = {k: v for k, v in payload.model_dump(exclude_none=True).items()}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    updated = await crud.update(item_id, update_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated

@router.delete("/{item_id}", status_code=204)
async def delete_item(item_id: str, crud: ItemCRUD = Depends(get_crud)):
    ok = await crud.delete(item_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Item not found")
    return None