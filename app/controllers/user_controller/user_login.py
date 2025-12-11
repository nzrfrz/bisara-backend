from datetime import datetime
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse

from ..._utils.database import db
from ..._utils.password_manager import verify_password
from ..._utils.jwt_manager import access_token_generator
from ..._utils.query_manager import find_one_query, find_one_by_id, update_one

from ...models.users_model import User, UserMutable

COLLECTION = db["users"]

async def user_login(payload: UserMutable) -> User:
  try:
    user_found = await find_one_query(
      COLLECTION,
      {
        "$or": [
          { "username": payload.credential },
          { "email": payload.credential }
        ]
      }
    )

    if not user_found:
      # user not found
      return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
          "status": 404,
          "message": "User not found",
          "data": {}
        }
      )
    
    # verify password if user is found
    if not verify_password(payload.password, user_found["password"]):
      return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
          "status": 400,
          "message": "Wrong password",
          "data": {}
        }
      )
    
    user_found_id = str(user_found["_id"])
    
    # create access token
    access_token = access_token_generator({
      "_id": user_found_id,
      "email": user_found["email"],
      "username": user_found.get("username"),
    })

    # update the access token field in DB
    await update_one(COLLECTION, user_found_id, { "accessToken": access_token, "updatedAt": datetime.now() })
    user_updated = await find_one_by_id(COLLECTION, user_found_id)

    response = JSONResponse(
      status_code=status.HTTP_200_OK,
      content={
        "status": 200,
        "message": "Login successfull",
        "data": {
          "username": user_found["username"],
          "email": user_found["email"],
          "userRole": user_updated["userRole"],
          "accessToken": user_updated["accessToken"]
        }
      }
    )
    return response
  except Exception as error:
    print("error user login: \n", error)
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail=str(error)
    )