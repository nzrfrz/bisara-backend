from fastapi import HTTPException, status
from fastapi.responses import JSONResponse

from ..._utils.database import db
from ..._utils.query_manager import find_one_by_id

COLLECTION = db["users"]

async def user_me(user_id):
  try:
    get_me = await find_one_by_id(COLLECTION, user_id)

    return JSONResponse(
      status_code=status.HTTP_200_OK,
      content={
        "status": 200,
        "message": "Payload Received",
        "data": {
          "_id": str(get_me["_id"]),
          "username": get_me["username"],
          "email": get_me["email"],
          "userRole": get_me["userRole"],
        }
      }
    )
  except Exception as error:
    print("error user me: \n", error)
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail=str(error)
    )