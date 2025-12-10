from bson import ObjectId
from bson.errors import InvalidId
from typing import List, Type, TypeVar

T = TypeVar("T")

async def insert_one(collection, payload: dict) -> T:
  result = await collection.insert_one(payload)
  saved = await collection.find_one({"_id": result.inserted_id})
  saved["_id"] = str(saved["_id"])
  return saved

async def update_one(collection, doc_id, payload: dict) -> T:
  result = await collection.update_one(
    {"_id": ObjectId(doc_id)},
    {"$set": payload},
  )
  return result

async def find_one_query(collection, query):
  result = await collection.find_one(query)
  if not result:
    return None
  
  result["_id"] = str(result["_id"])
  return result

async def find_one_by_id(collection, object_id):
  try:
    _object_id = ObjectId(object_id)
  except InvalidId:
    return None
  
  result = await collection.find_one({"_id": ObjectId(_object_id)})
  if not result:
    return None
  
  result["_id"] = str(result["_id"])
  return result