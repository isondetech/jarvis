from typing import Optional, List, Any, Dict
from datetime import datetime
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection
from .models import item_to_dict

class ItemCRUD:
    def __init__(self, coll: AsyncIOMotorCollection):
        self.coll = coll
        # Simple index for text search over name/description
        # This is idempotent and runs once on first use.
        self._ensure_indexes_task = None

    async def ensure_indexes(self):
        await self.coll.create_index([("name", "text"), ("description", "text")], name="text_idx")

    async def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        now = datetime.utcnow()
        doc = {**data, "created_at": now, "updated_at": now}
        res = await self.coll.insert_one(doc)
        created = await self.coll.find_one({"_id": res.inserted_id})
        return item_to_dict(created)

    async def get(self, id: str) -> Optional[Dict[str, Any]]:
        if not ObjectId.is_valid(id):
            return None
        doc = await self.coll.find_one({"_id": ObjectId(id)})
        if not doc:
            return None
        return item_to_dict(doc)

    async def list(self, skip: int = 0, limit: int = 20, q: Optional[str] = None) -> List[Dict[str, Any]]:
        query: Dict[str, Any] = {}
        if q:
            query = {"$text": {"$search": q}}
        cursor = self.coll.find(query).skip(skip).limit(limit).sort([("_id", -1)])
        return [item_to_dict(d) async for d in cursor]

    async def replace(self, id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if not ObjectId.is_valid(id):
            return None
        data["updated_at"] = datetime.utcnow()
        res = await self.coll.find_one_and_replace(
            {"_id": ObjectId(id)},
            {**data, "created_at": datetime.utcnow()},  # preserve created_at if needed (simplified)
            return_document=True,
        )
        return item_to_dict(res) if res else None

    async def update(self, id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if not ObjectId.is_valid(id):
            return None
        update_doc = {"$set": {**data, "updated_at": datetime.utcnow()}}
        res = await self.coll.find_one_and_update(
            {"_id": ObjectId(id)},
            update_doc,
            return_document=True,
        )
        return item_to_dict(res) if res else None

    async def delete(self, id: str) -> bool:
        if not ObjectId.is_valid(id):
            return False
        res = await self.coll.delete_one({"_id": ObjectId(id)})
        return res.deleted_count == 1