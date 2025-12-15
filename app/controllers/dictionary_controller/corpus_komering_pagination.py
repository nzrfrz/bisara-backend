import re
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from ..._utils.database import db
from ..._utils.query_manager import pagination

COLLECTION = db["corpus_komering"]

async def corpus_komering_pagination(page, limit, corpus_status, q):
  try:
    query = {}
    if corpus_status:
      query['status'] = corpus_status.upper()

    if not q != "" or q:
      regex = re.compile(q, re.IGNORECASE)
      query["$or"] = [
        { "indonesia": regex },
        { "komering": regex },
      ]

    results = await pagination(COLLECTION, page=page, limit=limit, query=query)

    # print(page, limit, corpus_status, q)
    return JSONResponse(
      status_code=status.HTTP_200_OK,
      content={
        "status": 200,
        "message": "Success",
        "data": jsonable_encoder(results)
      }
    )
  except Exception as error:
    print("error corpus lampung pagination: \n", error)
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail=str(error)
    )