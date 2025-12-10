from datetime import datetime
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from ..._utils.database import db
from ..._utils.query_manager import find_one_query, insert_one
from ..._utils.password_manager import hash_password
from ...models.users_model import User, UserMutable

COLLECTION = db["users"]

USER_ROLE = [
  'ROOT_ADMIN',
  'TEACHER',
  'ANOTATOR'
]

async def user_registration(payload: UserMutable) -> User:
  try:
    now = datetime.now()
    hash_pass = hash_password(payload.password)

    eisting_email = await find_one_query(COLLECTION, { 'email': payload.email })
    if eisting_email:
      return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
          "status": 400,
          "message": "Your email is already in use",
          "data": {}
        }
      )

    print("registration: \n", eisting_email)
    
    if payload.userRole == '' or payload.userRole.lower() not in [role.lower() for role in USER_ROLE ]:
      return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
          "status": 400,
          "message": f"userRole must be one of these {', '.join(USER_ROLE)}",
          "data": {}
        }
      )

    doc = {
      "username": payload.username if "" else payload.username,
      "email": payload.email,
      "password": hash_pass,
      "userRole": payload.userRole.upper(),
      "accessToken": "",
      "createdAt": now,
      "updatedAt": now
    }

    result = await insert_one(COLLECTION, doc)

    return JSONResponse(
      status_code=status.HTTP_200_OK,
      content={
        "status": 200,
        "message": "Registration successfull",
        "data": jsonable_encoder(User(**result))
      }
    )
  except Exception as error:
    print("error user registration: \n", error)
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail=str(error)
    )