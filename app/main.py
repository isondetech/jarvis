from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes.items import router as items_router
from .db import get_collection
from .crud import ItemCRUD

app = FastAPI(title="FastAPI MongoDB CRUD", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup():
    # Ensure text index exists
    crud = ItemCRUD(get_collection())
    try:
        await crud.ensure_indexes()
    except Exception:
        # Non-fatal if index creation fails on startup
        pass

@app.get("/", tags=["health"])
async def health():
    return {"status": "ok"}

app.include_router(items_router)