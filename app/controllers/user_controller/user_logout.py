from fastapi import HTTPException, status
from fastapi.responses import JSONResponse

from ..._utils.database import db

COLLECTION = db["users"]

async def user_logout(user_id):
  try:
    return JSONResponse(
      status_code=status.HTTP_200_OK,
      content={
        "status": 200,
        "message": "You have been logged out",
        "data": {
          "_id": user_id
        }
      }
    )
  except Exception as error:
    print("error user logout: \n", error)
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail=str(error)
    )