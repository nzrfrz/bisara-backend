import math
from bson import ObjectId
from bson.errors import InvalidId
from typing import List, Type, TypeVar, Dict, Any

T = TypeVar("T")

async def insert_one(collection, payload: dict) -> T:
  result = await collection.insert_one(payload)
  saved = await collection.find_one({"_id": result.inserted_id})
  saved["_id"] = str(saved["_id"])
  return saved

async def insert_many_chunked(collection, payloads: List[dict], chunk_size = 1000):
  total_inserted = 0
  for i in range(0, len(payloads), chunk_size):
    chunk = payloads[i:i + chunk_size]
    results = await collection.insert_many(chunk)
    total_inserted += len(results.inserted_ids)
  return total_inserted

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

async def pagination(
  collection, *,
  page: int = 1,
  limit: int = 10,
  query: Dict[str, Any] | None = None,
  sort: List[tuple] | None = None
):
  if page < 1: 
    page = 1
  if limit < 1:
    limit = 10

  query = query or {}
  skip = (page - 1) * limit

  total_item = await collection.count_documents(query)
  # list_all_docs = await collection.find().to_list()
  total_page = math.ceil(total_item / limit) if total_item > 0 else 1

  cursor = (collection.find(query).skip(skip).limit(limit))

  if sort:
    cursor = cursor.sort(sort)
  
  items = []
  async for doc in cursor:
    doc['_id'] = str(doc['_id'])
    items.append(doc)

  return {
    "meta": {
      "page": page,
      "limit": limit,
      "totalPage": total_page,
      "totalItem": total_item
    },
    "itemList": items
  }