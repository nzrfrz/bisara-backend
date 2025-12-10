import os
# import re
from fastapi import Request, status
from typing import Dict, Any
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError, ExpiredSignatureError

SECRET_KEY = os.getenv("ACCESS_TOKEN_SECRET", "secret")
ALGORITHM = "HS256"
EXPIRATION_MINUTES = 480

class TokenExpiredError(Exception):
  pass

class TokenInvalidError(Exception):
  pass

def access_token_generator(data: dict):
  to_encode = data.copy()
  expire = datetime.now(timezone.utc) + timedelta(minutes=EXPIRATION_MINUTES)

  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

  return encoded_jwt

async def access_token_verifier(request: Request) -> Dict[str, Any]:
  try:
    # pattern = r"['\s\{\}]"
    # cookies_parts = re.sub(pattern, "", str(request.cookies.get("accessToken"))).strip("accessToken:").split(";r")
    # token = cookies_parts[-1]
    token = request.cookies.get("accessToken")
    if not token:
      raise TokenInvalidError("Missing access token")
    
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload
  except ExpiredSignatureError as error:
    raise TokenExpiredError("Token has expired") from error
  except JWTError as error:
    raise TokenInvalidError("Invalid token") from error
  
def response_token_expired():
  response = JSONResponse(
    status_code=status.HTTP_401_UNAUTHORIZED,
    content={
      "status": 401,
      "message": "Access token has expired",
    }
  )
  response.delete_cookie("accessToken", path="/")
  response.delete_cookie("user", path="/")
  return response

def response_token_invalid():
  response = JSONResponse(
    status_code=status.HTTP_401_UNAUTHORIZED,
    content={
      "status": 401,
      "message": "Unauthorized Access",
    }
  )
  return response