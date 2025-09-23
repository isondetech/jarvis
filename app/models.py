from typing import Any
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate  # type: ignore[misc]

    @classmethod
    def validate(cls, v: Any):
        if isinstance(v, ObjectId):
            return v
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

def item_to_dict(doc: dict) -> dict:
    if not doc:
        return doc
    doc = {**doc}
    _id = doc.pop("_id", None)
    if _id is not None:
        doc["id"] = str(_id)
    return doc